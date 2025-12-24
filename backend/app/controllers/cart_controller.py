"""
장바구니 컨트롤러

장바구니 관련 API 엔드포인트
"""
from typing import Optional
from fastapi import APIRouter, Cookie, Response
from app.services.cart_service import cart_service
from app.models.cart import AddToCartRequest, UpdateCartItemRequest
from app.commons.response import success_response

router = APIRouter(prefix="/cart", tags=["장바구니"])


@router.get("")
async def get_cart(
    response: Response,
    cart_id: Optional[str] = Cookie(None, description="장바구니 ID (쿠키)"),
):
    """
    장바구니 조회

    현재 장바구니 내용을 조회합니다.
    장바구니가 없으면 새로 생성합니다.

    **쿠키:** cart_id - 장바구니 식별자
    """
    cart = cart_service.get_or_create_cart(cart_id)

    # 새 장바구니면 쿠키 설정
    if cart_id != cart.id:
        response.set_cookie(
            key="cart_id",
            value=cart.id,
            max_age=60 * 60 * 24 * 7,  # 7일
            httponly=True,
            samesite="lax",
        )

    return success_response(data=cart.model_dump())


@router.post("/items")
async def add_to_cart(
    request: AddToCartRequest,
    response: Response,
    cart_id: Optional[str] = Cookie(None),
):
    """
    장바구니에 상품 추가

    **요청 본문:**
    ```json
    {
        "product_id": "123",
        "variant_id": "옵션ID (선택)",
        "quantity": 1
    }
    ```
    """
    # 장바구니가 없으면 생성
    cart = cart_service.get_or_create_cart(cart_id)

    if cart_id != cart.id:
        response.set_cookie(
            key="cart_id",
            value=cart.id,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            samesite="lax",
        )

    updated_cart = await cart_service.add_item(cart.id, request)
    return success_response(
        data=updated_cart.model_dump(),
        message="장바구니에 추가되었습니다.",
    )


@router.put("/items/{item_id}")
async def update_cart_item(
    item_id: str,
    request: UpdateCartItemRequest,
    cart_id: Optional[str] = Cookie(None),
):
    """
    장바구니 아이템 수량 변경

    **파라미터:**
    - item_id: 장바구니 아이템 ID

    **요청 본문:**
    ```json
    {
        "quantity": 2
    }
    ```

    **참고:** 수량을 0으로 설정하면 삭제됩니다.
    """
    if not cart_id:
        return success_response(
            data=None,
            message="장바구니가 없습니다.",
        )

    updated_cart = cart_service.update_item(cart_id, item_id, request.quantity)
    return success_response(
        data=updated_cart.model_dump(),
        message="수량이 변경되었습니다.",
    )


@router.delete("/items/{item_id}")
async def remove_cart_item(
    item_id: str,
    cart_id: Optional[str] = Cookie(None),
):
    """
    장바구니에서 상품 삭제

    **파라미터:**
    - item_id: 삭제할 장바구니 아이템 ID
    """
    if not cart_id:
        return success_response(
            data=None,
            message="장바구니가 없습니다.",
        )

    updated_cart = cart_service.remove_item(cart_id, item_id)
    return success_response(
        data=updated_cart.model_dump(),
        message="상품이 삭제되었습니다.",
    )


@router.delete("")
async def clear_cart(
    cart_id: Optional[str] = Cookie(None),
):
    """
    장바구니 비우기

    모든 상품을 장바구니에서 삭제합니다.
    """
    if not cart_id:
        return success_response(
            data=None,
            message="장바구니가 없습니다.",
        )

    updated_cart = cart_service.clear_cart(cart_id)
    return success_response(
        data=updated_cart.model_dump(),
        message="장바구니를 비웠습니다.",
    )
