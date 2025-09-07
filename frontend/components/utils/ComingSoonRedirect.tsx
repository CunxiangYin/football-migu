'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface ComingSoonRedirectProps {
  feature?: string;
  delay?: number;
}

export function ComingSoonRedirect({ feature = '该功能', delay = 0 }: ComingSoonRedirectProps) {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push(`/coming-soon?feature=${encodeURIComponent(feature)}`);
    }, delay);

    return () => clearTimeout(timer);
  }, [feature, delay, router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        <p className="mt-4 text-gray-600">正在跳转...</p>
      </div>
    </div>
  );
}

// 用于按钮和链接的处理函数
export function handleComingSoon(router: any, feature: string) {
  router.push(`/coming-soon?feature=${encodeURIComponent(feature)}`);
}