import Link from 'next/link';
import Image from 'next/image';
import { Product } from '@/lib/api';

/**
 * 상품 카드 컴포넌트
 *
 * 상품 목록에서 각 상품을 보여주는 카드입니다.
 */
interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  // 가격 포맷 (원화)
  const formatPrice = (amount: string) => {
    return Number(amount).toLocaleString() + '원';
  };

  return (
    <Link href={`/product/${product.id}`} className="group">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        {/* 상품 이미지 */}
        <div className="aspect-square relative bg-gray-100 dark:bg-gray-700">
          {product.featured_image ? (
            <Image
              src={product.featured_image.url}
              alt={product.featured_image.alt || product.title}
              fill
              className="object-cover group-hover:scale-105 transition-transform"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400 dark:text-gray-500">
              이미지 없음
            </div>
          )}

          {/* 품절 표시 */}
          {!product.available && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <span className="text-white font-bold">SOLD OUT</span>
            </div>
          )}
        </div>

        {/* 상품 정보 */}
        <div className="p-4">
          <h3 className="font-medium text-gray-900 dark:text-gray-100 group-hover:text-black dark:group-hover:text-white truncate">
            {product.title}
          </h3>

          <div className="mt-2 flex items-center gap-2">
            {/* 할인가 */}
            {product.compare_at_price && (
              <span className="text-gray-400 dark:text-gray-500 line-through text-sm">
                {formatPrice(product.compare_at_price.amount)}
              </span>
            )}
            {/* 판매가 */}
            <span className="font-bold text-lg text-gray-900 dark:text-gray-100">
              {formatPrice(product.price.amount)}
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
}
