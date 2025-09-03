'use client'

import React, { useRef } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'
import { Expert } from '@/types/predictions'
import { cn } from '@/lib/utils'

interface ExpertProfilesSectionProps {
  experts: Expert[]
  onExpertClick?: (expert: Expert) => void
  selectedExpertId?: string
}

export function ExpertProfilesSection({ 
  experts, 
  onExpertClick,
  selectedExpertId 
}: ExpertProfilesSectionProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  const scrollLeft = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: -200, behavior: 'smooth' })
    }
  }

  const scrollRight = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollBy({ left: 200, behavior: 'smooth' })
    }
  }

  const getStreakLabel = (streak: number): string => {
    if (streak >= 14) return '14连红'
    if (streak >= 12) return '12连红'
    if (streak >= 10) return '10连红'
    if (streak >= 9) return '9连红'
    if (streak >= 7) return '7连红'
    if (streak >= 5) return '5连红'
    return `${streak}连红`
  }

  const getStreakColor = (streak: number): string => {
    if (streak >= 14) return 'bg-red-600'
    if (streak >= 10) return 'bg-red-500'
    if (streak >= 7) return 'bg-orange-500'
    return 'bg-orange-400'
  }

  return (
    <div className="bg-white py-4">
      <div className="relative">
        {/* Scroll Buttons */}
        <Button
          variant="ghost"
          size="icon"
          className="absolute left-0 top-1/2 -translate-y-1/2 z-10 h-8 w-8 bg-white/80 shadow-md"
          onClick={scrollLeft}
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-0 top-1/2 -translate-y-1/2 z-10 h-8 w-8 bg-white/80 shadow-md"
          onClick={scrollRight}
        >
          <ChevronRight className="h-4 w-4" />
        </Button>

        {/* Expert Profiles */}
        <ScrollArea className="w-full">
          <div
            ref={scrollRef}
            className="flex gap-4 px-4 pb-2"
          >
            {experts.map((expert) => (
              <button
                key={expert.id}
                onClick={() => onExpertClick?.(expert)}
                className={cn(
                  "flex flex-col items-center gap-1 min-w-[80px] group",
                  selectedExpertId === expert.id && "opacity-100"
                )}
              >
                <div className="relative">
                  <Avatar className="h-16 w-16 border-2 border-gray-200 group-hover:border-blue-500 transition-colors">
                    <AvatarImage src={expert.avatar} alt={expert.name} />
                    <AvatarFallback>{expert.name.slice(0, 2)}</AvatarFallback>
                  </Avatar>
                  {expert.winStreak >= 5 && (
                    <div className={cn(
                      "absolute -top-1 -right-1 h-5 w-5 rounded-full flex items-center justify-center text-white text-xs font-bold",
                      getStreakColor(expert.winStreak)
                    )}>
                      {expert.winStreak}
                    </div>
                  )}
                  {expert.isVerified && (
                    <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-blue-500 rounded-full flex items-center justify-center">
                      <svg className="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </div>
                <span className="text-xs text-gray-700 group-hover:text-blue-600 transition-colors line-clamp-1">
                  {expert.name}
                </span>
                {expert.winStreak >= 5 && (
                  <Badge 
                    variant="outline" 
                    className={cn(
                      "text-xs h-5 px-1",
                      getStreakColor(expert.winStreak),
                      "text-white border-0"
                    )}
                  >
                    {getStreakLabel(expert.winStreak)}
                  </Badge>
                )}
              </button>
            ))}
          </div>
          <ScrollBar orientation="horizontal" className="invisible" />
        </ScrollArea>
      </div>
    </div>
  )
}