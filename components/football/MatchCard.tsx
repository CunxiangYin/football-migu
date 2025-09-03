'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, MapPin } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Match } from '@/types/football';

interface MatchCardProps {
  match: Match;
  className?: string;
}

export function MatchCard({ match, className }: MatchCardProps) {
  const formatDateTime = (dateTime: string) => {
    const date = new Date(dateTime);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return {
      date: `${month}月${day}日`,
      time: `${hours}:${minutes}`
    };
  };

  const { date, time } = formatDateTime(match.dateTime);

  return (
    <Card className={cn("overflow-hidden", className)}>
      <CardContent className="p-4 space-y-4">
        {/* League Info */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img 
              src={match.league.logo} 
              alt={match.league.name}
              className="h-5 w-5 rounded"
            />
            <span className="text-sm font-medium">{match.league.name}</span>
            {match.round && (
              <Badge variant="secondary" className="text-xs">
                {match.round}
              </Badge>
            )}
          </div>
          <Badge 
            variant={match.status === 'live' ? 'destructive' : 'outline'}
            className="text-xs"
          >
            {match.status === 'live' ? '进行中' : match.status === 'finished' ? '已结束' : '未开始'}
          </Badge>
        </div>

        {/* Teams Display */}
        <div className="relative">
          <div className="grid grid-cols-3 items-center gap-4">
            {/* Home Team */}
            <div className="flex flex-col items-center space-y-2">
              <div className="relative">
                <img 
                  src={match.homeTeam.logo} 
                  alt={match.homeTeam.name}
                  className="h-16 w-16 rounded-lg bg-muted p-2"
                />
              </div>
              <span className="text-sm font-medium text-center line-clamp-2">
                {match.homeTeam.name}
              </span>
            </div>

            {/* VS Badge */}
            <div className="flex items-center justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-violet-600 rounded-full blur-xl opacity-30" />
                <div className="relative bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-full px-4 py-2 text-lg font-bold">
                  VS
                </div>
              </div>
            </div>

            {/* Away Team */}
            <div className="flex flex-col items-center space-y-2">
              <div className="relative">
                <img 
                  src={match.awayTeam.logo} 
                  alt={match.awayTeam.name}
                  className="h-16 w-16 rounded-lg bg-muted p-2"
                />
              </div>
              <span className="text-sm font-medium text-center line-clamp-2">
                {match.awayTeam.name}
              </span>
            </div>
          </div>
        </div>

        {/* Match Info */}
        <div className="flex items-center justify-center gap-4 text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            <span>{date} {time}</span>
          </div>
          {match.stadium && (
            <>
              <span>·</span>
              <div className="flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                <span className="line-clamp-1">{match.stadium}</span>
              </div>
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
}