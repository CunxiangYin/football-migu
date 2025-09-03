import { useState, useEffect, useCallback } from 'react';
import { PredictionItem, ExpertProfile, TabType, FilterType } from '@/types/predictions';
import { generateMockPredictions, generateMockExperts } from '@/utils/mockPredictionsData';

interface UsePredictionsOptions {
  tab: TabType;
  filter: FilterType;
  expertId: string | null;
  pageSize?: number;
}

interface UsePredictionsReturn {
  predictions: PredictionItem[];
  experts: ExpertProfile[];
  isLoading: boolean;
  isLoadingMore: boolean;
  hasMore: boolean;
  error: Error | null;
  loadMore: () => Promise<void>;
  refresh: () => Promise<void>;
}

export function usePredictions({
  tab,
  filter,
  expertId,
  pageSize = 10,
}: UsePredictionsOptions): UsePredictionsReturn {
  const [predictions, setPredictions] = useState<PredictionItem[]>([]);
  const [experts, setExperts] = useState<ExpertProfile[]>([]);
  const [page, setPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, [tab, filter, expertId]);

  const loadInitialData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Load experts
      const mockExperts = generateMockExperts();
      setExperts(mockExperts);
      
      // Load predictions
      const mockPredictions = generateMockPredictions(pageSize, 1, {
        tab,
        filter,
        expertId,
      });
      
      setPredictions(mockPredictions);
      setPage(1);
      setHasMore(mockPredictions.length === pageSize);
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadMore = useCallback(async () => {
    if (isLoadingMore || !hasMore) return;
    
    setIsLoadingMore(true);
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 600));
      
      const nextPage = page + 1;
      const newPredictions = generateMockPredictions(pageSize, nextPage, {
        tab,
        filter,
        expertId,
      });
      
      if (newPredictions.length === 0) {
        setHasMore(false);
      } else {
        setPredictions(prev => [...prev, ...newPredictions]);
        setPage(nextPage);
        setHasMore(newPredictions.length === pageSize);
      }
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsLoadingMore(false);
    }
  }, [page, isLoadingMore, hasMore, pageSize, tab, filter, expertId]);

  const refresh = useCallback(async () => {
    await loadInitialData();
  }, [tab, filter, expertId]);

  return {
    predictions,
    experts,
    isLoading,
    isLoadingMore,
    hasMore,
    error,
    loadMore,
    refresh,
  };
}