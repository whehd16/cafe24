/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    // 카페24 이미지 도메인 허용
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.cafe24.com',
      },
      {
        protocol: 'https',
        hostname: '*.cafe24img.com',
      },
    ],
  },
};

module.exports = nextConfig;
