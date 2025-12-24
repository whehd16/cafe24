"""
인증 컨트롤러

카페24 OAuth 인증 관련 API 엔드포인트
"""
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from app.services.auth_service import auth_service
from app.commons.response import success_response

router = APIRouter(prefix="/auth", tags=["인증"])


@router.get("/login")
async def login():
    """
    카페24 로그인

    이 API를 호출하면 카페24 로그인 페이지로 리다이렉트됩니다.

    **사용 방법:**
    1. 프론트엔드에서 이 URL로 이동
    2. 카페24에서 로그인
    3. /auth/callback으로 리다이렉트됨
    """
    login_url = auth_service.get_login_url()
    return RedirectResponse(url=login_url)


@router.get("/login-url")
async def get_login_url():
    """
    로그인 URL 조회

    리다이렉트 대신 URL만 반환합니다.
    프론트엔드에서 직접 이동할 때 사용합니다.
    """
    login_url = auth_service.get_login_url()
    return success_response(data={"url": login_url})


@router.get("/callback")
async def oauth_callback(
    code: str = Query(..., description="카페24에서 전달한 인증 코드"),
    state: str = Query("", description="상태 값 (선택)"),
):
    """
    OAuth 콜백

    카페24에서 로그인 완료 후 리다이렉트되는 엔드포인트입니다.
    인증 코드를 받아서 Access Token을 발급받습니다.

    **주의:** 이 API는 카페24가 직접 호출합니다.
    """
    token_data = await auth_service.handle_callback(code)

    # 토큰을 DAO에 설정
    auth_service.set_tokens(
        token_data["access_token"],
        token_data["refresh_token"],
    )

    return success_response(
        data=token_data,
        message="로그인 성공",
    )


@router.post("/refresh")
async def refresh_token():
    """
    토큰 갱신

    Access Token이 만료되면 이 API를 호출해서 갱신합니다.

    **주의:** 먼저 /auth/callback으로 토큰을 발급받아야 합니다.
    """
    token_data = await auth_service.refresh_token()
    return success_response(
        data=token_data,
        message="토큰 갱신 성공",
    )


@router.post("/set-tokens")
async def set_tokens(
    access_token: str,
    refresh_token: str,
):
    """
    토큰 수동 설정

    이미 발급받은 토큰을 수동으로 설정합니다.
    테스트용으로 사용합니다.
    """
    auth_service.set_tokens(access_token, refresh_token)
    return success_response(message="토큰 설정 완료")
