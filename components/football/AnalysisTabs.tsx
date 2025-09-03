'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { 
  FileText, 
  TrendingUp, 
  Users, 
  AlertCircle,
  Target,
  CheckCircle,
  XCircle,
  MinusCircle
} from 'lucide-react';
import { cn } from '@/lib/utils';
import type { Analysis } from '@/types/football';

interface AnalysisTabsProps {
  analysis: Analysis;
  className?: string;
}

export function AnalysisTabs({ analysis, className }: AnalysisTabsProps) {
  const getFormIcon = (result: 'W' | 'D' | 'L') => {
    switch (result) {
      case 'W':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'D':
        return <MinusCircle className="h-4 w-4 text-yellow-500" />;
      case 'L':
        return <XCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const getFormColor = (result: 'W' | 'D' | 'L') => {
    switch (result) {
      case 'W':
        return 'bg-green-500';
      case 'D':
        return 'bg-yellow-500';
      case 'L':
        return 'bg-red-500';
    }
  };

  return (
    <Card className={cn("overflow-hidden", className)}>
      <Tabs defaultValue="analysis" className="w-full">
        <TabsList className="grid w-full grid-cols-4 h-10">
          <TabsTrigger value="analysis" className="text-xs gap-1">
            <FileText className="h-3 w-3" />
            分析
          </TabsTrigger>
          <TabsTrigger value="form" className="text-xs gap-1">
            <TrendingUp className="h-3 w-3" />
            近况
          </TabsTrigger>
          <TabsTrigger value="h2h" className="text-xs gap-1">
            <Users className="h-3 w-3" />
            交锋
          </TabsTrigger>
          <TabsTrigger value="news" className="text-xs gap-1">
            <AlertCircle className="h-3 w-3" />
            情报
          </TabsTrigger>
        </TabsList>

        <TabsContent value="analysis" className="p-4 space-y-4">
          <div className="space-y-3">
            <p className="text-sm leading-relaxed">
              {analysis.summary}
            </p>
            
            <div className="space-y-2">
              <h4 className="text-sm font-semibold flex items-center gap-2">
                <Target className="h-4 w-4 text-violet-500" />
                关键要点
              </h4>
              <ul className="space-y-1.5">
                {analysis.keyPoints.map((point, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <span className="text-violet-500 mt-0.5">•</span>
                    <span className="text-muted-foreground">{point}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Score Prediction */}
            <div className="mt-4 p-3 rounded-lg bg-gradient-to-r from-purple-50 to-violet-50 dark:from-purple-950/20 dark:to-violet-950/20">
              <div className="flex items-center justify-between">
                <div className="text-sm font-medium">比分预测</div>
                <Badge variant="outline" className="text-xs">
                  置信度 {analysis.prediction.confidence}%
                </Badge>
              </div>
              <div className="mt-2 flex items-center justify-center gap-4">
                <span className="text-2xl font-bold">
                  {analysis.prediction.homeScore}
                </span>
                <span className="text-lg text-muted-foreground">:</span>
                <span className="text-2xl font-bold">
                  {analysis.prediction.awayScore}
                </span>
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="form" className="p-4 space-y-4">
          {/* Home Team Form */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">主队近况</h4>
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                {analysis.teamForm.home.last5.map((result, index) => (
                  <div
                    key={index}
                    className={cn(
                      "h-6 w-6 rounded flex items-center justify-center text-white text-xs font-bold",
                      getFormColor(result)
                    )}
                  >
                    {result}
                  </div>
                ))}
              </div>
              <Separator orientation="vertical" className="h-4" />
              <div className="text-xs text-muted-foreground">
                进{analysis.teamForm.home.goals}球 失{analysis.teamForm.home.conceded}球
              </div>
            </div>
          </div>

          {/* Away Team Form */}
          <div className="space-y-2">
            <h4 className="text-sm font-semibold">客队近况</h4>
            <div className="flex items-center gap-2">
              <div className="flex gap-1">
                {analysis.teamForm.away.last5.map((result, index) => (
                  <div
                    key={index}
                    className={cn(
                      "h-6 w-6 rounded flex items-center justify-center text-white text-xs font-bold",
                      getFormColor(result)
                    )}
                  >
                    {result}
                  </div>
                ))}
              </div>
              <Separator orientation="vertical" className="h-4" />
              <div className="text-xs text-muted-foreground">
                进{analysis.teamForm.away.goals}球 失{analysis.teamForm.away.conceded}球
              </div>
            </div>
          </div>

          {/* Form Analysis */}
          <div className="mt-4 p-3 rounded-lg bg-muted/50">
            <p className="text-xs text-muted-foreground leading-relaxed">
              主队近5场{analysis.teamForm.home.last5.filter(r => r === 'W').length}胜
              {analysis.teamForm.home.last5.filter(r => r === 'D').length}平
              {analysis.teamForm.home.last5.filter(r => r === 'L').length}负，
              客队近5场{analysis.teamForm.away.last5.filter(r => r === 'W').length}胜
              {analysis.teamForm.away.last5.filter(r => r === 'D').length}平
              {analysis.teamForm.away.last5.filter(r => r === 'L').length}负。
            </p>
          </div>
        </TabsContent>

        <TabsContent value="h2h" className="p-4 space-y-3">
          <h4 className="text-sm font-semibold">历史交锋</h4>
          <div className="space-y-2">
            {analysis.h2h.map((match, index) => (
              <div 
                key={index}
                className="flex items-center justify-between p-2 rounded-lg bg-muted/30 text-xs"
              >
                <div className="flex items-center gap-2">
                  <span className="text-muted-foreground">{match.date}</span>
                  <Badge variant="outline" className="text-xs">
                    {match.competition}
                  </Badge>
                </div>
                <div className="flex items-center gap-2 font-medium">
                  <span>{match.homeTeam}</span>
                  <span className="text-violet-500 font-bold">{match.score}</span>
                  <span>{match.awayTeam}</span>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-3 p-3 rounded-lg bg-muted/50">
            <p className="text-xs text-muted-foreground">
              双方近{analysis.h2h.length}次交锋记录
            </p>
          </div>
        </TabsContent>

        <TabsContent value="news" className="p-4 space-y-4">
          {/* Injuries */}
          <div className="space-y-3">
            <h4 className="text-sm font-semibold flex items-center gap-2">
              <AlertCircle className="h-4 w-4 text-orange-500" />
              伤停情报
            </h4>
            
            <div className="space-y-3">
              {/* Home Team Injuries */}
              <div className="space-y-2">
                <div className="text-xs font-medium text-muted-foreground">主队伤停</div>
                {analysis.injuries.home.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {analysis.injuries.home.map((player, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {player}
                      </Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-muted-foreground">无重要伤停</p>
                )}
              </div>

              {/* Away Team Injuries */}
              <div className="space-y-2">
                <div className="text-xs font-medium text-muted-foreground">客队伤停</div>
                {analysis.injuries.away.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {analysis.injuries.away.map((player, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {player}
                      </Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-muted-foreground">无重要伤停</p>
                )}
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
}