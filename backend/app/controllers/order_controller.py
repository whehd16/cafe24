"""
주문 컨트롤러

주문 생성 및 조회 관련 API 엔드포인트
"""
from typing import Optional
from fastapi import APIRouter, Query, Cookie
from app.services.order_service import order_service
from app.models.order import CreateOrderRequest
from app.commons.response import success_response

router = APIRouter(prefix="/orders", tags=["주문"])


@router.post("")
async def create_order(
    request: CreateOrderRequest,
    payment_key: str = Query(..., description="토스 결제 키"),
):
    """
    주문 생성

    결제 완료 후 주문을 생성합니다.
    카페24에도 주문이 등록됩니다.

    **요청 본문:**
    ```json
    {
        "cart_id": "장바구니 ID",
        "shipping_address": {
            "name": "홍길동",
            "phone": "010-1234-5678",
            "zip_code": "12345",
            "address1": "서울시 강남구",
            "address2": "101동 101호"
        }
    }
    ```

    **쿼리 파라미터:**
    - payment_key: 토스에서 받은 결제 키

    **주문 흐름:**
    1. 결제 완료 (토스)
    2. 이 API 호출
    3. 내부 주문 생성
    4. 카페24에 주문 등록
    5. 장바구니 비우기
    """
    order = await order_service.create_order(request, payment_key)
    return success_response(
        data=order.model_dump(),
        message="주문이 완료되었습니다.",
    )


@router.get("")
async def get_orders(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=50, description="페이지당 주문 수"),
):
    """
    주문 목록 조회

    내 주문 목록을 조회합니다.

    **파라미터:**
    - page: 페이지 번호
    - limit: 페이지당 주문 수

    **참고:** 현재는 인증 없이 모든 주문을 반환합니다.
    실제 서비스에서는 사용자별 필터링이 필요합니다.
    """
    orders = order_service.get_orders(page=page, limit=limit)
    return success_response(
        data=[o.model_dump() for o in orders],
    )


@router.get("/{order_id}")
async def get_order(order_id: str):
    """
    주문 상세 조회

    특정 주문의 상세 정보를 조회합니다.

    **파라미터:**
    - order_id: 주문 ID
    """
    order = order_service.get_order(order_id)
    return success_response(data=order.model_dump())


@router.post("/{order_id}/sync")
async def sync_order_status(order_id: str):
    """
    주문 상태 동기화

    카페24의 주문 상태를 가져와서 동기화합니다.
    배송 상태 등이 변경되었을 때 사용합니다.

    **파라미터:**
    - order_id: 주문 ID
    """
    order = await order_service.sync_order_status(order_id)
    return success_response(
        data=order.model_dump(),
        message="주문 상태가 동기화되었습니다.",
    )
