'use client';

import React, { useState } from 'react';
import { ArrowLeft, Share2, MoreVertical } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { ExpertSection } from './ExpertSection';
import { MatchCard } from './MatchCard';
import { BettingRecommendation } from './BettingRecommendation';
import { AnalysisTabs } from './AnalysisTabs';
import { StatsGrid } from './StatsGrid';
import { BottomActionBar } from './BottomActionBar';
import { ScrollArea } from '@/components/ui/scroll-area';
import type { MatchDetail } from '@/types/football';

interface FootballBettingDetailProps {
  data: MatchDetail;
  onBack?: () => void;
  onShare?: () => void;
}

export function FootballBettingDetail({ 
  data, 
  onBack,
  onShare 
}: FootballBettingDetailProps) {
  const [isFollowing, setIsFollowing] = useState(data.expert.isFollowing);
  const [engagement, setEngagement] = useState(data.engagement);

  const handleFollow = () => {
    setIsFollowing(!isFollowing);
  };

  const handleLike = () => {
    setEngagement(prev => ({
      ...prev,
      isLiked: !prev.isLiked,
      likes: prev.isLiked ? prev.likes - 1 : prev.likes + 1
    }));
  };

  const handleSave = () => {
    setEngagement(prev => ({
      ...prev,
      isSaved: !prev.isSaved,
      saves: prev.isSaved ? prev.saves - 1 : prev.saves + 1
    }));
  };

  const handleComment = () => {
    // Implement comment functionality
    console.log('Open comments');
  };

  const handleTip = () => {
    // Implement tip functionality
    console.log('Send tip');
  };

  return (
    <div className="relative min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center justify-between px-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={onBack}
            className="hover:bg-accent"
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          
          <h1 className="text-base font-semibold">专家预测</h1>
          
          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              onClick={onShare}
              className="hover:bg-accent"
            >
              <Share2 className="h-5 w-5" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="hover:bg-accent"
            >
              <MoreVertical className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <ScrollArea className="h-[calc(100vh-3.5rem-4rem)]">
        <div className="mx-auto max-w-2xl px-4 py-4 pb-20">
          {/* Expert Section */}
          <ExpertSection
            expert={{
              ...data.expert,
              isFollowing
            }}
            onFollow={handleFollow}
            publishedAt={engagement.publishedAt}
            views={engagement.views}
          />

          {/* Match Card */}
          <MatchCard match={data.match} className="mt-4" />

          {/* Betting Recommendation */}
          <BettingRecommendation 
            odds={data.betting} 
            className="mt-4"
          />

          {/* Analysis Tabs */}
          <AnalysisTabs 
            analysis={data.analysis}
            className="mt-4"
          />

          {/* Statistics Grid */}
          <StatsGrid 
            stats={data.stats}
            className="mt-4"
          />
        </div>
      </ScrollArea>

      {/* Bottom Action Bar */}
      <BottomActionBar
        engagement={engagement}
        onLike={handleLike}
        onSave={handleSave}
        onComment={handleComment}
        onTip={handleTip}
      />
    </div>
  );
}