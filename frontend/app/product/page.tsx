'use client';

import { useEffect, useState } from 'react';
import { getProducts, Product } from '@/lib/api';
import ProductCard from '@/components/product/ProductCard';

// 카테고리 메뉴 구조 (Cafe24 카테고리 ID와 매핑)
const categoryMenu = [
  {
    id: 'bags',
    label: 'BAGS',
    cafe24Id: 24,
    subcategories: [
      { label: 'ALL', cafe24Id: 24 },
      { label: 'ECO', cafe24Id: 29 },
    ],
  },
  {
    id: 'pouches',
    label: 'POUCHES',
    cafe24Id: 25,
    subcategories: [
      { label: 'ALL', cafe24Id: 25 },
      { label: 'POCKETS', cafe24Id: 32 },
    ],
  },
];

/**
 * 상품 목록 페이지
 */
export default function ProductListPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedSubcategory, setSelectedSubcategory] = useState<string | null>(null);
  const [hoveredCategory, setHoveredCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 현재 선택된 Cafe24 카테고리 ID 계산
  const getCafe24CategoryId = (): number | undefined => {
    if (!selectedCategory) return undefined;

    const category = categoryMenu.find((c) => c.id === selectedCategory);
    if (!category) return undefined;

    if (selectedSubcategory) {
      const sub = category.subcategories?.find((s) => s.label === selectedSubcategory);
      return sub?.cafe24Id;
    }

    return category.cafe24Id;
  };

  // 상품 로드
  useEffect(() => {
    async function loadProducts() {
      setLoading(true);
      try {
        const cafe24CategoryId = getCafe24CategoryId();
        const data = await getProducts(1, 24, cafe24CategoryId);
        setProducts(data.products);
        setError(null);
      } catch (e) {
        setError('상품을 불러올 수 없습니다.');
        console.error('상품 조회 실패:', e);
      } finally {
        setLoading(false);
      }
    }
    loadProducts();
  }, [selectedCategory, selectedSubcategory]);

  const handleCategoryClick = (categoryId: string) => {
    if (selectedCategory === categoryId) {
      setSelectedCategory(null);
      setSelectedSubcategory(null);
    } else {
      setSelectedCategory(categoryId);
      setSelectedSubcategory(null);
    }
  };

  const handleSubcategoryClick = (subcategoryLabel: string) => {
    setSelectedSubcategory(subcategoryLabel);
  };

  return (
    <div className="pt-20 px-6 min-h-screen bg-white dark:bg-gray-900">
      {/* 카테고리 메뉴 */}
      <nav className="mb-8">
        {/* 메인 카테고리 */}
        <div className="flex items-center justify-center gap-8 text-sm tracking-wide">
          {/* ALL 버튼 */}
          <button
            onClick={() => {
              setSelectedCategory(null);
              setSelectedSubcategory(null);
            }}
            className={`py-2 transition-colors ${
              selectedCategory === null
                ? 'text-[#84B067] font-medium'
                : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
            }`}
          >
            ALL
          </button>

          {categoryMenu.map((category) => (
            <div
              key={category.id}
              className="relative"
              onMouseEnter={() => setHoveredCategory(category.id)}
              onMouseLeave={() => setHoveredCategory(null)}
            >
              <button
                onClick={() => handleCategoryClick(category.id)}
                className={`py-2 transition-colors ${
                  selectedCategory === category.id
                    ? 'text-[#84B067] font-medium'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                {category.label}
              </button>

              {/* 서브카테고리 드롭다운 */}
              {category.subcategories && hoveredCategory === category.id && (
                <div className="absolute top-full left-1/2 -translate-x-1/2 pt-2 z-10">
                  <div className="bg-white dark:bg-gray-800 shadow-lg rounded-lg py-2 min-w-[100px]">
                    {category.subcategories.map((sub) => (
                      <button
                        key={sub.label}
                        onClick={() => {
                          setSelectedCategory(category.id);
                          handleSubcategoryClick(sub.label);
                        }}
                        className={`block w-full px-4 py-2 text-sm text-left transition-colors ${
                          selectedCategory === category.id && selectedSubcategory === sub.label
                            ? 'text-[#84B067] bg-gray-50 dark:bg-gray-700'
                            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-200'
                        }`}
                      >
                        {sub.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* 선택된 필터 표시 */}
        {selectedCategory && (
          <div className="flex items-center justify-center gap-2 mt-4 text-xs text-gray-500 dark:text-gray-400">
            <span>{categoryMenu.find((c) => c.id === selectedCategory)?.label}</span>
            {selectedSubcategory && (
              <>
                <span>/</span>
                <span>{selectedSubcategory}</span>
              </>
            )}
            <button
              onClick={() => {
                setSelectedCategory(null);
                setSelectedSubcategory(null);
              }}
              className="ml-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              ✕
            </button>
          </div>
        )}
      </nav>

      {/* 상품 목록 */}
      {loading ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">로딩 중...</div>
      ) : error ? (
        <div className="text-center py-12">
          <p className="text-red-500">{error}</p>
        </div>
      ) : products.length === 0 ? (
        <div className="text-center py-12 text-gray-500 dark:text-gray-400">
          등록된 상품이 없습니다.
        </div>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}
