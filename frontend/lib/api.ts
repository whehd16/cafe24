/**
 * API 클라이언트
 *
 * 이 파일이 Backend와 통신하는 핵심 파일입니다.
 * 모든 API 호출은 여기서 합니다.
 */

// Backend API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * 기본 fetch 함수 (공통 옵션 적용)
 */
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // 쿠키 포함 (장바구니용)
    cache: 'no-store', // 캐시 비활성화 - 항상 최신 데이터
  });

  if (!response.ok) {
    throw new Error(`API 오류: ${response.status}`);
  }

  const data = await response.json();
  return data.data; // { success, message, data } 형식에서 data만 반환
}

// ========== 상품 API ==========

export interface Product {
  id: string;
  handle: string;
  title: string;
  description: string;
  price: {
    amount: string;
    currency_code: string;
  };
  compare_at_price?: {
    amount: string;
    currency_code: string;
  };
  featured_image?: {
    url: string;
    alt: string;
  };
  images: Array<{
    url: string;
    alt: string;
  }>;
  variants: Array<{
    id: string;
    title: string;
    price: {
      amount: string;
      currency_code: string;
    };
    available: boolean;
  }>;
  available: boolean;
  tags: string[];
}

export interface ProductListResponse {
  products: Product[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

/**
 * 상품 목록 조회
 *
 * @param page 페이지 번호 (1부터 시작)
 * @param limit 페이지당 상품 수
 * @param category 카테고리 번호 (선택)
 */
export async function getProducts(
  page: number = 1,
  limit: number = 12,
  category?: number
): Promise<ProductListResponse> {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
  });

  if (category) {
    params.append('category', String(category));
  }

  return fetchAPI<ProductListResponse>(`/products?${params}`);
}

/**
 * 상품 상세 조회
 *
 * @param productId 상품 ID
 */
export async function getProduct(productId: string): Promise<Product> {
  return fetchAPI<Product>(`/products/${productId}`);
}

/**
 * 카테고리 목록 조회
 */
export async function getCategories() {
  return fetchAPI<Array<{
    id: string;
    name: string;
    parent_id?: string;
    path: string;
  }>>('/products/categories');
}

// ========== 장바구니 API ==========

export interface CartItem {
  id: string;
  product_id: string;
  variant_id?: string;
  title: string;
  quantity: number;
  price: {
    amount: string;
    currency_code: string;
  };
  image?: {
    url: string;
    alt: string;
  };
}

export interface Cart {
  id: string;
  items: CartItem[];
  total_quantity: number;
  total_price: {
    amount: string;
    currency_code: string;
  };
}

/**
 * 장바구니 조회
 */
export async function getCart(): Promise<Cart> {
  return fetchAPI<Cart>('/cart');
}

/**
 * 장바구니에 상품 추가
 *
 * @param productId 상품 ID
 * @param quantity 수량
 * @param variantId 옵션 ID (선택)
 */
export async function addToCart(
  productId: string,
  quantity: number = 1,
  variantId?: string
): Promise<Cart> {
  return fetchAPI<Cart>('/cart/items', {
    method: 'POST',
    body: JSON.stringify({
      product_id: productId,
      quantity,
      variant_id: variantId,
    }),
  });
}

/**
 * 장바구니 아이템 수량 변경
 *
 * @param itemId 장바구니 아이템 ID
 * @param quantity 새 수량
 */
export async function updateCartItem(
  itemId: string,
  quantity: number
): Promise<Cart> {
  return fetchAPI<Cart>(`/cart/items/${itemId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
}

/**
 * 장바구니에서 상품 삭제
 *
 * @param itemId 장바구니 아이템 ID
 */
export async function removeFromCart(itemId: string): Promise<Cart> {
  return fetchAPI<Cart>(`/cart/items/${itemId}`, {
    method: 'DELETE',
  });
}

// ========== 결제 API ==========

/**
 * 토스 Client Key 조회
 */
export async function getPaymentClientKey(): Promise<string> {
  const data = await fetchAPI<{ client_key: string }>('/payments/client-key');
  return data.client_key;
}

/**
 * 결제 승인
 *
 * @param paymentKey 토스에서 받은 결제 키
 * @param orderId 주문 ID
 * @param amount 결제 금액
 */
export async function confirmPayment(
  paymentKey: string,
  orderId: string,
  amount: number
) {
  return fetchAPI('/payments/confirm', {
    method: 'POST',
    body: JSON.stringify({
      payment_key: paymentKey,
      order_id: orderId,
      amount,
    }),
  });
}

// ========== 주문 API ==========

export interface ShippingAddress {
  name: string;
  phone: string;
  zip_code: string;
  address1: string;
  address2: string;
}

export interface Order {
  id: string;
  cafe24_order_id?: string;
  status: string;
  items: Array<{
    id: string;
    product_id: string;
    title: string;
    quantity: number;
    price: {
      amount: string;
      currency_code: string;
    };
  }>;
  shipping_address?: ShippingAddress;
  total_price: {
    amount: string;
    currency_code: string;
  };
  created_at: string;
}

/**
 * 주문 생성
 *
 * @param cartId 장바구니 ID
 * @param shippingAddress 배송 주소
 * @param paymentKey 결제 키
 */
export async function createOrder(
  cartId: string,
  shippingAddress: ShippingAddress,
  paymentKey: string
): Promise<Order> {
  return fetchAPI<Order>(`/orders?payment_key=${paymentKey}`, {
    method: 'POST',
    body: JSON.stringify({
      cart_id: cartId,
      shipping_address: shippingAddress,
    }),
  });
}

/**
 * 주문 목록 조회
 */
export async function getOrders(page: number = 1, limit: number = 10) {
  return fetchAPI<Order[]>(`/orders?page=${page}&limit=${limit}`);
}

/**
 * 주문 상세 조회
 */
export async function getOrder(orderId: string): Promise<Order> {
  return fetchAPI<Order>(`/orders/${orderId}`);
}

// ========== 인증 API ==========

/**
 * 카페24 로그인 URL 조회
 */
export async function getLoginUrl(): Promise<string> {
  const data = await fetchAPI<{ url: string }>('/auth/login-url');
  return data.url;
}
