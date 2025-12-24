"""
장바구니 관련 모델 정의
"""
from typing import Optional
from pydantic import BaseModel
from .product import ProductImage, ProductPrice


class CartItem(BaseModel):
    """장바구니 아이템"""

    id: str  # 장바구니 아이템 고유 ID
    product_id: str  # 상품 ID
    variant_id: Optional[str] = None  # 옵션 ID
    title: str  # 상품명
    quantity: int
    price: ProductPrice
    image: Optional[ProductImage] = None


class Cart(BaseModel):
    """장바구니"""

    id: str  # 장바구니 ID (세션 기반)
    items: list[CartItem] = []
    total_quantity: int = 0
    total_price: ProductPrice = ProductPrice(amount="0", currency_code="KRW")


class AddToCartRequest(BaseModel):
    """장바구니 추가 요청"""

    product_id: str
    variant_id: Optional[str] = None
    quantity: int = 1


class UpdateCartItemRequest(BaseModel):
    """장바구니 아이템 수정 요청"""

    quantity: int
