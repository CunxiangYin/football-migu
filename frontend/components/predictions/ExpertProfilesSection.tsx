'use client';

import React, { useRef } from 'react';
import { ExpertProfile } from '@/types/predictions';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { CheckCircle2 } from 'lucide-react';

interface ExpertProfilesSectionProps {
  experts: ExpertProfile[];
  selectedExpertId: string | null;
  onExpertSelect: (expertId: string) => void;
}

export function ExpertProfilesSection({
  experts,
  selectedExpertId,
  onExpertSelect,
}: ExpertProfilesSectionProps) {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const getStreakColor = (streak: number) => {
    if (streak >= 14) return 'bg-red-600';
    if (streak >= 10) return 'bg-red-500';
    if (streak >= 7) return 'bg-orange-500';
    return 'bg-gray-500';
  };

  return (
    <div className="bg-white border-b">
      <div
        ref={scrollContainerRef}
        className="flex gap-4 px-4 py-4 overflow-x-auto scrollbar-hide"
      >
        {experts.map((expert) => (
          <button
            key={expert.id}
            onClick={() => onExpertSelect(expert.id)}
            className={cn(
              "flex flex-col items-center min-w-[70px] transition-opacity",
              selectedExpertId && selectedExpertId !== expert.id
                ? "opacity-50"
                : "opacity-100"
            )}
          >
            <div className="relative mb-2">
              <Avatar className="h-14 w-14 border-2 border-white shadow-sm">
                <AvatarImage src={expert.avatar} alt={expert.name} />
                <AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-500 text-white">
                  {expert.name.slice(0, 2)}
                </AvatarFallback>
              </Avatar>
              
              {/* Win streak badge */}
              <div
                className={cn(
                  "absolute -top-1 -right-1 rounded-full text-white text-xs font-bold px-1.5 py-0.5",
                  getStreakColor(expert.winStreak)
                )}
              >
                {expert.winStreak}
              </div>

              {/* Verified badge */}
              {expert.isVerified && (
                <CheckCircle2 className="absolute -bottom-1 -right-1 h-4 w-4 text-blue-500 bg-white rounded-full" />
              )}
            </div>

            <span className="text-xs font-medium text-gray-700 truncate max-w-[70px]">
              {expert.name}
            </span>
            
            <span className="text-xs text-red-500 font-semibold mt-0.5">
              {expert.winStreak}连红
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}