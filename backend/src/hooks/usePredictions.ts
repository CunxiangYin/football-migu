'use client'

import { useState, useEffect, useCallback } from 'react'
import { Prediction, FilterType, TabType } from '@/types/predictions'
import { generateMockPredictions } from '@/utils/mockPredictionsData'

interface UsePredictionsOptions {
  filter: FilterType
  tab: TabType
  pageSize?: number
}

interface UsePredictionsResult {
  predictions: Prediction[]
  loading: boolean
  error: Error | null
  hasMore: boolean
  loadMore: () => Promise<void>
  refresh: () => Promise<void>
}

export function usePredictions({ 
  filter, 
  tab, 
  pageSize = 10 
}: UsePredictionsOptions): UsePredictionsResult {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(true)

  // Initial load and filter change
  useEffect(() => {
    loadPredictions(true)
  }, [filter, tab])

  const loadPredictions = async (reset: boolean = false) => {
    try {
      setLoading(true)
      setError(null)

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500))

      // Generate mock data
      const newPredictions = generateMockPredictions(pageSize)
      
      // Apply filters
      let filteredPredictions = [...newPredictions]
      
      if (filter === 'winning_streak') {
        filteredPredictions = filteredPredictions.filter(p => p.expert.winStreak >= 5)
      } else if (filter === 'returns') {
        filteredPredictions = filteredPredictions.filter(p => 
          p.expert.badges.some(b => b.type === 'return_rate')
        )
      }

      // Apply tab filter
      if (tab === 'football') {
        filteredPredictions = filteredPredictions.filter(p => 
          !['NBA', 'CBA'].includes(p.match.league)
        )
      } else if (tab === 'basketball') {
        filteredPredictions = filteredPredictions.filter(p => 
          ['NBA', 'CBA'].includes(p.match.league)
        )
      }

      if (reset) {
        setPredictions(filteredPredictions)
        setPage(1)
      } else {
        setPredictions(prev => [...prev, ...filteredPredictions])
      }

      // Simulate pagination end
      if (page >= 5) {
        setHasMore(false)
      }
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }

  const loadMore = useCallback(async () => {
    if (!hasMore || loading) return
    setPage(prev => prev + 1)
    await loadPredictions(false)
  }, [hasMore, loading, page])

  const refresh = useCallback(async () => {
    setHasMore(true)
    await loadPredictions(true)
  }, [])

  return {
    predictions,
    loading,
    error,
    hasMore,
    loadMore,
    refresh
  }
}