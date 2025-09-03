'use client';

import React from 'react';
import { PredictionItem } from '@/types/predictions';
import { Card } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Heart, 
  MessageCircle, 
  Bookmark, 
  Share2, 
  CheckCircle2,
  Eye,
  Clock
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { formatDistanceToNow } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import { useRouter } from 'next/navigation';

interface PredictionCardProps {
  prediction: PredictionItem;
  onLike?: () => void;
  onSave?: () => void;
  onComment?: () => void;
  onShare?: () => void;
}

export function PredictionCard({
  prediction,
  onLike,
  onSave,
  onComment,
  onShare,
}: PredictionCardProps) {
  const router = useRouter();
  const getBadgeStyle = (type: string) => {
    switch (type) {
      case 'streak':
        return 'bg-red-500 text-white';
      case 'hitRate':
        return 'bg-yellow-500 text-white';
      case 'returnRate':
        return 'bg-gray-500 text-white';
      default:
        return 'bg-gray-200 text-gray-700';
    }
  };

  const handleCardClick = (e: React.MouseEvent) => {
    // Prevent navigation when clicking on buttons
    const target = e.target as HTMLElement;
    if (target.closest('button')) {
      return;
    }
    router.push(`/prediction/${prediction.id}`);
  };

  return (
    <Card 
      className="p-4 hover:shadow-md transition-shadow cursor-pointer" 
      onClick={handleCardClick}
    >
      {/* Expert info header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Avatar className="h-10 w-10">
              <AvatarImage src={prediction.expert.avatar} />
              <AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-500 text-white text-sm">
                {prediction.expert.name.slice(0, 2)}
              </AvatarFallback>
            </Avatar>
            {prediction.expert.isVerified && (
              <CheckCircle2 className="absolute -bottom-0.5 -right-0.5 h-4 w-4 text-blue-500 bg-white rounded-full" />
            )}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-semibold text-sm">{prediction.expert.name}</span>
              {prediction.expert.badges.map((badge, idx) => (
                <Badge
                  key={idx}
                  className={cn("text-xs px-1.5 py-0", getBadgeStyle(badge.type))}
                >
                  {badge.text}
                </Badge>
              ))}
            </div>
          </div>
        </div>

        {/* Confidence percentage */}
        <div className="text-right">
          <div className="text-2xl font-bold text-red-500">{prediction.confidence}%</div>
          <div className="text-xs text-gray-500">命中率</div>
        </div>
      </div>

      {/* Prediction content */}
      <div className="mb-3">
        <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
          {prediction.title}
        </h3>
        {prediction.description && (
          <p className="text-sm text-gray-600 line-clamp-2">
            {prediction.description}
          </p>
        )}
      </div>

      {/* Match info */}
      <div className="flex items-center gap-2 mb-3 text-xs">
        <Badge variant="secondary" className="px-2 py-0.5">
          {prediction.match.league}
        </Badge>
        <span className="text-gray-500">
          {prediction.match.date} {prediction.match.time}
        </span>
        <span className="text-gray-700">
          {prediction.match.homeTeam.name} VS {prediction.match.awayTeam.name}
        </span>
      </div>

      {/* Footer with stats and actions */}
      <div className="flex items-center justify-between pt-3 border-t">
        <div className="flex items-center gap-4 text-xs text-gray-500">
          <span className="flex items-center gap-1">
            <Clock className="h-3 w-3" />
            {formatDistanceToNow(new Date(prediction.postedTime), {
              locale: zhCN,
              addSuffix: true,
            })}
          </span>
          <span className="flex items-center gap-1">
            <Eye className="h-3 w-3" />
            {prediction.viewCount}阅读
          </span>
        </div>

        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={onLike}
            className={cn(
              "h-8 px-2",
              prediction.isLiked && "text-red-500"
            )}
          >
            <Heart className={cn("h-4 w-4", prediction.isLiked && "fill-current")} />
            <span className="ml-1 text-xs">{prediction.likeCount || ''}</span>
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={onComment}
            className="h-8 px-2"
          >
            <MessageCircle className="h-4 w-4" />
            <span className="ml-1 text-xs">{prediction.commentCount || ''}</span>
          </Button>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={onSave}
            className={cn(
              "h-8 px-2",
              prediction.isSaved && "text-yellow-500"
            )}
          >
            <Bookmark className={cn("h-4 w-4", prediction.isSaved && "fill-current")} />
          </Button>
        </div>
      </div>
    </Card>
  );
}