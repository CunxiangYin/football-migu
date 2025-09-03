import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { matchesApi } from '@/lib/api/matches';
import { expertsApi } from '@/lib/api/experts';
import { MatchDetail } from '@/types/football';
import { useState } from 'react';

export function useMatchDetail(matchId: string | number) {
  const queryClient = useQueryClient();
  const [isFollowing, setIsFollowing] = useState(false);

  // Fetch match detail
  const { data: matchDetail, isLoading, error } = useQuery({
    queryKey: ['match', matchId],
    queryFn: async () => {
      const match = await matchesApi.getMatchDetail(matchId);
      
      // Fetch all related data in parallel
      const [predictions, odds, analysis, statistics, engagement] = await Promise.all([
        matchesApi.getMatchPredictions(matchId),
        matchesApi.getBettingOdds(matchId),
        matchesApi.getMatchAnalysis(matchId),
        matchesApi.getMatchStatistics(matchId),
        matchesApi.getEngagement(matchId),
      ]);

      // Combine all data
      const detail: MatchDetail = {
        ...match,
        predictions,
        betting_odds: odds,
        analysis,
        statistics,
        engagement,
      };

      // Set initial following state if expert exists
      if (detail.expert) {
        setIsFollowing(detail.expert.is_following || false);
      }

      return detail;
    },
    staleTime: 30 * 1000, // Consider data stale after 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
  });

  // Like mutation
  const likeMutation = useMutation({
    mutationFn: () => matchesApi.likeMatch(matchId),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['match', matchId] });
      const previousData = queryClient.getQueryData<MatchDetail>(['match', matchId]);
      
      if (previousData?.engagement) {
        queryClient.setQueryData<MatchDetail>(['match', matchId], {
          ...previousData,
          engagement: {
            ...previousData.engagement,
            likes: previousData.engagement.likes + (previousData.engagement.user_liked ? -1 : 1),
            user_liked: !previousData.engagement.user_liked,
          },
        });
      }
      
      return { previousData };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      if (context?.previousData) {
        queryClient.setQueryData(['match', matchId], context.previousData);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['match', matchId] });
    },
  });

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: () => matchesApi.saveMatch(matchId),
    onMutate: async () => {
      // Optimistic update
      await queryClient.cancelQueries({ queryKey: ['match', matchId] });
      const previousData = queryClient.getQueryData<MatchDetail>(['match', matchId]);
      
      if (previousData?.engagement) {
        queryClient.setQueryData<MatchDetail>(['match', matchId], {
          ...previousData,
          engagement: {
            ...previousData.engagement,
            user_saved: !previousData.engagement.user_saved,
          },
        });
      }
      
      return { previousData };
    },
    onError: (err, variables, context) => {
      if (context?.previousData) {
        queryClient.setQueryData(['match', matchId], context.previousData);
      }
    },
  });

  // Follow expert mutation
  const followMutation = useMutation({
    mutationFn: (expertId: number) => expertsApi.toggleFollow(expertId),
    onSuccess: (data) => {
      setIsFollowing(data.is_following);
      // Update expert data in cache
      queryClient.invalidateQueries({ queryKey: ['match', matchId] });
    },
  });

  // Comment mutation
  const commentMutation = useMutation({
    mutationFn: (comment: string) => matchesApi.addComment(matchId, comment),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['match', matchId] });
    },
  });

  return {
    matchDetail,
    isLoading,
    error,
    isFollowing,
    actions: {
      like: () => likeMutation.mutate(),
      save: () => saveMutation.mutate(),
      follow: (expertId: number) => followMutation.mutate(expertId),
      comment: (text: string) => commentMutation.mutate(text),
    },
    isLiking: likeMutation.isPending,
    isSaving: saveMutation.isPending,
    isFollowPending: followMutation.isPending,
  };
}