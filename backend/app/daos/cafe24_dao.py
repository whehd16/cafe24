"""
카페24 API 호출 담당 DAO

카페24 Admin API와 통신합니다.
- 상품 조회
- 주문 생성/조회
- 카테고리 조회
"""
import json
import httpx
from pathlib import Path
from typing import Optional
from app.commons.config import get_settings
from app.commons.exceptions import Cafe24APIException, Cafe24AuthException

# 토큰 저장 파일 경로
TOKEN_FILE = Path(__file__).parent.parent.parent / "token.json"


class Cafe24DAO:
    """카페24 API 클라이언트"""

    def __init__(self):
        self.settings = get_settings()
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        # 서버 시작 시 토큰 로드
        self._load_tokens()

    @property
    def base_url(self) -> str:
        """카페24 API 기본 URL"""
        return f"https://{self.settings.cafe24_mall_id}.cafe24api.com/api/v2/admin"

    @property
    def auth_url(self) -> str:
        """카페24 OAuth URL"""
        return f"https://{self.settings.cafe24_mall_id}.cafe24api.com/api/v2/oauth"

    def _load_tokens(self):
        """토큰 로드 (파일 → .env 순서)"""
        # 1. 파일에서 로드 시도
        if TOKEN_FILE.exists():
            try:
                with open(TOKEN_FILE, "r") as f:
                    data = json.load(f)
                    self._access_token = data.get("access_token")
                    self._refresh_token = data.get("refresh_token")
                    print(f"토큰 로드 완료 (파일)")
                    return
            except Exception as e:
                print(f"토큰 파일 로드 실패: {e}")

        # 2. .env에서 로드
        if self.settings.cafe24_access_token:
            self._access_token = self.settings.cafe24_access_token
            self._refresh_token = self.settings.cafe24_refresh_token
            print(f"토큰 로드 완료 (.env)")

    def _save_tokens(self):
        """토큰을 파일에 저장"""
        try:
            with open(TOKEN_FILE, "w") as f:
                json.dump({
                    "access_token": self._access_token,
                    "refresh_token": self._refresh_token,
                }, f)
            print(f"토큰 저장 완료")
        except Exception as e:
            print(f"토큰 저장 실패: {e}")

    def set_tokens(self, access_token: str, refresh_token: str):
        """토큰 설정 및 저장"""
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._save_tokens()

    def _get_headers(self) -> dict:
        """API 요청 헤더"""
        if not self._access_token:
            raise Cafe24AuthException("Access token이 없습니다. 먼저 로그인하세요.")

        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
            "X-Cafe24-Api-Version": "2025-12-01",
        }

    # ========== 인증 관련 ==========

    def get_auth_url(self, state: str = "") -> str:
        """OAuth 인증 URL 생성 (브라우저에서 열 URL)"""
        params = {
            "response_type": "code",
            "client_id": self.settings.cafe24_client_id,
            "redirect_uri": self.settings.cafe24_redirect_uri,
            "scope": "mall.read_product,mall.read_category,mall.write_order,mall.read_order",
            "state": state,
        }
        query = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.auth_url}/authorize?{query}"

    async def get_access_token(self, auth_code: str) -> dict:
        """인증 코드로 Access Token 발급"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.auth_url}/token",
                data={
                    "grant_type": "authorization_code",
                    "code": auth_code,
                    "redirect_uri": self.settings.cafe24_redirect_uri,
                },
                auth=(
                    self.settings.cafe24_client_id,
                    self.settings.cafe24_client_secret,
                ),
            )

            if response.status_code != 200:
                raise Cafe24AuthException(f"토큰 발급 실패: {response.text}")

            data = response.json()
            self.set_tokens(data["access_token"], data["refresh_token"])
            return data

    async def refresh_access_token(self) -> dict:
        """Refresh Token으로 Access Token 갱신"""
        if not self._refresh_token:
            raise Cafe24AuthException("Refresh token이 없습니다.")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.auth_url}/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self._refresh_token,
                },
                auth=(
                    self.settings.cafe24_client_id,
                    self.settings.cafe24_client_secret,
                ),
            )

            if response.status_code != 200:
                raise Cafe24AuthException(f"토큰 갱신 실패: {response.text}")

            data = response.json()
            self.set_tokens(
                data["access_token"],
                data.get("refresh_token", self._refresh_token)
            )
            return data

    async def _request_with_retry(self, method: str, url: str, **kwargs) -> httpx.Response:
        """
        API 요청 (토큰 만료 시 자동 갱신)

        401 에러 발생 시 토큰을 갱신하고 재시도합니다.
        """
        async with httpx.AsyncClient() as client:
            # 첫 번째 시도
            response = await client.request(method, url, headers=self._get_headers(), **kwargs)

            # 401 (토큰 만료) → 갱신 후 재시도
            if response.status_code == 401:
                print("토큰 만료됨, 갱신 시도...")
                try:
                    await self.refresh_access_token()
                    response = await client.request(method, url, headers=self._get_headers(), **kwargs)
                except Exception as e:
                    raise Cafe24AuthException(f"토큰 갱신 실패: {e}")

            return response

    # ========== 상품 관련 ==========

    async def get_products(
        self,
        limit: int = 10,
        offset: int = 0,
        category_no: Optional[int] = None,
    ) -> dict:
        """상품 목록 조회"""
        params = {"limit": limit, "offset": offset}

        # 카테고리 필터링은 category 파라미터 사용
        if category_no:
            params["category"] = category_no
            print(f"[DEBUG] 카테고리 {category_no} 상품 조회, params: {params}")

        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/products",
            params=params,
        )

        if response.status_code != 200:
            raise Cafe24APIException(f"상품 조회 실패: {response.text}")

        return response.json()

    async def get_product(self, product_no: int) -> dict:
        """상품 상세 조회"""
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/products/{product_no}",
            params={"embed": "variants,images"},
        )

        if response.status_code != 200:
            raise Cafe24APIException(f"상품 조회 실패: {response.text}")

        return response.json()

    # ========== 카테고리 관련 ==========

    async def get_categories(self) -> dict:
        """카테고리 목록 조회"""
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/categories",
        )

        if response.status_code != 200:
            raise Cafe24APIException(f"카테고리 조회 실패: {response.text}")

        return response.json()

    # ========== 주문 관련 ==========

    async def create_order(self, order_data: dict) -> dict:
        """주문 생성"""
        response = await self._request_with_retry(
            "POST",
            f"{self.base_url}/orders",
            json=order_data,
        )

        if response.status_code not in [200, 201]:
            raise Cafe24APIException(f"주문 생성 실패: {response.text}")

        return response.json()

    async def get_order(self, order_id: str) -> dict:
        """주문 조회"""
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/orders/{order_id}",
        )

        if response.status_code != 200:
            raise Cafe24APIException(f"주문 조회 실패: {response.text}")

        return response.json()

    async def get_orders(self, limit: int = 10, offset: int = 0) -> dict:
        """주문 목록 조회"""
        response = await self._request_with_retry(
            "GET",
            f"{self.base_url}/orders",
            params={"limit": limit, "offset": offset},
        )

        if response.status_code != 200:
            raise Cafe24APIException(f"주문 목록 조회 실패: {response.text}")

        return response.json()


# 싱글톤 인스턴스
cafe24_dao = Cafe24DAO()
