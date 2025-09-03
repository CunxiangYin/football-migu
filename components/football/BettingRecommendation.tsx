'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown, Minus, Sparkles } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import type { BettingOdds } from '@/types/football';

interface BettingRecommendationProps {
  odds: BettingOdds;
  className?: string;
}

export function BettingRecommendation({ odds, className }: BettingRecommendationProps) {
  const getTrendIcon = (change?: 'up' | 'down' | 'stable') => {
    switch (change) {
      case 'up':
        return <TrendingUp className="h-3 w-3 text-green-500" />;
      case 'down':
        return <TrendingDown className="h-3 w-3 text-red-500" />;
      default:
        return <Minus className="h-3 w-3 text-muted-foreground" />;
    }
  };

  const options = [
    { 
      label: '主胜', 
      data: odds.homeWin, 
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50 dark:bg-blue-950'
    },
    { 
      label: '平局', 
      data: odds.draw, 
      color: 'from-gray-500 to-slate-500',
      bgColor: 'bg-gray-50 dark:bg-gray-950'
    },
    { 
      label: '客胜', 
      data: odds.awayWin, 
      color: 'from-red-500 to-orange-500',
      bgColor: 'bg-red-50 dark:bg-red-950'
    }
  ];

  return (
    <Card className={cn("overflow-hidden", className)}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">投注推荐</CardTitle>
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">置信度</span>
            <div className="flex items-center gap-1">
              <Progress value={odds.confidence} className="h-1.5 w-12" />
              <span className="text-xs font-semibold">{odds.confidence}%</span>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pb-4">
        <div className="grid grid-cols-3 gap-3">
          {options.map((option) => (
            <div
              key={option.label}
              className={cn(
                "relative rounded-lg border-2 p-3 transition-all",
                option.data.recommended
                  ? "border-violet-500 bg-violet-50 dark:bg-violet-950/30"
                  : "border-border hover:border-muted-foreground/30"
              )}
            >
              {option.data.recommended && (
                <div className="absolute -top-2 left-1/2 -translate-x-1/2">
                  <Badge 
                    className="h-5 bg-gradient-to-r from-purple-600 to-violet-600 text-white text-xs px-2 gap-1"
                  >
                    <Sparkles className="h-3 w-3" />
                    推荐
                  </Badge>
                </div>
              )}
              
              <div className="space-y-2 pt-1">
                <div className="text-center">
                  <div className="text-xs text-muted-foreground mb-1">
                    {option.label}
                  </div>
                  <div className="flex items-center justify-center gap-1">
                    <span className="text-xl font-bold">
                      {option.data.odds.toFixed(2)}
                    </span>
                    {getTrendIcon(option.data.change)}
                  </div>
                </div>
                
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">概率</span>
                    <span className="font-medium">
                      {option.data.probability}%
                    </span>
                  </div>
                  <div className="relative h-1.5 w-full rounded-full bg-muted overflow-hidden">
                    <div 
                      className={cn(
                        "absolute left-0 top-0 h-full rounded-full bg-gradient-to-r",
                        option.color
                      )}
                      style={{ width: `${option.data.probability}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Info */}
        <div className="mt-4 flex items-center justify-center">
          <p className="text-xs text-muted-foreground text-center">
            基于AI分析的投注建议，仅供参考
          </p>
        </div>
      </CardContent>
    </Card>
  );
}