'use client';

import React, { useState, useEffect, useRef } from 'react';
import { PageHeader } from './PageHeader';
import { ExpertProfilesSection } from './ExpertProfilesSection';
import { FilterTabs } from './FilterTabs';
import { PredictionCard } from './PredictionCard';
import { PredictionCardSkeleton } from './PredictionCardSkeleton';
import { RealMatchesList } from './RealMatchesList';
import { usePredictions } from '@/hooks/usePredictions';
import { useInfiniteScroll } from '@/hooks/useInfiniteScroll';
import { usePullToRefresh } from '@/hooks/usePullToRefresh';
import { TabType, FilterType } from '@/types/predictions';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Button } from '@/components/ui/button';
import { RefreshCw, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';

export function ExpertPredictionsPage() {
  const [activeTab, setActiveTab] = useState<TabType>('football');
  const [activeFilter, setActiveFilter] = useState<FilterType>('hot');
  const [selectedExpertId, setSelectedExpertId] = useState<string | null>(null);
  const [showScrollTop, setShowScrollTop] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const {
    predictions,
    experts,
    isLoading,
    isLoadingMore,
    hasMore,
    error,
    loadMore,
    refresh,
  } = usePredictions({
    tab: activeTab,
    filter: activeFilter,
    expertId: selectedExpertId,
  });

  // Infinite scroll
  const { sentinelRef } = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    isLoading: isLoadingMore,
  });

  // Pull to refresh
  const { isRefreshing } = usePullToRefresh({
    onRefresh: refresh,
    containerRef: scrollContainerRef,
  });

  // Show/hide scroll to top button
  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = scrollContainerRef.current?.scrollTop || 0;
      setShowScrollTop(scrollTop > 500);
    };

    const container = scrollContainerRef.current;
    container?.addEventListener('scroll', handleScroll);
    return () => container?.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToTop = () => {
    scrollContainerRef.current?.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  const handleExpertSelect = (expertId: string) => {
    setSelectedExpertId(expertId === selectedExpertId ? null : expertId);
  };

  const handleLike = async (predictionId: string) => {
    // 跳转到功能未发布页面
    window.location.href = '/coming-soon?feature=点赞功能';
  };

  const handleSave = async (predictionId: string) => {
    // 跳转到功能未发布页面
    window.location.href = '/coming-soon?feature=收藏功能';
  };

  const handleComment = async (predictionId: string) => {
    // 跳转到功能未发布页面
    window.location.href = '/coming-soon?feature=评论功能';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <PageHeader activeTab={activeTab} onTabChange={setActiveTab} />
      
      <div 
        ref={scrollContainerRef}
        className="h-[calc(100vh-60px)] overflow-y-auto"
      >
        {/* Pull to refresh indicator */}
        {isRefreshing && (
          <div className="flex items-center justify-center p-4">
            <RefreshCw className="h-5 w-5 animate-spin text-primary" />
            <span className="ml-2 text-sm text-gray-600">刷新中...</span>
          </div>
        )}

        {/* Expert profiles horizontal scroll */}
        <ExpertProfilesSection
          experts={experts}
          selectedExpertId={selectedExpertId}
          onExpertSelect={handleExpertSelect}
        />

        {/* Filter tabs */}
        <FilterTabs
          activeFilter={activeFilter}
          onFilterChange={setActiveFilter}
        />

        {/* Show real matches when activeFilter is 'hot' */}
        {activeFilter === 'hot' ? (
          <RealMatchesList />
        ) : (
          /* Predictions list */
          <div className="px-4 pb-20">
            {isLoading && !predictions.length ? (
            // Initial loading state
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <PredictionCardSkeleton key={i} />
              ))}
            </div>
          ) : error ? (
            // Error state
            <div className="flex flex-col items-center justify-center py-12">
              <p className="text-gray-500 mb-4">加载失败</p>
              <Button onClick={refresh} variant="outline" size="sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                重试
              </Button>
            </div>
          ) : predictions.length === 0 ? (
            // Empty state
            <div className="flex flex-col items-center justify-center py-12">
              <p className="text-gray-500">暂无预测数据</p>
            </div>
          ) : (
            // Predictions list
            <div className="space-y-4">
              {predictions.map((prediction) => (
                <PredictionCard
                  key={prediction.id}
                  prediction={prediction}
                  onLike={() => handleLike(prediction.id)}
                  onSave={() => handleSave(prediction.id)}
                  onComment={() => handleComment(prediction.id)}
                />
              ))}

              {/* Loading more indicator */}
              {isLoadingMore && (
                <div className="py-4">
                  <PredictionCardSkeleton />
                </div>
              )}

              {/* Infinite scroll sentinel */}
              <div ref={sentinelRef} className="h-1" />

              {/* No more data */}
              {!hasMore && predictions.length > 0 && (
                <div className="text-center py-8 text-sm text-gray-500">
                  没有更多数据了
                </div>
              )}
            </div>
          )}
          </div>
        )}
      </div>

      {/* Scroll to top button */}
      <Button
        onClick={scrollToTop}
        size="icon"
        className={cn(
          "fixed bottom-20 right-4 z-50 rounded-full shadow-lg transition-all duration-300",
          showScrollTop
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-10 pointer-events-none"
        )}
      >
        <ChevronUp className="h-5 w-5" />
      </Button>
    </div>
  );
}