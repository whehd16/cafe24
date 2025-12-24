"""
FastAPI 앱 시작점

이 파일이 서버의 진입점입니다.
uvicorn app.main:app --reload 로 실행합니다.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.commons.config import get_settings
from app.controllers import (
    auth_router,
    product_router,
    cart_router,
    order_router,
    payment_router,
)

# 설정 로드
settings = get_settings()

# FastAPI 앱 생성
app = FastAPI(
    title="카페24 쇼핑몰 API",
    description="""
    카페24와 연동된 쇼핑몰 백엔드 API입니다.

    ## 기능

    * **인증** - 카페24 OAuth 로그인
    * **상품** - 상품 목록/상세 조회
    * **장바구니** - 상품 담기/수정/삭제
    * **결제** - 토스페이먼츠 결제
    * **주문** - 주문 생성/조회

    ## 인증 흐름

    1. `/api/auth/login` 호출 → 카페24 로그인 페이지로 이동
    2. 로그인 완료 → `/api/auth/callback` 으로 리다이렉트
    3. Access Token 발급 완료
    4. 이후 API 호출 가능

    ## 결제 흐름

    1. 장바구니에 상품 담기
    2. `/api/payments/client-key` 로 토스 키 조회
    3. 프론트엔드에서 토스 결제 위젯으로 결제
    4. 결제 완료 후 `/api/payments/confirm` 호출
    5. `/api/orders` 로 주문 생성
    """,
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router, prefix="/api")
app.include_router(product_router, prefix="/api")
app.include_router(cart_router, prefix="/api")
app.include_router(order_router, prefix="/api")
app.include_router(payment_router, prefix="/api")


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "status": "ok",
        "message": "카페24 쇼핑몰 API가 실행 중입니다.",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 (상세)"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "debug": settings.debug,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
