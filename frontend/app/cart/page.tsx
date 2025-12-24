'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { getCart, updateCartItem, removeFromCart, Cart } from '@/lib/api';

/**
 * 장바구니 페이지
 */
export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);

  // 장바구니 로드
  useEffect(() => {
    async function loadCart() {
      try {
        const data = await getCart();
        setCart(data);
      } catch (e) {
        console.error('장바구니 로드 실패:', e);
      } finally {
        setLoading(false);
      }
    }
    loadCart();
  }, []);

  // 수량 변경
  const handleUpdateQuantity = async (itemId: string, quantity: number) => {
    try {
      const updatedCart = await updateCartItem(itemId, quantity);
      setCart(updatedCart);
    } catch (e) {
      alert('수량 변경에 실패했습니다.');
    }
  };

  // 상품 삭제
  const handleRemove = async (itemId: string) => {
    try {
      const updatedCart = await removeFromCart(itemId);
      setCart(updatedCart);
    } catch (e) {
      alert('삭제에 실패했습니다.');
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

  if (!cart || cart.items.length === 0) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold mb-4">장바구니</h1>
        <p className="text-gray-500 mb-8">장바구니가 비어있습니다.</p>
        <Link href="/" className="btn btn-primary">
          쇼핑하러 가기
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-8">장바구니</h1>

      {/* 장바구니 아이템 목록 */}
      <div className="space-y-4 mb-8">
        {cart.items.map((item) => (
          <div
            key={item.id}
            className="card p-4 flex items-center gap-4"
          >
            {/* 상품 이미지 */}
            <div className="w-24 h-24 relative bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
              {item.image ? (
                <Image
                  src={item.image.url}
                  alt={item.image.alt || item.title}
                  fill
                  className="object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400 text-xs">
                  이미지 없음
                </div>
              )}
            </div>

            {/* 상품 정보 */}
            <div className="flex-1">
              <Link
                href={`/product/${item.product_id}`}
                className="font-medium hover:underline"
              >
                {item.title}
              </Link>
              <p className="text-gray-600">
                {formatPrice(item.price.amount)}
              </p>
            </div>

            {/* 수량 조절 */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                className="w-8 h-8 border border-gray-300 rounded"
                disabled={item.quantity <= 1}
              >
                -
              </button>
              <span className="w-8 text-center">{item.quantity}</span>
              <button
                onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                className="w-8 h-8 border border-gray-300 rounded"
              >
                +
              </button>
            </div>

            {/* 소계 */}
            <div className="w-24 text-right font-bold">
              {formatPrice(String(Number(item.price.amount) * item.quantity))}
            </div>

            {/* 삭제 버튼 */}
            <button
              onClick={() => handleRemove(item.id)}
              className="text-gray-400 hover:text-red-500"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ))}
      </div>

      {/* 합계 및 결제 버튼 */}
      <div className="card p-6">
        <div className="flex justify-between items-center mb-6">
          <span className="text-lg">총 {cart.total_quantity}개 상품</span>
          <span className="text-2xl font-bold">
            {formatPrice(cart.total_price.amount)}
          </span>
        </div>

        <Link
          href="/checkout"
          className="block w-full btn btn-primary py-4 text-lg text-center"
        >
          결제하기
        </Link>
      </div>
    </div>
  );
}
