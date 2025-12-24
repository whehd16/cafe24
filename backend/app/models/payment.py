"""
결제 관련 모델 정의
"""
from typing import Optional
from pydantic import BaseModel


class PaymentRequest(BaseModel):
    """결제 요청 (프론트엔드 → 백엔드)"""

    order_id: str  # 내부 주문 ID
    amount: int  # 결제 금액
    order_name: str  # 주문명 (예: "티셔츠 외 2건")
    customer_name: str
    customer_email: Optional[str] = None


class PaymentConfirm(BaseModel):
    """결제 승인 요청 (토스 콜백 후)"""

    payment_key: str  # 토스에서 발급한 결제 키
    order_id: str  # 주문 ID
    amount: int  # 결제 금액


class PaymentResult(BaseModel):
    """결제 결과"""

    success: bool
    payment_key: Optional[str] = None
    order_id: str
    amount: int
    status: str  # DONE, CANCELED, FAILED 등
    message: str = ""
