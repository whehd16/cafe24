'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { useParams, useRouter } from 'next/navigation';
import { getProduct, addToCart, Product } from '@/lib/api';

/**
 * 상품 상세 페이지
 *
 * 상품 정보를 보여주고 장바구니에 담을 수 있습니다.
 */
export default function ProductPage() {
  const params = useParams();
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [selectedVariant, setSelectedVariant] = useState('');
  const [adding, setAdding] = useState(false);

  // 상품 정보 로드
  useEffect(() => {
    async function loadProduct() {
      try {
        const data = await getProduct(params.id as string);
        setProduct(data);
        if (data.variants.length > 0) {
          setSelectedVariant(data.variants[0].id);
        }
      } catch (e) {
        setError('상품을 찾을 수 없습니다.');
      } finally {
        setLoading(false);
      }
    }
    loadProduct();
  }, [params.id]);

  // 장바구니에 추가
  const handleAddToCart = async () => {
    if (!product) return;

    setAdding(true);
    try {
      await addToCart(product.id, quantity, selectedVariant || undefined);
      alert('장바구니에 추가되었습니다.');
      router.refresh(); // 헤더의 장바구니 수량 갱신
    } catch (e) {
      alert('장바구니 추가에 실패했습니다.');
    } finally {
      setAdding(false);
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

  if (error || !product) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500">{error || '상품을 찾을 수 없습니다.'}</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
        {/* 상품 이미지 */}
        <div className="aspect-square relative bg-gray-100 rounded-lg overflow-hidden">
          {product.featured_image ? (
            <Image
              src={product.featured_image.url}
              alt={product.featured_image.alt || product.title}
              fill
              className="object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">
              이미지 없음
            </div>
          )}
        </div>

        {/* 상품 정보 */}
        <div>
          <h1 className="text-3xl font-bold mb-4">{product.title}</h1>

          {/* 가격 */}
          <div className="mb-6">
            {product.compare_at_price && (
              <span className="text-gray-400 line-through text-lg mr-2">
                {formatPrice(product.compare_at_price.amount)}
              </span>
            )}
            <span className="text-2xl font-bold">
              {formatPrice(product.price.amount)}
            </span>
          </div>

          {/* 옵션 선택 */}
          {product.variants.length > 1 && (
            <div className="mb-6">
              <label className="block text-sm font-medium mb-2">옵션</label>
              <select
                value={selectedVariant}
                onChange={(e) => setSelectedVariant(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2"
              >
                {product.variants.map((variant) => (
                  <option
                    key={variant.id}
                    value={variant.id}
                    disabled={!variant.available}
                  >
                    {variant.title}
                    {!variant.available && ' (품절)'}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* 수량 */}
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">수량</label>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="w-10 h-10 border border-gray-300 rounded-lg"
              >
                -
              </button>
              <span className="text-lg font-medium">{quantity}</span>
              <button
                onClick={() => setQuantity(quantity + 1)}
                className="w-10 h-10 border border-gray-300 rounded-lg"
              >
                +
              </button>
            </div>
          </div>

          {/* 장바구니 버튼 */}
          <button
            onClick={handleAddToCart}
            disabled={adding || !product.available}
            className="w-full btn btn-primary py-4 text-lg disabled:bg-gray-400"
          >
            {adding ? '추가 중...' : product.available ? '장바구니에 담기' : '품절'}
          </button>

          {/* 상품 설명 */}
          {product.description && (
            <div className="mt-8 pt-8 border-t border-gray-200">
              <h2 className="text-lg font-bold mb-4">상품 설명</h2>
              <p className="text-gray-600 whitespace-pre-wrap">
                {product.description}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
