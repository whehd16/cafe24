'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { getOrder, Order } from '@/lib/api';

/**
 * 주문 상세 페이지
 */
export default function OrderDetailPage() {
  const params = useParams();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadOrder() {
      try {
        const data = await getOrder(params.id as string);
        setOrder(data);
      } catch (e) {
        console.error('주문 로드 실패:', e);
      } finally {
        setLoading(false);
      }
    }
    loadOrder();
  }, [params.id]);

  // 가격 포맷
  const formatPrice = (amount: string) => {
    return Number(amount).toLocaleString() + '원';
  };

  // 상태 한글 변환
  const getStatusText = (status: string) => {
    const statusMap: { [key: string]: string } = {
      pending: '결제 대기',
      paid: '결제 완료',
      shipped: '배송 중',
      delivered: '배송 완료',
      cancelled: '취소됨',
    };
    return statusMap[status] || status;
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <p>로딩 중...</p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">주문을 찾을 수 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* 주문 완료 메시지 */}
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg
            className="w-8 h-8 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>
        <h1 className="text-2xl font-bold mb-2">주문이 완료되었습니다</h1>
        <p className="text-gray-600">
          주문번호: {order.id}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* 주문 상품 */}
        <div className="card p-6">
          <h2 className="text-lg font-bold mb-4">주문 상품</h2>

          <div className="space-y-4">
            {order.items.map((item) => (
              <div key={item.id} className="flex justify-between">
                <div>
                  <p className="font-medium">{item.title}</p>
                  <p className="text-sm text-gray-500">수량: {item.quantity}</p>
                </div>
                <p className="font-bold">
                  {formatPrice(String(Number(item.price.amount) * item.quantity))}
                </p>
              </div>
            ))}
          </div>

          <div className="border-t border-gray-200 mt-4 pt-4">
            <div className="flex justify-between items-center">
              <span className="font-bold">총 결제금액</span>
              <span className="text-xl font-bold text-blue-600">
                {formatPrice(order.total_price.amount)}
              </span>
            </div>
          </div>
        </div>

        {/* 배송 정보 */}
        <div className="card p-6">
          <h2 className="text-lg font-bold mb-4">배송 정보</h2>

          {order.shipping_address ? (
            <div className="space-y-2 text-gray-600">
              <p>
                <span className="font-medium text-gray-900">수령인:</span>{' '}
                {order.shipping_address.name}
              </p>
              <p>
                <span className="font-medium text-gray-900">연락처:</span>{' '}
                {order.shipping_address.phone}
              </p>
              <p>
                <span className="font-medium text-gray-900">주소:</span>{' '}
                ({order.shipping_address.zip_code}){' '}
                {order.shipping_address.address1}{' '}
                {order.shipping_address.address2}
              </p>
            </div>
          ) : (
            <p className="text-gray-500">배송 정보가 없습니다.</p>
          )}

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p>
              <span className="font-medium">주문 상태:</span>{' '}
              <span className="text-blue-600 font-bold">
                {getStatusText(order.status)}
              </span>
            </p>
            <p className="text-sm text-gray-500 mt-1">
              주문일: {new Date(order.created_at).toLocaleString('ko-KR')}
            </p>
          </div>
        </div>
      </div>

      {/* 버튼 */}
      <div className="mt-8 flex justify-center gap-4">
        <Link href="/orders" className="btn btn-secondary">
          주문 내역
        </Link>
        <Link href="/" className="btn btn-primary">
          쇼핑 계속하기
        </Link>
      </div>
    </div>
  );
}
