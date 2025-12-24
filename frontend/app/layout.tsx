import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/layout/Header';
import { ThemeProvider } from '@/components/ThemeProvider';

export const metadata: Metadata = {
  title: 'Pistachio Love',
  description: '피스타치오 디저트 쇼핑몰',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        <ThemeProvider>
          {/* 상단 헤더 */}
          <Header />

          {/* 메인 콘텐츠 */}
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
