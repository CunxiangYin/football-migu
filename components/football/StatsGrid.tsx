'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { 
  Activity, 
  Target, 
  TrendingUp,
  Crosshair,
  Flag,
  AlertTriangle
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Statistics } from '@/types/football';

interface StatsGridProps {
  stats: Statistics;
  className?: string;
}

interface StatItemProps {
  icon: React.ReactNode;
  label: string;
  homeValue: number;
  awayValue: number;
  unit?: string;
  showPercentage?: boolean;
}

function StatItem({ 
  icon, 
  label, 
  homeValue, 
  awayValue, 
  unit = '',
  showPercentage = false 
}: StatItemProps) {
  const total = homeValue + awayValue;
  const homePercentage = total > 0 ? (homeValue / total) * 100 : 50;
  const awayPercentage = total > 0 ? (awayValue / total) * 100 : 50;

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        {icon}
        <span>{label}</span>
      </div>
      
      <div className="flex items-center justify-between text-sm font-semibold">
        <span>{homeValue}{unit}</span>
        <span>{awayValue}{unit}</span>
      </div>
      
      {showPercentage && (
        <div className="flex h-2 w-full overflow-hidden rounded-full bg-muted">
          <div 
            className="bg-blue-500 transition-all"
            style={{ width: `${homePercentage}%` }}
          />
          <div 
            className="bg-red-500 transition-all"
            style={{ width: `${awayPercentage}%` }}
          />
        </div>
      )}
    </div>
  );
}

export function StatsGrid({ stats, className }: StatsGridProps) {
  const statItems = [
    {
      icon: <Activity className="h-3 w-3" />,
      label: '控球率',
      homeValue: stats.possession.home,
      awayValue: stats.possession.away,
      unit: '%',
      showPercentage: true
    },
    {
      icon: <Target className="h-3 w-3" />,
      label: '射门',
      homeValue: stats.shots.home,
      awayValue: stats.shots.away,
      showPercentage: true
    },
    {
      icon: <Crosshair className="h-3 w-3" />,
      label: '射正',
      homeValue: stats.shotsOnTarget.home,
      awayValue: stats.shotsOnTarget.away,
      showPercentage: true
    },
    {
      icon: <Flag className="h-3 w-3" />,
      label: '角球',
      homeValue: stats.corners.home,
      awayValue: stats.corners.away,
      showPercentage: true
    },
    {
      icon: <AlertTriangle className="h-3 w-3" />,
      label: '犯规',
      homeValue: stats.fouls.home,
      awayValue: stats.fouls.away,
      showPercentage: true
    },
    {
      icon: <TrendingUp className="h-3 w-3" />,
      label: '预期进球',
      homeValue: stats.xG.home,
      awayValue: stats.xG.away,
      unit: '',
      showPercentage: true
    }
  ];

  return (
    <Card className={cn("overflow-hidden", className)}>
      <CardHeader className="pb-3">
        <CardTitle className="text-base">数据统计</CardTitle>
      </CardHeader>
      <CardContent className="pb-4">
        <div className="grid grid-cols-2 gap-4">
          {statItems.map((item, index) => (
            <StatItem
              key={index}
              icon={item.icon}
              label={item.label}
              homeValue={item.homeValue}
              awayValue={item.awayValue}
              unit={item.unit}
              showPercentage={item.showPercentage}
            />
          ))}
        </div>

        {/* Summary */}
        <div className="mt-4 p-3 rounded-lg bg-gradient-to-r from-blue-50 to-red-50 dark:from-blue-950/20 dark:to-red-950/20">
          <div className="flex items-center justify-between text-xs">
            <span className="font-medium text-blue-600 dark:text-blue-400">主队</span>
            <span className="text-muted-foreground">综合数据对比</span>
            <span className="font-medium text-red-600 dark:text-red-400">客队</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}