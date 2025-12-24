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

## 프로젝트 구조

```
cafe24/
├── frontend/                    # Next.js 프론트엔드
│   ├── app/                    # 페이지 (App Router)
│   │   ├── page.tsx           # 메인 페이지 (물감 애니메이션)
│   │   ├── product/           # 상품 목록/상세
│   │   ├── cart/              # 장바구니
│   │   ├── checkout/          # 결제
│   │   ├── orders/            # 주문 내역
│   │   ├── layout.tsx         # 루트 레이아웃
│   │   └── globals.css        # 전역 스타일
│   │
│   ├── components/            # UI 컴포넌트
│   │   ├── layout/
│   │   │   └── Header.tsx     # 헤더 (햄버거 메뉴, 로고, 아이콘)
│   │   ├── product/
│   │   │   └── ProductCard.tsx
│   │   └── ThemeProvider.tsx  # 다크모드 Provider
│   │
│   ├── lib/
│   │   └── api.ts             # Backend API 클라이언트 (핵심!)
│   │
│   └── public/
│       └── paint-stroke.png   # 메인 페이지 물감 이미지
│
├── backend/                    # FastAPI 백엔드 (MVC)
│   ├── app/
│   │   ├── main.py            # FastAPI 앱 엔트리포인트
│   │   ├── controllers/       # API 엔드포인트
│   │   │   ├── product_controller.py
│   │   │   ├── cart_controller.py
│   │   │   ├── order_controller.py
│   │   │   ├── payment_controller.py
│   │   │   └── auth_controller.py
│   │   ├── services/          # 비즈니스 로직
│   │   ├── daos/              # 외부 API 호출
│   │   │   ├── cafe24_dao.py  # 카페24 API
│   │   │   └── toss_dao.py    # 토스페이먼츠 API
│   │   ├── models/            # 데이터 모델
│   │   └── commons/           # 공통 유틸
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── .gitignore
└── README.md
```

## 시작하기

### 1. 사전 준비

- Node.js 18+ 설치
- Python 3.11+ 설치
- 카페24 개발자 앱 등록 (https://developers.cafe24.com)
- 토스페이먼츠 가입 (https://developers.tosspayments.com)

### 2. Backend 설정

```bash
cd backend

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열고 카페24/토스 키 입력

# 서버 실행
uvicorn app.main:app --reload
```

서버 실행 후 http://localhost:8000/docs 에서 API 문서를 확인할 수 있습니다.

### 3. Frontend 설정

```bash
cd frontend

# 패키지 설치
npm install

# 환경변수 설정
cp .env.example .env.local
# .env.local 파일에 아래 내용 입력:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api

# 개발 서버 실행
npm run dev
```

http://localhost:3000 에서 쇼핑몰을 확인할 수 있습니다.

### 4. 카페24 OAuth 인증

1. http://localhost:8000/api/auth/login 접속
2. 카페24 로그인 완료
3. 토큰 발급 확인
4. 이제 상품 조회 등 API 사용 가능

## 환경 변수

### Backend (.env)

```env
# 카페24
CAFE24_CLIENT_ID=your_client_id
CAFE24_CLIENT_SECRET=your_client_secret
CAFE24_MALL_ID=your_mall_id
CAFE24_REDIRECT_URI=http://localhost:8000/api/auth/callback

# 토스페이먼츠
TOSS_SECRET_KEY=your_toss_secret_key
TOSS_CLIENT_KEY=your_toss_client_key
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

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
| `/` | 메인 페이지 (물감 애니메이션) |
| `/product` | 상품 목록 (카테고리 필터) |
| `/product/[id]` | 상품 상세 |
| `/cart` | 장바구니 |
| `/checkout` | 결제 |
| `/orders` | 주문 내역 |
| `/login` | 로그인 |
| `/mypage` | 마이페이지 |
| `/about` | About us |

## UI/UX 기능

### 헤더 구성
- **좌측**: 햄버거 메뉴 (Home/Shop/About us) + 다크모드 토글
- **중앙**: Pistachio Love 로고 (Pacifico 폰트, #84B067 색상)
- **우측**: 로그인, 마이페이지, 장바구니 아이콘

### 메인 페이지
- 흰 배경 (다크모드: 어두운 배경)
- 물감 브러시 이미지가 왼쪽에서 오른쪽으로 칠해지는 애니메이션

### 상품 목록 페이지
- 상단 카테고리 메뉴: HIT / SALES / BAGS / POUCHES / CLOTHES / ETC
- 서브카테고리 드롭다운 지원
- 그리드 형태의 상품 카드

### 다크모드
- localStorage에 테마 설정 저장
- 시스템 설정 자동 감지
- 부드러운 전환 애니메이션

## 코드 흐름

```
[사용자] → [Next.js Frontend]
              ↓ API 호출 (lib/api.ts)
         [FastAPI Backend]
              ↓
    [Controller] → 요청 받음
              ↓
    [Service] → 로직 처리
              ↓
    [DAO] → 카페24/토스 API 호출
              ↓
         응답 반환
```

## 개발 팁

### Frontend 수정 시

- API 연동: `lib/api.ts` 수정
- UI 수정: `components/` 폴더 참고
- 스타일: `globals.css` 또는 Tailwind 클래스 사용
- 다크모드: `dark:` prefix 클래스 추가

### Backend 수정 시

MVC 패턴을 따릅니다:
1. **Controller** - 새 API 엔드포인트 추가
2. **Service** - 비즈니스 로직 구현
3. **DAO** - 외부 API 호출

### 디버깅

- Backend: http://localhost:8000/docs (Swagger UI)
- Frontend: 브라우저 개발자 도구

## 참고 문서

- [카페24 API 문서](https://developers.cafe24.com/docs/api/)
- [토스페이먼츠 문서](https://docs.tosspayments.com/)
- [Next.js 문서](https://nextjs.org/docs)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)

## 라이선스

MIT License
