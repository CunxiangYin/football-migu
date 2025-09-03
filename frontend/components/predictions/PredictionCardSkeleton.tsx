'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export function PredictionCardSkeleton() {
  return (
    <Card className="p-4">
      {/* Expert info header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <Skeleton className="h-10 w-10 rounded-full" />
          <div className="space-y-2">
            <Skeleton className="h-4 w-24" />
            <div className="flex gap-2">
              <Skeleton className="h-5 w-16" />
              <Skeleton className="h-5 w-20" />
            </div>
          </div>
        </div>
        <Skeleton className="h-8 w-16" />
      </div>

      {/* Content */}
      <div className="space-y-2 mb-3">
        <Skeleton className="h-5 w-full" />
        <Skeleton className="h-4 w-3/4" />
      </div>

      {/* Match info */}
      <div className="flex items-center gap-2 mb-3">
        <Skeleton className="h-5 w-12" />
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-32" />
      </div>

      {/* Footer */}
      <div className="pt-3 border-t">
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Skeleton className="h-4 w-16" />
            <Skeleton className="h-4 w-20" />
          </div>
          <div className="flex gap-2">
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-8 w-8" />
            <Skeleton className="h-8 w-8" />
          </div>
        </div>
      </div>
    </Card>
  );
}