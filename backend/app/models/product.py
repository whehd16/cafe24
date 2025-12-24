"""
상품 관련 모델 정의
"""
from typing import Optional
from pydantic import BaseModel


class ProductImage(BaseModel):
    """상품 이미지"""

    url: str
    alt: str = ""


class ProductPrice(BaseModel):
    """상품 가격"""

    amount: str  # 문자열로 저장 (프론트엔드 호환)
    currency_code: str = "KRW"


class ProductVariant(BaseModel):
    """상품 옵션 (사이즈, 색상 등)"""

    id: str
    title: str
    price: ProductPrice
    available: bool = True


class Product(BaseModel):
    """상품 모델 (프론트엔드용)"""

    id: str
    handle: str  # URL용 식별자
    title: str
    description: str = ""
    price: ProductPrice
    compare_at_price: Optional[ProductPrice] = None  # 할인 전 가격
    featured_image: Optional[ProductImage] = None
    images: list[ProductImage] = []
    variants: list[ProductVariant] = []
    available: bool = True
    tags: list[str] = []
    category_no: Optional[int] = None


class ProductListResponse(BaseModel):
    """상품 목록 응답"""

    products: list[Product]
    total: int
    page: int
    limit: int
    has_next: bool


class Category(BaseModel):
    """카테고리 모델"""

    id: str
    name: str
    parent_id: Optional[str] = None
    path: str = ""  # 전체 경로 (예: "의류/상의/티셔츠")
