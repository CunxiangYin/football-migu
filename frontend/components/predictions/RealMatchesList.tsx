'use client';

import React from 'react';
import { useRealMatches } from '@/hooks/useRealMatches';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Calendar, Clock, MapPin, TrendingUp, Users } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

export function RealMatchesList() {
  const { matches, predictions, experts, isLoading, error, generatePrediction } = useRealMatches();
  const router = useRouter();
  
  // Debug logging
  console.log('RealMatchesList render:', { isLoading, error, matches, experts });

  const formatMatchTime = (dateString: string) => {
    const date = new Date(dateString);
    return format(date, 'HH:mm', { locale: zhCN });
  };

  const formatMatchDate = (dateString: string) => {
    const date = new Date(dateString);
    return format(date, 'MM月dd日', { locale: zhCN });
  };

  const handleMatchClick = async (match: any) => {
    // Generate prediction for this match
    await generatePrediction(match.fixture_id);
    // Navigate to prediction detail
    router.push(`/prediction/${match.fixture_id}`);
  };

  // Show loading only for initial load
  if (isLoading && matches.today.length === 0 && matches.tomorrow.length === 0) {
    return (
      <div className="space-y-4 px-4">
        <div className="text-center py-4 text-sm text-gray-500">
          正在加载真实比赛数据...
        </div>
        {[1, 2, 3].map(i => (
          <Card key={i} className="p-4">
            <Skeleton className="h-20 w-full" />
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 text-gray-500">
        加载比赛数据失败，请稍后重试
      </div>
    );
  }

  const renderMatchCard = (match: any) => {
    const matchTime = new Date(match.date);
    const isLive = false; // You can add live match detection logic here
    const hasStarted = matchTime < new Date();

    return (
      <Card
        key={match.fixture_id}
        className="p-4 mb-4 cursor-pointer hover:shadow-lg transition-shadow"
        onClick={() => handleMatchClick(match)}
      >
        <div className="flex items-center justify-between mb-3">
          <Badge variant={match.league.country === '韩国' ? 'default' : 'secondary'}>
            {match.league.name}
          </Badge>
          <div className="flex items-center text-sm text-gray-500">
            <Clock className="h-3 w-3 mr-1" />
            {formatMatchTime(match.date)}
          </div>
        </div>

        <div className="flex items-center justify-between mb-3">
          <div className="flex-1 text-center">
            <div className="font-semibold text-lg">{match.home_team.name}</div>
            <div className="text-sm text-gray-500 mt-1">主场</div>
          </div>
          
          <div className="px-4">
            <div className="text-2xl font-bold text-gray-400">VS</div>
            {isLive && (
              <Badge variant="destructive" className="mt-1">
                进行中
              </Badge>
            )}
          </div>
          
          <div className="flex-1 text-center">
            <div className="font-semibold text-lg">{match.away_team.name}</div>
            <div className="text-sm text-gray-500 mt-1">客场</div>
          </div>
        </div>

        <div className="flex items-center justify-between text-sm text-gray-500">
          <div className="flex items-center">
            <MapPin className="h-3 w-3 mr-1" />
            {match.venue}
          </div>
          <Button size="sm" variant="ghost">
            <TrendingUp className="h-3 w-3 mr-1" />
            查看预测
          </Button>
        </div>
      </Card>
    );
  };

  return (
    <div className="pb-20">

      <div className="px-4">
        {/* Today's Matches */}
        {matches.today.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center mb-3">
            <Calendar className="h-4 w-4 mr-2 text-primary" />
            <h3 className="font-semibold text-lg">今日比赛</h3>
            <Badge variant="outline" className="ml-2">
              {matches.today.length}场
            </Badge>
          </div>
          {matches.today.map(renderMatchCard)}
        </div>
      )}

      {/* Tomorrow's Matches */}
      {matches.tomorrow.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center mb-3">
            <Calendar className="h-4 w-4 mr-2 text-primary" />
            <h3 className="font-semibold text-lg">明日比赛</h3>
            <Badge variant="outline" className="ml-2">
              {matches.tomorrow.length}场
            </Badge>
          </div>
          {matches.tomorrow.map(renderMatchCard)}
        </div>
      )}

      {/* Recent Predictions */}
      {predictions.length > 0 && (
        <div className="mb-6">
          <div className="flex items-center mb-3">
            <TrendingUp className="h-4 w-4 mr-2 text-primary" />
            <h3 className="font-semibold text-lg">最新预测</h3>
          </div>
          <div className="space-y-3">
            {predictions.slice(0, 5).map((pred: any) => (
              <Card
                key={pred.id}
                className="p-3 cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => window.location.href = '/coming-soon?feature=最新预测'}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="font-medium">{pred.title}</div>
                    <div className="text-sm text-gray-500 mt-1">
                      {pred.expert.name} · 准确率 {pred.expert.accuracy}%
                    </div>
                  </div>
                  <Badge variant={pred.confidence > 80 ? 'default' : 'secondary'}>
                    置信度 {pred.confidence}%
                  </Badge>
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

        {matches.today.length === 0 && matches.tomorrow.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <Users className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>暂无比赛数据</p>
          </div>
        )}
      </div>
    </div>
  );
}