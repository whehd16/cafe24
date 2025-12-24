'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  getCart,
  getPaymentClientKey,
  confirmPayment,
  createOrder,
  Cart,
  ShippingAddress,
} from '@/lib/api';

/**
 * 결제 페이지
 *
 * 배송 정보 입력 → 토스페이먼츠 결제 → 주문 완료
 */
export default function CheckoutPage() {
  const router = useRouter();
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  // 배송 정보
  const [address, setAddress] = useState<ShippingAddress>({
    name: '',
    phone: '',
    zip_code: '',
    address1: '',
    address2: '',
  });

  // 장바구니 로드
  useEffect(() => {
    async function loadCart() {
      try {
        const data = await getCart();
        if (!data || data.items.length === 0) {
          router.push('/cart');
          return;
        }
        setCart(data);
      } catch (e) {
        console.error('장바구니 로드 실패:', e);
      } finally {
        setLoading(false);
      }
    }
    loadCart();
  }, [router]);

  // 결제 처리
  const handlePayment = async () => {
    if (!cart) return;

    // 배송 정보 검증
    if (!address.name || !address.phone || !address.zip_code || !address.address1) {
      alert('배송 정보를 모두 입력해주세요.');
      return;
    }

    setProcessing(true);

    try {
      // 1. 토스 Client Key 조회
      const clientKey = await getPaymentClientKey();

      // 2. 토스 결제 위젯 로드
      const { loadPaymentWidget } = await import('@tosspayments/payment-widget-sdk');
      const paymentWidget = await loadPaymentWidget(clientKey, 'ANONYMOUS');

      // 주문 ID 생성 (임시)
      const orderId = `ORDER_${Date.now()}`;
      const amount = Number(cart.total_price.amount);

      // 3. 결제 요청
      const paymentResult = await paymentWidget.requestPayment({
        orderId,
        orderName: cart.items.length > 1
          ? `${cart.items[0].title} 외 ${cart.items.length - 1}건`
          : cart.items[0].title,
        customerName: address.name,
        successUrl: `${window.location.origin}/checkout/success`,
        failUrl: `${window.location.origin}/checkout/fail`,
      });

      if (paymentResult?.paymentKey) {
        // 4. 결제 승인
        await confirmPayment(paymentResult.paymentKey, orderId, amount);

        // 5. 주문 생성
        const order = await createOrder(cart.id, address, paymentResult.paymentKey);

        // 6. 주문 완료 페이지로 이동
        router.push(`/orders/${order.id}`);
      }
    } catch (e: any) {
      console.error('결제 실패:', e);
      if (e.code !== 'USER_CANCEL') {
        alert('결제에 실패했습니다. 다시 시도해주세요.');
      }
    } finally {
      setProcessing(false);
    }
  };

  // 가격 포맷
  const formatPrice = (amount: string) => {
    return Number(amount).toLocaleString() + '원';
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <p>로딩 중...</p>
      </div>
    );
  }

  if (!cart) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">결제</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* 배송 정보 입력 */}
        <div className="card p-6">
          <h2 className="text-lg font-bold mb-4">배송 정보</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">수령인</label>
              <input
                type="text"
                value={address.name}
                onChange={(e) => setAddress({ ...address, name: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
                placeholder="홍길동"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">연락처</label>
              <input
                type="tel"
                value={address.phone}
                onChange={(e) => setAddress({ ...address, phone: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
                placeholder="010-1234-5678"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">우편번호</label>
              <input
                type="text"
                value={address.zip_code}
                onChange={(e) => setAddress({ ...address, zip_code: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
                placeholder="12345"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">주소</label>
              <input
                type="text"
                value={address.address1}
                onChange={(e) => setAddress({ ...address, address1: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
                placeholder="서울시 강남구 테헤란로 123"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">상세주소</label>
              <input
                type="text"
                value={address.address2}
                onChange={(e) => setAddress({ ...address, address2: e.target.value })}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
                placeholder="101동 101호"
              />
            </div>
          </div>
        </div>

        {/* 주문 요약 */}
        <div className="card p-6">
          <h2 className="text-lg font-bold mb-4">주문 요약</h2>

          <div className="space-y-4 mb-6">
            {cart.items.map((item) => (
              <div key={item.id} className="flex justify-between">
                <span className="text-gray-600">
                  {item.title} x {item.quantity}
                </span>
                <span>
                  {formatPrice(String(Number(item.price.amount) * item.quantity))}
                </span>
              </div>
            ))}
          </div>

          <div className="border-t border-gray-200 pt-4">
            <div className="flex justify-between items-center mb-6">
              <span className="text-lg font-bold">총 결제금액</span>
              <span className="text-2xl font-bold text-blue-600">
                {formatPrice(cart.total_price.amount)}
              </span>
            </div>

            <button
              onClick={handlePayment}
              disabled={processing}
              className="w-full btn btn-primary py-4 text-lg disabled:bg-gray-400"
            >
              {processing ? '결제 처리 중...' : '결제하기'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
