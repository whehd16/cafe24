# Pistachio Love - 카페24 연동 쇼핑몰

카페24 API와 토스페이먼츠를 연동한 피스타치오 디저트 쇼핑몰 프로젝트입니다.

## 기술 스택

- **Frontend**: Next.js 14 (App Router) + React + TypeScript + Tailwind CSS
- **Backend**: FastAPI (Python) - MVC 구조
- **결제**: 토스페이먼츠
- **데이터**: 카페24 Admin API

## 주요 기능

- 다크모드 / 라이트모드 지원
- 카테고리별 상품 필터링 (HIT, SALES, BAGS, POUCHES, CLOTHES, ETC)
- 장바구니 기능
- 토스페이먼츠 결제 연동
- 카페24 OAuth 인증
- 3D Tilted Card 이미지 슬라이더 (메인 페이지)

## 로컬 실행 (Quick Start)

### 1. 저장소 클론

```bash
git clone <repository-url>
cd cafe24
```

### 2. Backend 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
```

`.env` 파일을 열어 아래 값들을 입력:

```env
# 카페24 설정 (https://developers.cafe24.com에서 앱 등록 후 발급)
CAFE24_CLIENT_ID=발급받은_클라이언트ID
CAFE24_CLIENT_SECRET=발급받은_시크릿
CAFE24_MALL_ID=내_쇼핑몰_ID
CAFE24_REDIRECT_URI=http://localhost:3000/auth/callback

# 토스페이먼츠 설정 (https://developers.tosspayments.com에서 발급)
TOSS_CLIENT_KEY=test_ck_xxx
TOSS_SECRET_KEY=test_sk_xxx

# 서버 설정
FRONTEND_URL=http://localhost:3000
DEBUG=true
SECRET_KEY=your-secret-key-change-this
```

서버 실행:

```bash
uvicorn app.main:app --reload --port 8000
```

API 문서: http://localhost:8000/docs

### 3. Frontend 실행

새 터미널을 열고:

```bash
cd frontend

# 패키지 설치
npm install

# 환경변수 설정
cp .env.example .env.local
```

`.env.local` 파일 확인:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_TOSS_CLIENT_KEY=test_ck_xxx
```

개발 서버 실행:

```bash
npm run dev
```

쇼핑몰: http://localhost:3000

### 4. 카페24 OAuth 인증 (최초 1회)

1. http://localhost:8000/api/auth/login 접속
2. 카페24 로그인 완료
3. 토큰이 `backend/token.json`에 자동 저장됨
4. 이제 상품 조회 등 API 사용 가능

## 프로젝트 구조

```
cafe24/
├── frontend/                    # Next.js 프론트엔드
│   ├── app/                    # 페이지 (App Router)
│   │   ├── page.tsx           # 메인 페이지 (이미지 슬라이더)
│   │   ├── product/           # 상품 목록/상세
│   │   ├── cart/              # 장바구니
│   │   ├── checkout/          # 결제
│   │   ├── orders/            # 주문 내역
│   │   └── globals.css        # 전역 스타일
│   │
│   ├── components/            # UI 컴포넌트
│   │   ├── layout/
│   │   │   └── Header.tsx     # 헤더
│   │   ├── home/
│   │   │   └── ImageSlider.tsx # 메인 이미지 슬라이더
│   │   ├── product/
│   │   │   └── ProductCard.tsx
│   │   ├── ui/
│   │   │   └── TiltedCard.tsx # 3D 틸트 카드 효과
│   │   └── ThemeProvider.tsx  # 다크모드 Provider
│   │
│   ├── lib/
│   │   └── api.ts             # Backend API 클라이언트
│   │
│   └── public/
│       └── slides/            # 메인 슬라이더 이미지들
│
├── backend/                    # FastAPI 백엔드 (MVC)
│   ├── app/
│   │   ├── main.py            # FastAPI 앱 엔트리포인트
│   │   ├── controllers/       # API 엔드포인트
│   │   ├── services/          # 비즈니스 로직
│   │   ├── daos/              # 외부 API 호출
│   │   ├── models/            # 데이터 모델
│   │   └── commons/           # 공통 유틸
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── token.json             # 카페24 OAuth 토큰 (자동 생성)
│
└── README.md
```

## 환경 변수

### Backend (.env)

| 변수명 | 설명 |
|--------|------|
| CAFE24_CLIENT_ID | 카페24 앱 클라이언트 ID |
| CAFE24_CLIENT_SECRET | 카페24 앱 시크릿 |
| CAFE24_MALL_ID | 카페24 쇼핑몰 ID |
| CAFE24_REDIRECT_URI | OAuth 콜백 URL |
| TOSS_CLIENT_KEY | 토스 클라이언트 키 |
| TOSS_SECRET_KEY | 토스 시크릿 키 |
| FRONTEND_URL | 프론트엔드 URL |

### Frontend (.env.local)

| 변수명 | 설명 |
|--------|------|
| NEXT_PUBLIC_API_URL | 백엔드 API URL |
| NEXT_PUBLIC_TOSS_CLIENT_KEY | 토스 클라이언트 키 |

## API 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/products` | 상품 목록 |
| GET | `/api/products/{id}` | 상품 상세 |
| GET | `/api/products/categories` | 카테고리 목록 |
| GET | `/api/cart` | 장바구니 조회 |
| POST | `/api/cart/items` | 장바구니 추가 |
| PUT | `/api/cart/items/{id}` | 장바구니 수량 변경 |
| DELETE | `/api/cart/items/{id}` | 장바구니 삭제 |
| POST | `/api/payments/confirm` | 결제 승인 |
| POST | `/api/orders` | 주문 생성 |
| GET | `/api/orders` | 주문 목록 |
| GET | `/api/auth/login` | 카페24 로그인 |

## 페이지 구조

| 경로 | 설명 |
|------|------|
| `/` | 메인 페이지 (이미지 슬라이더) |
| `/product` | 상품 목록 (카테고리 필터) |
| `/product/[id]` | 상품 상세 |
| `/cart` | 장바구니 |
| `/checkout` | 결제 |
| `/orders` | 주문 내역 |
| `/login` | 로그인 |
| `/mypage` | 마이페이지 |
| `/about` | About us |

## UI/UX 기능

### 메인 페이지
- 옅은 초록색 배경 (#f0f7eb)
- 반응형 이미지 슬라이더 (모바일: 1개, 태블릿: 2개, 데스크탑: 3개)
- 3D Tilted Card 효과 (마우스 호버 시)
- 데스크탑에서 양쪽 이미지 180도 회전

### 헤더
- **좌측**: 햄버거 메뉴 + 다크모드 토글
- **중앙**: Pistachio Love 로고
- **우측**: 로그인, 마이페이지, 장바구니 아이콘

### 다크모드
- localStorage에 테마 설정 저장
- 시스템 설정 자동 감지

## 문제 해결

### 카페24 토큰 만료 시

```bash
rm backend/token.json
# http://localhost:8000/api/auth/login 접속하여 재인증
```

### CORS 에러 발생 시

Backend `.env`에서 `FRONTEND_URL` 확인:
```env
FRONTEND_URL=http://localhost:3000
```

### 상품이 안 보일 때

1. 카페24 OAuth 인증 완료 확인
2. `backend/token.json` 파일 존재 확인
3. Backend 로그 확인

## 참고 문서

- [카페24 API 문서](https://developers.cafe24.com/docs/api/)
- [토스페이먼츠 문서](https://docs.tosspayments.com/)
- [Next.js 문서](https://nextjs.org/docs)
- [FastAPI 문서](https://fastapi.tiangolo.com/)

## 라이선스

MIT License
