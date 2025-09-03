'use client'

import React from 'react'
import { Eye, TrendingUp, Trophy, Clock, ChevronRight } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Prediction } from '@/types/predictions'
import { formatMatchTime, formatViewCount, getTimeAgo } from '@/utils/mockPredictionsData'
import { cn } from '@/lib/utils'

interface PredictionCardProps {
  prediction: Prediction
  onCardClick?: () => void
  onExpertClick?: () => void
}

export function PredictionCard({ 
  prediction, 
  onCardClick,
  onExpertClick 
}: PredictionCardProps) {
  const { expert, confidence, match, viewCount, postedAt, tags } = prediction

  const getBadgeStyles = (type: string) => {
    switch (type) {
      case 'win_streak':
        return 'bg-red-500 text-white border-0'
      case 'hit_rate':
        return 'bg-yellow-500 text-white border-0'
      case 'return_rate':
        return 'bg-gray-500 text-white border-0'
      default:
        return ''
    }
  }

  const getConfidenceColor = (conf: number) => {
    if (conf >= 90) return 'text-red-600'
    if (conf >= 80) return 'text-orange-500'
    if (conf >= 70) return 'text-yellow-600'
    return 'text-gray-600'
  }

  return (
    <Card className="mb-3 overflow-hidden hover:shadow-md transition-shadow cursor-pointer">
      <CardContent className="p-4" onClick={onCardClick}>
        {/* Expert Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3 flex-1" onClick={(e) => {
            e.stopPropagation()
            onExpertClick?.()
          }}>
            <div className="relative">
              <Avatar className="h-10 w-10 border-2 border-gray-200">
                <AvatarImage src={expert.avatar} alt={expert.name} />
                <AvatarFallback>{expert.name.slice(0, 2)}</AvatarFallback>
              </Avatar>
              {expert.isVerified && (
                <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-blue-500 rounded-full flex items-center justify-center">
                  <svg className="h-3 w-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-medium text-sm">{expert.name}</span>
                <div className="flex gap-1">
                  {expert.badges.slice(0, 2).map((badge, index) => (
                    <Badge
                      key={index}
                      variant="outline"
                      className={cn("text-xs h-5 px-1", getBadgeStyles(badge.type))}
                    >
                      {badge.label}
                    </Badge>
                  ))}
                </div>
              </div>
              {expert.badges.length > 2 && (
                <div className="flex gap-1">
                  {expert.badges.slice(2).map((badge, index) => (
                    <Badge
                      key={index}
                      variant="outline"
                      className={cn("text-xs h-5 px-1", getBadgeStyles(badge.type))}
                    >
                      {badge.label}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
          </div>
          
          {/* Confidence Indicator */}
          <div className={cn("text-2xl font-bold", getConfidenceColor(confidence))}>
            {confidence}%
          </div>
        </div>

        {/* Prediction Content */}
        <div className="mb-3">
          <p className="text-sm text-gray-700 line-clamp-2">
            {prediction.content}
          </p>
        </div>

        {/* Match Info */}
        <div className="bg-gray-50 rounded-lg p-3 mb-3">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-xl">{match.leagueLogo}</span>
              <span className="font-medium text-sm">{match.league}</span>
            </div>
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <Clock className="h-3 w-3" />
              <span>{formatMatchTime(match.startTime)}</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">{match.homeTeam}</span>
            <span className="text-xs text-gray-500">VS</span>
            <span className="text-sm font-medium">{match.awayTeam}</span>
          </div>
        </div>

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex gap-2 mb-3">
            {tags.map((tag, index) => (
              <Badge key={index} variant="secondary" className="text-xs">
                {tag}
              </Badge>
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1">
              <Eye className="h-3 w-3" />
              <span>{formatViewCount(viewCount)}</span>
            </div>
            <span>{getTimeAgo(postedAt)}</span>
          </div>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-blue-500">
            查看详情
            <ChevronRight className="h-3 w-3 ml-1" />
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}