'use client'

import { useState, useRef, useCallback, useEffect } from 'react'

interface UsePullToRefreshOptions {
  onRefresh: () => Promise<void>
  threshold?: number
  resistance?: number
}

interface UsePullToRefreshResult {
  pullDistance: number
  isRefreshing: boolean
  isPulling: boolean
  containerProps: {
    onTouchStart: (e: React.TouchEvent) => void
    onTouchMove: (e: React.TouchEvent) => void
    onTouchEnd: () => void
  }
}

export function usePullToRefresh({
  onRefresh,
  threshold = 80,
  resistance = 2.5
}: UsePullToRefreshOptions): UsePullToRefreshResult {
  const [pullDistance, setPullDistance] = useState(0)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [isPulling, setIsPulling] = useState(false)
  
  const startY = useRef(0)
  const currentY = useRef(0)

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    if (window.scrollY === 0 && !isRefreshing) {
      startY.current = e.touches[0].clientY
      setIsPulling(true)
    }
  }, [isRefreshing])

  const handleTouchMove = useCallback((e: React.TouchEvent) => {
    if (!isPulling || isRefreshing) return

    currentY.current = e.touches[0].clientY
    const distance = currentY.current - startY.current

    if (distance > 0) {
      // Apply resistance
      const resistedDistance = distance / resistance
      setPullDistance(Math.min(resistedDistance, threshold * 1.5))
      
      // Prevent default scrolling when pulling
      if (window.scrollY === 0) {
        e.preventDefault()
      }
    }
  }, [isPulling, isRefreshing, resistance, threshold])

  const handleTouchEnd = useCallback(async () => {
    if (!isPulling) return

    setIsPulling(false)

    if (pullDistance >= threshold && !isRefreshing) {
      setIsRefreshing(true)
      
      try {
        await onRefresh()
      } finally {
        setIsRefreshing(false)
        setPullDistance(0)
      }
    } else {
      // Animate back to 0
      setPullDistance(0)
    }
  }, [isPulling, pullDistance, threshold, isRefreshing, onRefresh])

  // Reset pull distance when not pulling
  useEffect(() => {
    if (!isPulling && !isRefreshing && pullDistance !== 0) {
      const timer = setTimeout(() => setPullDistance(0), 300)
      return () => clearTimeout(timer)
    }
  }, [isPulling, isRefreshing, pullDistance])

  return {
    pullDistance,
    isRefreshing,
    isPulling,
    containerProps: {
      onTouchStart: handleTouchStart,
      onTouchMove: handleTouchMove,
      onTouchEnd: handleTouchEnd
    }
  }
}