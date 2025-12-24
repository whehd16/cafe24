"""
상품 컨트롤러

상품 조회 관련 API 엔드포인트
"""
from typing import Optional
from fastapi import APIRouter, Query
from app.services.product_service import product_service
from app.commons.response import success_response

router = APIRouter(prefix="/products", tags=["상품"])


@router.get("")
async def get_products(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 상품 수"),
    category: Optional[int] = Query(None, description="카테고리 번호"),
):
    """
    상품 목록 조회

    카페24에서 상품 목록을 가져옵니다.

    **파라미터:**
    - page: 페이지 번호 (1부터 시작)
    - limit: 페이지당 상품 수 (최대 100)
    - category: 특정 카테고리의 상품만 조회

    **응답 예시:**
    ```json
    {
        "success": true,
        "data": {
            "products": [...],
            "total": 100,
            "page": 1,
            "limit": 10,
            "has_next": true
        }
    }
    ```
    """
    result = await product_service.get_products(
        page=page,
        limit=limit,
        category_no=category,
    )
    return success_response(data=result.model_dump())


@router.get("/categories")
async def get_categories():
    """
    카테고리 목록 조회

    모든 상품 카테고리를 조회합니다.
    """
    categories = await product_service.get_categories()
    return success_response(data=[c.model_dump() for c in categories])


@router.get("/{product_id}")
async def get_product(product_id: str):
    """
    상품 상세 조회

    특정 상품의 상세 정보를 조회합니다.

    **파라미터:**
    - product_id: 상품 ID (카페24의 product_no)

    **응답에 포함되는 정보:**
    - 상품명, 설명
    - 가격, 할인가
    - 이미지
    - 옵션 (사이즈, 색상 등)
    """
    product = await product_service.get_product(product_id)
    return success_response(data=product.model_dump())
