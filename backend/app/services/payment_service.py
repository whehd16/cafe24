"""
결제 서비스

토스페이먼츠 결제를 처리합니다.
"""
from app.daos.toss_dao import toss_dao
from app.models.payment import PaymentConfirm, PaymentResult
from app.commons.config import get_settings


class PaymentService:
    """결제 관련 비즈니스 로직"""

    def __init__(self):
        self.toss = toss_dao
        self.settings = get_settings()

    def get_client_key(self) -> str:
        """프론트엔드용 Client Key 반환"""
        return self.settings.toss_client_key

    async def confirm_payment(self, payment_data: PaymentConfirm) -> PaymentResult:
        """
        결제 승인

        프론트엔드에서 토스 결제가 완료되면 이 API를 호출합니다.
        백엔드에서 최종 승인을 해야 결제가 완료됩니다.
        """
        result = await self.toss.confirm_payment(
            payment_key=payment_data.payment_key,
            order_id=payment_data.order_id,
            amount=payment_data.amount,
        )

        return PaymentResult(
            success=result.get("status") == "DONE",
            payment_key=result.get("paymentKey"),
            order_id=result.get("orderId"),
            amount=result.get("totalAmount", payment_data.amount),
            status=result.get("status", "UNKNOWN"),
            message="결제가 완료되었습니다." if result.get("status") == "DONE" else "결제 처리 중",
        )

    async def get_payment_info(self, payment_key: str) -> dict:
        """결제 정보 조회"""
        return await self.toss.get_payment(payment_key)

    async def cancel_payment(
        self,
        payment_key: str,
        cancel_reason: str,
        cancel_amount: int = None,
    ) -> PaymentResult:
        """결제 취소"""
        result = await self.toss.cancel_payment(
            payment_key=payment_key,
            cancel_reason=cancel_reason,
            cancel_amount=cancel_amount,
        )

        return PaymentResult(
            success=True,
            payment_key=result.get("paymentKey"),
            order_id=result.get("orderId"),
            amount=result.get("totalAmount", 0),
            status="CANCELED",
            message="결제가 취소되었습니다.",
        )


# 싱글톤 인스턴스
payment_service = PaymentService()
