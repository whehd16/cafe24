/**
 * 하단 푸터 컴포넌트
 */
export default function Footer() {
  return (
    <footer className="bg-gray-100 border-t border-gray-200">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* 회사 정보 */}
          <div>
            <h3 className="font-bold mb-4">SHOP</h3>
            <p className="text-gray-600 text-sm">
              카페24 API 연동 쇼핑몰
            </p>
          </div>

          {/* 고객 서비스 */}
          <div>
            <h3 className="font-bold mb-4">고객 서비스</h3>
            <ul className="text-gray-600 text-sm space-y-2">
              <li>배송 안내</li>
              <li>교환/반품</li>
              <li>자주 묻는 질문</li>
            </ul>
          </div>

          {/* 연락처 */}
          <div>
            <h3 className="font-bold mb-4">연락처</h3>
            <p className="text-gray-600 text-sm">
              이메일: help@shop.com<br />
              전화: 02-1234-5678
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 text-center text-gray-500 text-sm">
          © 2024 SHOP. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
