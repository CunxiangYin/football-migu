'use client'

import React from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

export function PredictionCardSkeleton() {
  return (
    <Card className="mb-3">
      <CardContent className="p-4">
        {/* Expert Header Skeleton */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3 flex-1">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="flex-1">
              <Skeleton className="h-4 w-24 mb-1" />
              <div className="flex gap-1">
                <Skeleton className="h-5 w-16" />
                <Skeleton className="h-5 w-20" />
              </div>
            </div>
          </div>
          <Skeleton className="h-8 w-12" />
        </div>

        {/* Content Skeleton */}
        <div className="mb-3">
          <Skeleton className="h-4 w-full mb-1" />
          <Skeleton className="h-4 w-3/4" />
        </div>

        {/* Match Info Skeleton */}
        <div className="bg-gray-50 rounded-lg p-3 mb-3">
          <div className="flex items-center justify-between mb-2">
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-3 w-20" />
          </div>
          <div className="flex items-center justify-between">
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-3 w-8" />
            <Skeleton className="h-4 w-20" />
          </div>
        </div>

        {/* Footer Skeleton */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Skeleton className="h-3 w-12" />
            <Skeleton className="h-3 w-16" />
          </div>
          <Skeleton className="h-6 w-20" />
        </div>
      </CardContent>
    </Card>
  )
}

export function PredictionListSkeleton({ count = 3 }: { count?: number }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <PredictionCardSkeleton key={i} />
      ))}
    </>
  )
}