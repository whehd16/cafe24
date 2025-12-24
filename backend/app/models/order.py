"""
주문 관련 모델 정의
"""
from typing import Optional
from pydantic import BaseModel
from .product import ProductPrice


class OrderItem(BaseModel):
    """주문 상품"""

    id: str
    product_id: str
    variant_id: Optional[str] = None
    title: str
    quantity: int
    price: ProductPrice


class ShippingAddress(BaseModel):
    """배송 주소"""

    name: str  # 수령인
    phone: str  # 연락처
    zip_code: str  # 우편번호
    address1: str  # 기본 주소
    address2: str = ""  # 상세 주소


class Order(BaseModel):
    """주문"""

    id: str  # 주문 ID
    cafe24_order_id: Optional[str] = None  # 카페24 주문 ID
    status: str = "pending"  # pending, paid, shipped, delivered, cancelled
    items: list[OrderItem] = []
    shipping_address: Optional[ShippingAddress] = None
    total_price: ProductPrice
    payment_id: Optional[str] = None  # 토스 결제 ID
    created_at: str
    updated_at: str


class CreateOrderRequest(BaseModel):
    """주문 생성 요청"""

    cart_id: str
    shipping_address: ShippingAddress
