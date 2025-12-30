'use client';

import { useState, useEffect } from 'react';
import TiltedCard from '@/components/ui/TiltedCard';

interface ImageSliderProps {
  slides: string[];
}

export default function ImageSlider({ slides }: ImageSliderProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [repeatCount, setRepeatCount] = useState(1);
  const [cardSize, setCardSize] = useState({ width: '70vw', height: '50vh' });

  // 화면 크기에 따라 이미지 반복 개수 및 크기 조절
  useEffect(() => {
    const updateLayout = () => {
      if (window.innerWidth >= 1024) {
        setRepeatCount(3); // lg 이상: 3개
        setCardSize({ width: '280px', height: '400px' });
      } else if (window.innerWidth >= 640) {
        setRepeatCount(2); // sm~lg: 2개
        setCardSize({ width: '250px', height: '350px' });
      } else {
        setRepeatCount(1); // 모바일: 1개
        setCardSize({ width: '280px', height: '400px' });
      }
    };

    updateLayout();
    window.addEventListener('resize', updateLayout);
    return () => window.removeEventListener('resize', updateLayout);
  }, []);

  const currentSlide = slides[currentIndex];

  return (
    <div className="min-h-screen w-full bg-[#f0f7eb] dark:bg-gray-900 relative overflow-hidden flex flex-col items-center justify-center">
      {/* 이미지 컨테이너 - 같은 이미지를 반복 */}
      <div className="flex items-center justify-center gap-4 sm:gap-6 lg:gap-8 px-4">
        {Array.from({ length: repeatCount }).map((_, index) => {
          // 3개일 때 1번(index 0), 3번(index 2)은 180도 회전
          const shouldRotate = repeatCount === 3 && (index === 0 || index === 2);
          return (
            <div
              key={index}
              className={`transition-all duration-500 ${shouldRotate ? 'rotate-180' : ''}`}
            >
              <TiltedCard
                imageSrc={currentSlide}
                altText={`Slide ${currentIndex + 1}`}
                containerHeight={cardSize.height}
                containerWidth={cardSize.width}
                imageHeight={cardSize.height}
                imageWidth={cardSize.width}
                rotateAmplitude={12}
                scaleOnHover={1.05}
                showMobileWarning={false}
                showTooltip={false}
              />
            </div>
          );
        })}
      </div>

      {/* 하단 인디케이터 (동그라미 버튼) */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3 z-10">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentIndex
                ? 'bg-[#84B067] scale-125'
                : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'
            }`}
            aria-label={`슬라이드 ${index + 1}로 이동`}
          />
        ))}
      </div>
    </div>
  );
}
