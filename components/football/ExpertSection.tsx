'use client';

import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Eye, TrendingUp, UserCheck } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Expert } from '@/types/football';

interface ExpertSectionProps {
  expert: Expert;
  onFollow: () => void;
  publishedAt: string;
  views: number;
  className?: string;
}

export function ExpertSection({ 
  expert, 
  onFollow, 
  publishedAt,
  views,
  className 
}: ExpertSectionProps) {
  const formatNumber = (num: number) => {
    if (num >= 10000) {
      return `${(num / 10000).toFixed(1)}万`;
    }
    return num.toString();
  };

  const formatTime = (time: string) => {
    const date = new Date(time);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) {
      const minutes = Math.floor(diff / (1000 * 60));
      return `${minutes}分钟前`;
    } else if (hours < 24) {
      return `${hours}小时前`;
    } else {
      const days = Math.floor(hours / 24);
      return `${days}天前`;
    }
  };

  const getBadgeVariant = (badge: string) => {
    switch (badge) {
      case 'elite':
        return 'bg-gradient-to-r from-yellow-500 to-amber-500';
      case 'pro':
        return 'bg-gradient-to-r from-purple-500 to-violet-500';
      default:
        return 'bg-gradient-to-r from-blue-500 to-cyan-500';
    }
  };

  return (
    <div className={cn("space-y-3", className)}>
      <div className="flex items-start justify-between">
        <div className="flex gap-3">
          <Avatar className="h-12 w-12 ring-2 ring-violet-100 dark:ring-violet-900">
            <AvatarImage src={expert.avatar} alt={expert.name} />
            <AvatarFallback>{expert.name[0]}</AvatarFallback>
          </Avatar>
          
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <h2 className="text-base font-semibold">{expert.name}</h2>
              <Badge 
                className={cn(
                  "px-2 py-0.5 text-xs text-white border-0",
                  getBadgeVariant(expert.badge)
                )}
              >
                {expert.badge === 'elite' ? '金牌' : expert.badge === 'pro' ? '专业' : '认证'}
              </Badge>
            </div>
            
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <span className="flex items-center gap-1">
                <UserCheck className="h-3 w-3" />
                {formatNumber(expert.followers)} 粉丝
              </span>
              <span className="flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                胜率 {expert.winRate}%
              </span>
            </div>
          </div>
        </div>

        <Button
          size="sm"
          onClick={onFollow}
          className={cn(
            "h-8 px-4 text-xs font-medium transition-all",
            expert.isFollowing
              ? "bg-muted text-foreground hover:bg-muted/80"
              : "bg-gradient-to-r from-purple-600 to-violet-600 text-white hover:from-purple-700 hover:to-violet-700"
          )}
        >
          {expert.isFollowing ? '已关注' : '关注'}
        </Button>
      </div>

      {/* Description */}
      {expert.description && (
        <p className="text-sm text-muted-foreground line-clamp-2">
          {expert.description}
        </p>
      )}

      {/* Publish Info */}
      <div className="flex items-center gap-3 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <Eye className="h-3 w-3" />
          {formatNumber(views)} 阅读
        </span>
        <span>·</span>
        <span>{formatTime(publishedAt)}</span>
      </div>
    </div>
  );
}