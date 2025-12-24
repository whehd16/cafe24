'use client';

import Image from 'next/image';

/**
 * 메인 페이지
 *
 * 흰 배경에 물감 브러시 이미지 애니메이션이 있는 랜딩 페이지
 */
export default function HomePage() {
  return (
    <div className="min-h-screen w-full bg-white dark:bg-gray-900 relative overflow-hidden">
      {/* 물감 브러시 이미지 애니메이션 */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="paint-image-container">
          <Image
            src="/paint-stroke.png"
            alt="Paint stroke"
            width={600}
            height={800}
            className="paint-image"
            priority
          />
        </div>
      </div>
    </div>
  );
}
