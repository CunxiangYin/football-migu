import { useState, useEffect, useRef, RefObject } from 'react';

interface UsePullToRefreshOptions {
  onRefresh: () => Promise<void>;
  containerRef?: RefObject<HTMLElement>;
  threshold?: number;
}

export function usePullToRefresh({
  onRefresh,
  containerRef,
  threshold = 80,
}: UsePullToRefreshOptions) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [pullDistance, setPullDistance] = useState(0);
  const startY = useRef(0);
  const isPulling = useRef(false);

  useEffect(() => {
    const container = containerRef?.current || document.body;
    let touchStartY = 0;

    const handleTouchStart = (e: TouchEvent) => {
      if (container.scrollTop === 0) {
        touchStartY = e.touches[0].clientY;
        startY.current = touchStartY;
        isPulling.current = true;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!isPulling.current) return;
      
      const currentY = e.touches[0].clientY;
      const distance = currentY - startY.current;
      
      if (distance > 0 && container.scrollTop === 0) {
        e.preventDefault();
        setPullDistance(Math.min(distance, threshold * 1.5));
      }
    };

    const handleTouchEnd = async () => {
      if (!isPulling.current) return;
      
      isPulling.current = false;
      
      if (pullDistance > threshold) {
        setIsRefreshing(true);
        setPullDistance(0);
        
        try {
          await onRefresh();
        } finally {
          setIsRefreshing(false);
        }
      } else {
        setPullDistance(0);
      }
    };

    container.addEventListener('touchstart', handleTouchStart, { passive: false });
    container.addEventListener('touchmove', handleTouchMove, { passive: false });
    container.addEventListener('touchend', handleTouchEnd);

    return () => {
      container.removeEventListener('touchstart', handleTouchStart);
      container.removeEventListener('touchmove', handleTouchMove);
      container.removeEventListener('touchend', handleTouchEnd);
    };
  }, [onRefresh, threshold, pullDistance, containerRef]);

  return {
    isRefreshing,
    pullDistance,
    pullProgress: Math.min((pullDistance / threshold) * 100, 100),
  };
}