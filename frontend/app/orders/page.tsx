'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getOrders, Order } from '@/lib/api';

/**
 * 주문 내역 페이지
 */
export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadOrders() {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (e) {
        console.error('주문 목록 로드 실패:', e);
      } finally {
        setLoading(false);
      }
    }
    loadOrders();
  }, []);

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

  // 상태 색상
  const getStatusColor = (status: string) => {
    const colorMap: { [key: string]: string } = {
      pending: 'text-yellow-600 bg-yellow-100',
      paid: 'text-blue-600 bg-blue-100',
      shipped: 'text-purple-600 bg-purple-100',
      delivered: 'text-green-600 bg-green-100',
      cancelled: 'text-red-600 bg-red-100',
    };
    return colorMap[status] || 'text-gray-600 bg-gray-100';
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <p>로딩 중...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">주문 내역</h1>

      {orders.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-8">주문 내역이 없습니다.</p>
          <Link href="/" className="btn btn-primary">
            쇼핑하러 가기
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <Link
              key={order.id}
              href={`/orders/${order.id}`}
              className="card p-6 block hover:shadow-md transition-shadow"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="text-sm text-gray-500">
                    주문번호: {order.id.slice(0, 8)}...
                  </p>
                  <p className="text-sm text-gray-500">
                    {new Date(order.created_at).toLocaleDateString('ko-KR')}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(
                    order.status
                  )}`}
                >
                  {getStatusText(order.status)}
                </span>
              </div>

              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">
                    {order.items[0]?.title}
                    {order.items.length > 1 && ` 외 ${order.items.length - 1}건`}
                  </p>
                </div>
                <p className="text-lg font-bold">
                  {formatPrice(order.total_price.amount)}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
