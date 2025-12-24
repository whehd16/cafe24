"""
환경변수 설정 파일

.env 파일에서 환경변수를 읽어서 사용합니다.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """앱 설정"""

    # 카페24 설정
    cafe24_client_id: str = ""
    cafe24_client_secret: str = ""
    cafe24_mall_id: str = ""
    cafe24_redirect_uri: str = "http://localhost:3000/auth/callback"

    # 카페24 토큰 (개발자센터에서 발급받아 저장)
    cafe24_access_token: str = ""
    cafe24_refresh_token: str = ""

    # 토스페이먼츠 설정
    toss_client_key: str = ""
    toss_secret_key: str = ""

    # 서버 설정
    frontend_url: str = "http://localhost:3000"
    debug: bool = True
    secret_key: str = "change-this-secret-key"

    # 카페24 API 기본 URL (mall_id로 동적 생성)
    @property
    def cafe24_api_url(self) -> str:
        return f"https://{self.cafe24_mall_id}.cafe24api.com/api/v2/admin"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """설정 싱글톤 반환 (캐싱)"""
    return Settings()
