"""
결제 컨트롤러

토스페이먼츠 결제 관련 API 엔드포인트
"""
from fastapi import APIRouter
from app.services.payment_service import payment_service
from app.models.payment import PaymentConfirm
from app.commons.response import success_response

router = APIRouter(prefix="/payments", tags=["결제"])


@router.get("/client-key")
async def get_client_key():
    """
    토스 Client Key 조회

    프론트엔드에서 토스 결제 위젯을 초기화할 때 필요한 키입니다.

    **사용 방법:**
    ```javascript
    const clientKey = await fetch('/api/payments/client-key');
    const tossPayments = TossPayments(clientKey);
    ```
    """
    client_key = payment_service.get_client_key()
    return success_response(data={"client_key": client_key})


@router.post("/confirm")
async def confirm_payment(request: PaymentConfirm):
    """
    결제 승인

    프론트엔드에서 토스 결제가 완료되면 이 API를 호출합니다.
    백엔드에서 최종 승인을 해야 결제가 완료됩니다.

    **요청 본문:**
    ```json
    {
        "payment_key": "토스에서 받은 paymentKey",
        "order_id": "주문 ID",
        "amount": 29000
    }
    ```

    **결제 흐름:**
    1. 프론트엔드: 토스 결제 위젯으로 결제 시작
    2. 사용자: 결제 수단 선택 및 결제
    3. 토스: 결제 완료 후 프론트엔드로 paymentKey 전달
    4. 프론트엔드: 이 API 호출
    5. 백엔드: 토스 API로 최종 승인
    """
    result = await payment_service.confirm_payment(request)
    return success_response(
        data=result.model_dump(),
        message=result.message,
    )


@router.get("/{payment_key}")
async def get_payment(payment_key: str):
    """
    결제 정보 조회

    결제 상세 정보를 조회합니다.

    **파라미터:**
    - payment_key: 토스에서 발급한 결제 키
    """
    payment_info = await payment_service.get_payment_info(payment_key)
    return success_response(data=payment_info)


@router.post("/{payment_key}/cancel")
async def cancel_payment(
    payment_key: str,
    cancel_reason: str = "고객 요청",
    cancel_amount: int = None,
):
    """
    결제 취소

    결제를 취소합니다. 전체 취소 또는 부분 취소가 가능합니다.

    **파라미터:**
    - payment_key: 결제 키
    - cancel_reason: 취소 사유
    - cancel_amount: 취소 금액 (없으면 전체 취소)
    """
    result = await payment_service.cancel_payment(
        payment_key=payment_key,
        cancel_reason=cancel_reason,
        cancel_amount=cancel_amount,
    )
    return success_response(
        data=result.model_dump(),
        message=result.message,
    )
