"""
토스페이먼츠 API 호출 담당 DAO

토스페이먼츠 결제 API와 통신합니다.
- 결제 승인
- 결제 취소
- 결제 조회
"""
import httpx
import base64
from app.commons.config import get_settings
from app.commons.exceptions import TossPaymentException


class TossDAO:
    """토스페이먼츠 API 클라이언트"""

    BASE_URL = "https://api.tosspayments.com/v1"

    def __init__(self):
        self.settings = get_settings()

    def _get_headers(self) -> dict:
        """API 요청 헤더 (Basic Auth)"""
        # 토스는 Secret Key를 Base64로 인코딩해서 사용
        secret_key = self.settings.toss_secret_key
        encoded = base64.b64encode(f"{secret_key}:".encode()).decode()

        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json",
        }

    async def confirm_payment(
        self,
        payment_key: str,
        order_id: str,
        amount: int,
    ) -> dict:
        """
        결제 승인

        프론트엔드에서 결제가 완료되면 이 API를 호출해서 최종 승인합니다.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/payments/confirm",
                headers=self._get_headers(),
                json={
                    "paymentKey": payment_key,
                    "orderId": order_id,
                    "amount": amount,
                },
            )

            if response.status_code != 200:
                error_data = response.json()
                raise TossPaymentException(
                    f"결제 승인 실패: {error_data.get('message', '알 수 없는 오류')}"
                )

            return response.json()

    async def get_payment(self, payment_key: str) -> dict:
        """결제 정보 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/payments/{payment_key}",
                headers=self._get_headers(),
            )

            if response.status_code != 200:
                raise TossPaymentException("결제 정보 조회 실패")

            return response.json()

    async def cancel_payment(
        self,
        payment_key: str,
        cancel_reason: str,
        cancel_amount: int = None,
    ) -> dict:
        """
        결제 취소

        전체 취소 또는 부분 취소가 가능합니다.
        """
        data = {"cancelReason": cancel_reason}
        if cancel_amount:
            data["cancelAmount"] = cancel_amount

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/payments/{payment_key}/cancel",
                headers=self._get_headers(),
                json=data,
            )

            if response.status_code != 200:
                error_data = response.json()
                raise TossPaymentException(
                    f"결제 취소 실패: {error_data.get('message', '알 수 없는 오류')}"
                )

            return response.json()


# 싱글톤 인스턴스
toss_dao = TossDAO()
