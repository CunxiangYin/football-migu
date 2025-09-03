'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { 
  Heart, 
  Bookmark, 
  MessageCircle, 
  Gift,
  Share2
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Engagement } from '@/types/football';

interface BottomActionBarProps {
  engagement: Engagement;
  onLike: () => void;
  onSave: () => void;
  onComment: () => void;
  onTip: () => void;
  className?: string;
}

export function BottomActionBar({
  engagement,
  onLike,
  onSave,
  onComment,
  onTip,
  className
}: BottomActionBarProps) {
  const formatNumber = (num: number) => {
    if (num >= 10000) {
      return `${(num / 10000).toFixed(1)}万`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  };

  return (
    <div className={cn(
      "fixed bottom-0 left-0 right-0 z-50 border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60",
      className
    )}>
      <div className="flex items-center justify-between px-4 py-2">
        <div className="flex items-center gap-1">
          {/* Like Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={onLike}
            className="gap-1.5 hover:bg-accent"
          >
            <Heart 
              className={cn(
                "h-4 w-4 transition-colors",
                engagement.isLiked && "fill-red-500 text-red-500"
              )}
            />
            <span className="text-xs font-medium">
              {formatNumber(engagement.likes)}
            </span>
          </Button>

          {/* Save Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={onSave}
            className="gap-1.5 hover:bg-accent"
          >
            <Bookmark 
              className={cn(
                "h-4 w-4 transition-colors",
                engagement.isSaved && "fill-yellow-500 text-yellow-500"
              )}
            />
            <span className="text-xs font-medium">
              {formatNumber(engagement.saves)}
            </span>
          </Button>

          {/* Comment Button */}
          <Button
            variant="ghost"
            size="sm"
            onClick={onComment}
            className="gap-1.5 hover:bg-accent"
          >
            <MessageCircle className="h-4 w-4" />
            <span className="text-xs font-medium">
              {formatNumber(engagement.comments)}
            </span>
          </Button>
        </div>

        {/* Tip Button */}
        <Button
          size="sm"
          onClick={onTip}
          className="gap-1.5 bg-gradient-to-r from-purple-600 to-violet-600 text-white hover:from-purple-700 hover:to-violet-700 shadow-lg shadow-violet-500/25"
        >
          <Gift className="h-4 w-4" />
          <span className="text-xs font-semibold">打赏专家</span>
          {engagement.tips > 0 && (
            <Badge className="ml-1 h-4 px-1 bg-white/20 text-white text-xs">
              {formatNumber(engagement.tips)}
            </Badge>
          )}
        </Button>
      </div>
    </div>
  );
}

// Note: Badge import should be added at the top if used
import { Badge } from '@/components/ui/badge';