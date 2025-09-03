'use client'

import React, { useState, useCallback, useMemo } from 'react'
import { RefreshCw, AlertCircle } from 'lucide-react'
import { PageHeader } from './PageHeader'
import { ExpertProfilesSection } from './ExpertProfilesSection'
import { FilterTabs } from './FilterTabs'
import { PredictionCard } from './PredictionCard'
import { PredictionListSkeleton } from './PredictionCardSkeleton'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { usePredictions } from '@/hooks/usePredictions'
import { useInfiniteScroll } from '@/hooks/useInfiniteScroll'
import { usePullToRefresh } from '@/hooks/usePullToRefresh'
import { FilterType, TabType, Expert } from '@/types/predictions'
import { generateMockExperts } from '@/utils/mockPredictionsData'
import { cn } from '@/lib/utils'

export function ExpertPredictionsPage() {
  // State
  const [activeTab, setActiveTab] = useState<TabType>('football')
  const [activeFilter, setActiveFilter] = useState<FilterType>('hot')
  const [showBanner, setShowBanner] = useState(true)
  const [selectedExpertId, setSelectedExpertId] = useState<string | undefined>()

  // Mock experts data
  const experts = useMemo(() => generateMockExperts(15), [])

  // Fetch predictions
  const { 
    predictions, 
    loading, 
    error, 
    hasMore, 
    loadMore, 
    refresh 
  } = usePredictions({
    filter: activeFilter,
    tab: activeTab
  })

  // Infinite scroll
  const sentinelRef = useInfiniteScroll({
    onLoadMore: loadMore,
    hasMore,
    loading
  })

  // Pull to refresh
  const { 
    pullDistance, 
    isRefreshing, 
    isPulling,
    containerProps 
  } = usePullToRefresh({
    onRefresh: refresh
  })

  // Handlers
  const handleExpertClick = useCallback((expert: Expert) => {
    setSelectedExpertId(expert.id)
    // Could navigate to expert detail page or filter by expert
    console.log('Expert clicked:', expert)
  }, [])

  const handlePredictionClick = useCallback((predictionId: string) => {
    // Navigate to prediction detail
    console.log('Prediction clicked:', predictionId)
  }, [])

  const handleTabChange = useCallback((tab: TabType) => {
    setActiveTab(tab)
    setSelectedExpertId(undefined)
  }, [])

  const handleFilterChange = useCallback((filter: FilterType) => {
    setActiveFilter(filter)
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <PageHeader
        activeTab={activeTab}
        onTabChange={handleTabChange}
        showBanner={showBanner}
        onCloseBanner={() => setShowBanner(false)}
      />

      {/* Pull to refresh container */}
      <div 
        className="relative"
        {...containerProps}
      >
        {/* Pull to refresh indicator */}
        {(isPulling || isRefreshing) && (
          <div 
            className="absolute top-0 left-0 right-0 flex items-center justify-center py-4 transition-all duration-300 z-30"
            style={{ 
              transform: `translateY(${pullDistance}px)`,
              opacity: pullDistance > 40 ? 1 : pullDistance / 40
            }}
          >
            <div className="flex items-center gap-2">
              <RefreshCw 
                className={cn(
                  "h-5 w-5 text-blue-500",
                  isRefreshing && "animate-spin"
                )}
              />
              <span className="text-sm text-gray-600">
                {isRefreshing ? '刷新中...' : pullDistance > 80 ? '释放刷新' : '下拉刷新'}
              </span>
            </div>
          </div>
        )}

        {/* Main content with pull effect */}
        <div 
          className={cn(
            "transition-transform duration-300",
            isPulling && "translate-y-2"
          )}
          style={{ 
            transform: isPulling ? `translateY(${pullDistance}px)` : undefined 
          }}
        >
          {/* Expert Profiles */}
          <ExpertProfilesSection
            experts={experts}
            onExpertClick={handleExpertClick}
            selectedExpertId={selectedExpertId}
          />

          {/* Filter Tabs */}
          <FilterTabs
            activeFilter={activeFilter}
            onFilterChange={handleFilterChange}
          />

          {/* Predictions List */}
          <div className="px-4 py-3">
            {/* Error State */}
            {error && (
              <Alert variant="destructive" className="mb-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  加载失败，请稍后重试
                </AlertDescription>
              </Alert>
            )}

            {/* Loading State - Initial Load */}
            {loading && predictions.length === 0 && (
              <PredictionListSkeleton count={3} />
            )}

            {/* Predictions List */}
            {predictions.map((prediction) => (
              <PredictionCard
                key={prediction.id}
                prediction={prediction}
                onCardClick={() => handlePredictionClick(prediction.id)}
                onExpertClick={() => handleExpertClick(prediction.expert)}
              />
            ))}

            {/* Loading More Indicator */}
            {loading && predictions.length > 0 && (
              <div className="py-4 text-center">
                <div className="inline-flex items-center gap-2 text-sm text-gray-500">
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  加载更多...
                </div>
              </div>
            )}

            {/* No More Data */}
            {!hasMore && predictions.length > 0 && (
              <div className="py-8 text-center text-sm text-gray-500">
                没有更多内容了
              </div>
            )}

            {/* Empty State */}
            {!loading && predictions.length === 0 && (
              <div className="py-16 text-center">
                <div className="text-gray-400 mb-4">
                  <svg
                    className="mx-auto h-12 w-12"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                </div>
                <p className="text-gray-500 mb-4">暂无预测内容</p>
                <Button onClick={refresh} variant="outline" size="sm">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  刷新试试
                </Button>
              </div>
            )}

            {/* Infinite Scroll Sentinel */}
            <div ref={sentinelRef} className="h-1" />
          </div>
        </div>
      </div>
    </div>
  )
}