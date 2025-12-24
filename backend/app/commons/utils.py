"""
공통 유틸리티 함수

여러 곳에서 사용하는 공통 함수들을 정의합니다.
"""
import uuid
from datetime import datetime
from typing import Any


def generate_uuid() -> str:
    """UUID 생성"""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """현재 시간을 ISO 형식으로 반환"""
    return datetime.now().isoformat()


def format_price(amount: int) -> str:
    """가격을 한국 원화 형식으로 포맷"""
    return f"{amount:,}원"


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """
    중첩된 딕셔너리에서 안전하게 값 가져오기

    예: safe_get(data, "product", "price", default=0)
    """
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result
