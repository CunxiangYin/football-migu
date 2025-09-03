'use client'

import { useEffect, useRef, useCallback } from 'react'

interface UseInfiniteScrollOptions {
  onLoadMore: () => void
  hasMore: boolean
  loading: boolean
  threshold?: number
}

export function useInfiniteScroll({
  onLoadMore,
  hasMore,
  loading,
  threshold = 100
}: UseInfiniteScrollOptions) {
  const observerRef = useRef<IntersectionObserver | null>(null)
  const sentinelRef = useRef<HTMLDivElement>(null)

  const handleIntersection = useCallback(
    (entries: IntersectionObserverEntry[]) => {
      const [entry] = entries
      if (entry.isIntersecting && hasMore && !loading) {
        onLoadMore()
      }
    },
    [hasMore, loading, onLoadMore]
  )

  useEffect(() => {
    if (!sentinelRef.current) return

    // Clean up previous observer
    if (observerRef.current) {
      observerRef.current.disconnect()
    }

    // Create new observer
    observerRef.current = new IntersectionObserver(handleIntersection, {
      root: null,
      rootMargin: `${threshold}px`,
      threshold: 0
    })

    // Start observing
    observerRef.current.observe(sentinelRef.current)

    // Cleanup
    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect()
      }
    }
  }, [handleIntersection, threshold])

  return sentinelRef
}