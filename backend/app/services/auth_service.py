"""
인증 서비스

카페24 OAuth 인증을 처리합니다.
"""
from app.daos.cafe24_dao import cafe24_dao


class AuthService:
    """인증 관련 비즈니스 로직"""

    def __init__(self):
        self.cafe24 = cafe24_dao

    def get_login_url(self, state: str = "") -> str:
        """
        카페24 로그인 URL 생성

        이 URL을 브라우저에서 열면 카페24 로그인 페이지가 표시됩니다.
        """
        return self.cafe24.get_auth_url(state)

    async def handle_callback(self, code: str) -> dict:
        """
        OAuth 콜백 처리

        카페24에서 리다이렉트된 후 호출됩니다.
        인증 코드를 받아서 Access Token을 발급받습니다.
        """
        token_data = await self.cafe24.get_access_token(code)

        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "expires_in": token_data.get("expires_in", 7200),  # 기본 2시간
            "token_type": "Bearer",
        }

    async def refresh_token(self) -> dict:
        """
        토큰 갱신

        Access Token이 만료되면 Refresh Token으로 갱신합니다.
        """
        token_data = await self.cafe24.refresh_access_token()

        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_in": token_data.get("expires_in", 7200),
        }

    def set_tokens(self, access_token: str, refresh_token: str):
        """
        토큰 설정

        발급받은 토큰을 DAO에 설정합니다.
        """
        self.cafe24.set_tokens(access_token, refresh_token)


# 싱글톤 인스턴스
auth_service = AuthService()
