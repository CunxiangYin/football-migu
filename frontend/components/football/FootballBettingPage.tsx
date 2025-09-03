'use client';

import React from 'react';
import { useMatchDetail } from '@/hooks/use-match-detail';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';
import {
  ArrowLeft,
  Share2,
  Heart,
  Bookmark,
  MessageCircle,
  Gift,
  TrendingUp,
  Users,
  Trophy,
  Target,
  Calendar,
  Eye,
} from 'lucide-react';

interface FootballBettingPageProps {
  matchId: string | number;
}

export function FootballBettingPage({ matchId }: FootballBettingPageProps) {
  const { matchDetail, isLoading, error, isFollowing, actions, isLiking, isSaving } = useMatchDetail(matchId);

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="p-6 max-w-md w-full">
          <p className="text-center text-red-500">加载失败，请重试</p>
          <Button 
            className="w-full mt-4" 
            onClick={() => window.location.reload()}
          >
            重新加载
          </Button>
        </Card>
      </div>
    );
  }

  if (!matchDetail) {
    return null;
  }

  const {
    home_team,
    away_team,
    league,
    match_date,
    match_time,
    expert,
    betting_odds,
    analysis,
    statistics,
    engagement,
    predictions,
  } = matchDetail;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b">
        <div className="flex items-center justify-between p-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => window.history.back()}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-lg font-semibold">赛事详情</h1>
          <Button variant="ghost" size="icon">
            <Share2 className="h-5 w-5" />
          </Button>
        </div>
      </div>

      <ScrollArea className="h-[calc(100vh-60px-60px)]">
        <div className="p-4 space-y-4 pb-20">
          {/* Expert Section */}
          {expert && (
            <Card className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="h-12 w-12">
                    <AvatarImage src={expert.avatar} />
                    <AvatarFallback className="bg-gradient-to-br from-purple-500 to-blue-500 text-white">
                      {expert.name.slice(0, 2)}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold">{expert.name}</span>
                      {expert.badges.map((badge, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {badge}
                        </Badge>
                      ))}
                    </div>
                    <div className="text-sm text-gray-500 mt-1">
                      {expert.recent_record} · 胜率{expert.win_rate}% · 连红{expert.consecutive_wins}场
                    </div>
                  </div>
                </div>
                <Button
                  size="sm"
                  variant={isFollowing ? "default" : "outline"}
                  onClick={() => expert && actions.follow(expert.id)}
                  className="min-w-[80px]"
                >
                  {isFollowing ? '已关注' : '关注'}
                </Button>
              </div>
            </Card>
          )}

          {/* Match Card */}
          <Card className="p-6">
            <div className="text-center mb-4">
              <Badge variant="secondary" className="mb-2">
                {league}
              </Badge>
              <p className="text-sm text-gray-500">
                {format(new Date(match_date), 'MM月dd日 EEEE', { locale: zhCN })} {match_time}
              </p>
            </div>

            <div className="flex items-center justify-between mb-6">
              <div className="flex-1 text-center">
                <div className="w-16 h-16 mx-auto mb-2 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
                  🔴
                </div>
                <p className="font-medium">{home_team.name}</p>
              </div>
              <div className="text-2xl font-bold text-gray-400 px-4">VS</div>
              <div className="flex-1 text-center">
                <div className="w-16 h-16 mx-auto mb-2 bg-gray-100 rounded-full flex items-center justify-center text-2xl">
                  🔵
                </div>
                <p className="font-medium">{away_team.name}</p>
              </div>
            </div>

            {/* Betting Odds */}
            {betting_odds && (
              <div className="grid grid-cols-3 gap-3">
                <Button
                  variant={betting_odds.recommended === 'home' ? 'default' : 'outline'}
                  className="flex flex-col h-auto py-3"
                >
                  <span className="text-xs opacity-80">主胜</span>
                  <span className="text-lg font-bold">{betting_odds.home_win.toFixed(2)}</span>
                </Button>
                <Button
                  variant={betting_odds.recommended === 'draw' ? 'default' : 'outline'}
                  className="flex flex-col h-auto py-3"
                >
                  <span className="text-xs opacity-80">平局</span>
                  <span className="text-lg font-bold">{betting_odds.draw.toFixed(2)}</span>
                </Button>
                <Button
                  variant={betting_odds.recommended === 'away' ? 'default' : 'outline'}
                  className="flex flex-col h-auto py-3"
                >
                  <span className="text-xs opacity-80">客胜</span>
                  <span className="text-lg font-bold">{betting_odds.away_win.toFixed(2)}</span>
                </Button>
              </div>
            )}

            {betting_odds && (
              <div className="mt-4 p-3 bg-purple-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">推荐置信度</span>
                  <span className="text-sm font-semibold">{betting_odds.confidence}%</span>
                </div>
                <Progress value={betting_odds.confidence} className="mt-2" />
              </div>
            )}
          </Card>

          {/* Analysis Tabs */}
          {analysis && (
            <Card className="p-4">
              <Tabs defaultValue="analysis" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="analysis">分析</TabsTrigger>
                  <TabsTrigger value="recent">近况</TabsTrigger>
                  <TabsTrigger value="h2h">交锋</TabsTrigger>
                  <TabsTrigger value="news">情报</TabsTrigger>
                </TabsList>

                <TabsContent value="analysis" className="space-y-4 mt-4">
                  <div className="prose prose-sm max-w-none">
                    <p className="text-gray-700 leading-relaxed">
                      {analysis.match_analysis}
                    </p>
                  </div>
                </TabsContent>

                <TabsContent value="recent" className="space-y-4 mt-4">
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium mb-2">{home_team.name}</h4>
                      <p className="text-sm text-gray-600">{analysis.recent_form.home_team}</p>
                      {statistics?.home_team_stats.recent_form && (
                        <div className="flex gap-1 mt-2">
                          {statistics.home_team_stats.recent_form.map((result, idx) => (
                            <Badge
                              key={idx}
                              variant={result === 'W' ? 'default' : result === 'D' ? 'secondary' : 'destructive'}
                              className="w-6 h-6 p-0 flex items-center justify-center"
                            >
                              {result}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                    <Separator />
                    <div>
                      <h4 className="font-medium mb-2">{away_team.name}</h4>
                      <p className="text-sm text-gray-600">{analysis.recent_form.away_team}</p>
                      {statistics?.away_team_stats.recent_form && (
                        <div className="flex gap-1 mt-2">
                          {statistics.away_team_stats.recent_form.map((result, idx) => (
                            <Badge
                              key={idx}
                              variant={result === 'W' ? 'default' : result === 'D' ? 'secondary' : 'destructive'}
                              className="w-6 h-6 p-0 flex items-center justify-center"
                            >
                              {result}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="h2h" className="space-y-2 mt-4">
                  {analysis.h2h_history.map((match, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-500">{match.date}</span>
                      <span className="text-sm font-medium">
                        {match.home_team} {match.score} {match.away_team}
                      </span>
                    </div>
                  ))}
                </TabsContent>

                <TabsContent value="news" className="space-y-4 mt-4">
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium mb-2">{home_team.name}</h4>
                      <p className="text-sm text-gray-600">{analysis.team_news.home_team}</p>
                    </div>
                    <Separator />
                    <div>
                      <h4 className="font-medium mb-2">{away_team.name}</h4>
                      <p className="text-sm text-gray-600">{analysis.team_news.away_team}</p>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </Card>
          )}

          {/* Statistics */}
          {statistics && (
            <Card className="p-4">
              <h3 className="font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                数据对比
              </h3>
              <div className="space-y-4">
                <StatRow
                  label="近期胜率"
                  homeValue={statistics.home_team_stats.win_percentage}
                  awayValue={statistics.away_team_stats.win_percentage}
                  format="percentage"
                />
                <StatRow
                  label="场均进球"
                  homeValue={statistics.home_team_stats.avg_goals_per_match}
                  awayValue={statistics.away_team_stats.avg_goals_per_match}
                  format="decimal"
                />
                <StatRow
                  label="场均失球"
                  homeValue={statistics.home_team_stats.goals_conceded / 10}
                  awayValue={statistics.away_team_stats.goals_conceded / 10}
                  format="decimal"
                />
                <StatRow
                  label="零封场次"
                  homeValue={statistics.home_team_stats.clean_sheets}
                  awayValue={statistics.away_team_stats.clean_sheets}
                  format="number"
                />
              </div>
            </Card>
          )}

          {/* Engagement Stats */}
          {engagement && (
            <Card className="p-4">
              <div className="flex items-center justify-between text-sm text-gray-500">
                <span className="flex items-center gap-1">
                  <Eye className="h-4 w-4" />
                  {engagement.views} 阅读
                </span>
                <span>{format(new Date(match_date), 'yyyy-MM-dd')}</span>
              </div>
            </Card>
          )}
        </div>
      </ScrollArea>

      {/* Bottom Action Bar */}
      {engagement && (
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4">
          <div className="flex items-center justify-around">
            <Button
              variant="ghost"
              size="sm"
              onClick={actions.like}
              disabled={isLiking}
              className={engagement.user_liked ? 'text-red-500' : ''}
            >
              <Heart className={`h-5 w-5 ${engagement.user_liked ? 'fill-current' : ''}`} />
              <span className="ml-1 text-xs">{engagement.likes}</span>
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={actions.save}
              disabled={isSaving}
              className={engagement.user_saved ? 'text-yellow-500' : ''}
            >
              <Bookmark className={`h-5 w-5 ${engagement.user_saved ? 'fill-current' : ''}`} />
            </Button>
            <Button variant="ghost" size="sm">
              <MessageCircle className="h-5 w-5" />
              <span className="ml-1 text-xs">{engagement.comments}</span>
            </Button>
            <Button variant="ghost" size="sm">
              <Gift className="h-5 w-5" />
              <span className="ml-1 text-xs">{engagement.tips}</span>
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

// Statistics Row Component
function StatRow({ 
  label, 
  homeValue, 
  awayValue, 
  format = 'number' 
}: { 
  label: string; 
  homeValue: number; 
  awayValue: number; 
  format?: 'number' | 'percentage' | 'decimal';
}) {
  const total = homeValue + awayValue || 1;
  const homePercentage = (homeValue / total) * 100;
  
  const formatValue = (value: number) => {
    switch (format) {
      case 'percentage':
        return `${value}%`;
      case 'decimal':
        return value.toFixed(1);
      default:
        return value.toString();
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="font-medium">{formatValue(homeValue)}</span>
        <span className="text-gray-500">{label}</span>
        <span className="font-medium">{formatValue(awayValue)}</span>
      </div>
      <div className="flex h-2 rounded-full overflow-hidden bg-gray-200">
        <div 
          className="bg-gradient-to-r from-purple-500 to-purple-400 transition-all duration-300"
          style={{ width: `${homePercentage}%` }}
        />
      </div>
    </div>
  );
}

// Loading Skeleton Component
function LoadingSkeleton() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 p-4">
      <div className="space-y-4">
        <Skeleton className="h-20 w-full rounded-lg" />
        <Skeleton className="h-64 w-full rounded-lg" />
        <Skeleton className="h-48 w-full rounded-lg" />
        <Skeleton className="h-32 w-full rounded-lg" />
      </div>
    </div>
  );
}