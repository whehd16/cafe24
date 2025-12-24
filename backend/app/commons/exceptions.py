"""
커스텀 예외 정의

API에서 발생하는 다양한 에러를 정의합니다.
"""
from fastapi import HTTPException, status


class Cafe24APIException(HTTPException):
    """카페24 API 호출 실패"""

    def __init__(self, detail: str = "카페24 API 호출에 실패했습니다."):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class Cafe24AuthException(HTTPException):
    """카페24 인증 실패"""

    def __init__(self, detail: str = "카페24 인증에 실패했습니다."):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TossPaymentException(HTTPException):
    """토스페이먼츠 결제 실패"""

    def __init__(self, detail: str = "결제 처리에 실패했습니다."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class CartNotFoundException(HTTPException):
    """장바구니를 찾을 수 없음"""

    def __init__(self, detail: str = "장바구니를 찾을 수 없습니다."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ProductNotFoundException(HTTPException):
    """상품을 찾을 수 없음"""

    def __init__(self, detail: str = "상품을 찾을 수 없습니다."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class OrderNotFoundException(HTTPException):
    """주문을 찾을 수 없음"""

    def __init__(self, detail: str = "주문을 찾을 수 없습니다."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
