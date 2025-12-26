"""
상품 서비스

카페24 상품 데이터를 프론트엔드 형식으로 변환합니다.
"""
from typing import Optional
from app.daos.cafe24_dao import cafe24_dao
from app.models.product import (
    Product,
    ProductImage,
    ProductPrice,
    ProductVariant,
    ProductListResponse,
    Category,
)


class ProductService:
    """상품 관련 비즈니스 로직"""

    def __init__(self):
        self.cafe24 = cafe24_dao

    def _transform_product(self, cafe24_product: dict) -> Product:
        """
        카페24 상품 데이터를 프론트엔드 형식으로 변환

        카페24 API 응답:
        {
            "product_no": 123,
            "product_name": "티셔츠",
            "price": 29000,
            "detail_image": "http://...",
            ...
        }

        프론트엔드 형식:
        {
            "id": "123",
            "title": "티셔츠",
            "price": { "amount": "29000", "currency_code": "KRW" },
            ...
        }
        """
        # 기본 이미지 처리
        featured_image = None
        if cafe24_product.get("detail_image"):
            featured_image = ProductImage(
                url=cafe24_product["detail_image"],
                alt=cafe24_product.get("product_name", ""),
            )

        # 추가 이미지 처리
        images = []
        if featured_image:
            images.append(featured_image)
        for img in cafe24_product.get("additional_images", []):
            if img:
                images.append(ProductImage(url=img, alt=""))

        # 가격 처리
        price = ProductPrice(
            amount=str(cafe24_product.get("price", 0)),
            currency_code="KRW",
        )

        # 할인 전 가격
        compare_at_price = None
        if cafe24_product.get("retail_price"):
            compare_at_price = ProductPrice(
                amount=str(cafe24_product["retail_price"]),
                currency_code="KRW",
            )

        # 옵션(variants) 처리
        variants = []
        for variant in cafe24_product.get("variants", []) or []:
            if not variant:
                continue
            options = variant.get("options") or []
            option_value = options[0].get("value", "기본") if options else "기본"
            variants.append(
                ProductVariant(
                    id=str(variant.get("variant_code", "")),
                    title=option_value,
                    price=ProductPrice(
                        amount=str((variant.get("additional_amount") or 0) + (cafe24_product.get("price") or 0)),
                        currency_code="KRW",
                    ),
                    available=(variant.get("quantity") or 0) > 0,
                )
            )

        # 기본 옵션이 없으면 하나 추가
        if not variants:
            variants.append(
                ProductVariant(
                    id="default",
                    title="기본",
                    price=price,
                    available=True,
                )
            )

        return Product(
            id=str(cafe24_product.get("product_no", "")),
            handle=str(cafe24_product.get("product_no", "")),
            title=cafe24_product.get("product_name", ""),
            description=cafe24_product.get("description", ""),
            price=price,
            compare_at_price=compare_at_price,
            featured_image=featured_image,
            images=images,
            variants=variants,
            available=cafe24_product.get("display", "T") == "T",
            tags=cafe24_product.get("product_tag", "").split(",") if cafe24_product.get("product_tag") else [],
            category_no=cafe24_product.get("category", [{}])[0].get("category_no") if cafe24_product.get("category") and len(cafe24_product.get("category", [])) > 0 else None,
        )

    async def _get_child_category_ids(self, parent_category_no: int) -> list[int]:
        """부모 카테고리의 모든 하위 카테고리 ID 조회"""
        response = await self.cafe24.get_categories()
        categories = response.get("categories", [])

        child_ids = []
        for cat in categories:
            if cat.get("parent_category_no") == parent_category_no:
                child_ids.append(cat.get("category_no"))

        return child_ids

    async def get_products(
        self,
        page: int = 1,
        limit: int = 10,
        category_no: Optional[int] = None,
        include_children: bool = True,
    ) -> ProductListResponse:
        """상품 목록 조회"""
        offset = (page - 1) * limit

        all_products = []
        seen_product_ids = set()

        if category_no and include_children:
            # 대분류 + 하위 카테고리 모두 조회
            category_ids = [category_no]
            child_ids = await self._get_child_category_ids(category_no)
            category_ids.extend(child_ids)

            print(f"[DEBUG] 카테고리 {category_no} + 하위 카테고리 {child_ids} 조회")

            for cat_id in category_ids:
                response = await self.cafe24.get_products(
                    limit=100,  # 각 카테고리에서 충분히 가져오기
                    offset=0,
                    category_no=cat_id,
                )
                for p in response.get("products", []):
                    product_no = p.get("product_no")
                    if product_no not in seen_product_ids:
                        seen_product_ids.add(product_no)
                        all_products.append(self._transform_product(p))

            # 페이지네이션 적용
            total = len(all_products)
            products = all_products[offset:offset + limit]
            has_next = offset + limit < total
        else:
            # 카테고리 없거나 하위 포함 안 함
            response = await self.cafe24.get_products(
                limit=limit,
                offset=offset,
                category_no=category_no,
            )
            products = [
                self._transform_product(p) for p in response.get("products", [])
            ]
            total = response.get("count", len(products))
            has_next = offset + limit < total

        return ProductListResponse(
            products=products,
            total=total,
            page=page,
            limit=limit,
            has_next=has_next,
        )

    async def get_product(self, product_id: str) -> Product:
        """상품 상세 조회"""
        from app.commons.exceptions import ProductNotFoundException

        try:
            response = await self.cafe24.get_product(int(product_id))
            print(f"[DEBUG] 카페24 응답: {response}")  # 디버깅용
            product_data = response.get("product", {})

            if not product_data:
                raise ProductNotFoundException(f"상품 ID {product_id}를 찾을 수 없습니다.")

            return self._transform_product(product_data)
        except ValueError:
            raise ProductNotFoundException(f"잘못된 상품 ID: {product_id}")
        except Exception as e:
            import traceback
            print(f"[ERROR] 상품 조회 에러: {traceback.format_exc()}")
            if "ProductNotFoundException" in str(type(e)):
                raise
            raise ProductNotFoundException(f"상품 조회 실패: {str(e)}")

    async def get_categories(self) -> list[Category]:
        """카테고리 목록 조회"""
        response = await self.cafe24.get_categories()

        categories = []
        for cat in response.get("categories", []):
            categories.append(
                Category(
                    id=str(cat.get("category_no", "")),
                    name=cat.get("category_name", ""),
                    parent_id=str(cat.get("parent_category_no", "")) if cat.get("parent_category_no") else None,
                    path=cat.get("full_category_name", {}).get("1", ""),
                )
            )

        return categories


# 싱글톤 인스턴스
product_service = ProductService()
