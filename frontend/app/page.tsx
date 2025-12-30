import fs from 'fs';
import path from 'path';
import ImageSlider from '@/components/home/ImageSlider';

// 서버에서 slides 폴더의 이미지 목록을 읽어옴
function getSlides(): string[] {
  const slidesDir = path.join(process.cwd(), 'public', 'slides');
  const files = fs.readdirSync(slidesDir);
  return files
    .filter((file) => /\.(png|jpg|jpeg|gif|webp)$/i.test(file))
    .sort()
    .map((file) => `/slides/${file}`);
}

/**
 * 메인 페이지
 *
 * 이미지 슬라이더가 있는 랜딩 페이지
 */
export default function HomePage() {
  const slides = getSlides();

  return <ImageSlider slides={slides} />;
}
