"""
API 응답 형식 정의

모든 API 응답에서 일관된 형식을 사용합니다.
"""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """표준 API 응답 형식"""

    success: bool = True
    message: str = "성공"
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """페이지네이션이 포함된 응답"""

    success: bool = True
    message: str = "성공"
    data: list[T] = []
    total: int = 0
    page: int = 1
    limit: int = 10
    has_next: bool = False


def success_response(data: Any = None, message: str = "성공") -> dict:
    """성공 응답 생성"""
    return {"success": True, "message": message, "data": data}


def error_response(message: str = "오류가 발생했습니다.") -> dict:
    """에러 응답 생성"""
    return {"success": False, "message": message, "data": None}
