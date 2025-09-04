'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  ArrowLeft, 
  Share2, 
  Heart, 
  Bookmark, 
  MessageCircle,
  CheckCircle2,
  TrendingUp,
  Calendar,
  Clock,
  Eye,
  Trophy,
  Target,
  AlertCircle,
  Users,
  RefreshCw
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface PredictionDetailPageProps {
  predictionId: string;
}

export function PredictionDetailPage({ predictionId }: PredictionDetailPageProps) {
  const router = useRouter();
  const [prediction, setPrediction] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [apiResponse, setApiResponse] = useState<any>(null);

  const fetchPredictionDetail = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Direct API URL - bypass any proxies
      const apiUrl = 'https://web-production-ccc8.up.railway.app/api/v1';
      const url = `${apiUrl}/real-matches/generate-prediction/${predictionId}`;
      
      console.log('Fetching from:', url);
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error(`API请求失败: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('API Response received:', result);
      setApiResponse(result);
      
      if (result.status === 'success' && result.data) {
        const apiData = result.data;
        
        // Extract real match info from content
        const content = apiData.content || '';
        const matchTeams = extractTeamsFromContent(content);
        
        const transformedData = {
          id: apiData.prediction_id,
          expert: {
            id: 'expert-1',
            name: apiData.expert?.name || '专家',
            avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${apiData.expert?.name || 'expert'}`,
            isVerified: true,
            badges: [
              { type: 'streak', text: '6连红' },
              { type: 'hitRate', text: '近15中13' },
            ],
            winRate: apiData.expert?.win_rate || 80,
            followerCount: 12389,
            totalPredictions: 1567,
            recentRecord: '近10中8',
          },
          confidence: apiData.confidence || 75,
          title: apiData.title || `比赛预测 #${predictionId}`,
          content: content, // Use the actual content from API
          match: {
            homeTeam: { name: matchTeams.home || 'FC首尔', logo: '🔴' },
            awayTeam: { name: matchTeams.away || '蔚山现代', logo: '🔵' },
            league: 'K联赛1',
            date: new Date().toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }),
            time: '18:00',
            venue: '体育场',
          },
          odds: {
            home: 2.28,
            draw: 3.20,
            away: 2.95,
            recommended: apiData.predicted_outcome === 'home_win' ? 'home' : 
                         apiData.predicted_outcome === 'away_win' ? 'away' : 'draw',
          },
          statistics: {
            homeTeamForm: ['W', 'W', 'D', 'W', 'W'],
            awayTeamForm: ['L', 'W', 'D', 'W', 'L'],
            h2hLast5: [],
          },
          viewCount: 2258,
          likeCount: 108,
          commentCount: 16,
          postedTime: new Date().toISOString(),
        };
        
        setPrediction(transformedData);
        console.log('Prediction set successfully. Content length:', content.length);
      } else {
        throw new Error('API返回数据格式错误');
      }
    } catch (error: any) {
      console.error('Error fetching prediction:', error);
      setError(error.message || '加载失败');
      setPrediction(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Extract team names from content
  const extractTeamsFromContent = (content: string) => {
    // Try to extract team names from the first line or title
    const lines = content.split('\n');
    for (const line of lines) {
      if (line.includes(' vs ') || line.includes(' VS ')) {
        const parts = line.split(/\s+vs\s+|\s+VS\s+/i);
        if (parts.length === 2) {
          return {
            home: parts[0].trim(),
            away: parts[1].trim()
          };
        }
      }
    }
    return { home: null, away: null };
  };

  useEffect(() => {
    fetchPredictionDetail();
  }, [predictionId]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600">正在生成专业预测分析...</p>
          <p className="text-xs text-gray-400 mt-2">从API加载数据中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">加载失败</p>
          <p className="text-sm text-gray-500 mb-4">{error}</p>
          <Button onClick={fetchPredictionDetail}>
            <RefreshCw className="h-4 w-4 mr-2" />
            重试
          </Button>
          {apiResponse && (
            <div className="mt-4 text-left max-w-2xl mx-auto">
              <details className="bg-gray-100 p-4 rounded">
                <summary className="cursor-pointer text-sm font-medium">调试信息</summary>
                <pre className="text-xs mt-2 overflow-auto">
                  {JSON.stringify(apiResponse, null, 2)}
                </pre>
              </details>
            </div>
          )}
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">无数据</p>
          <Button className="mt-4" onClick={fetchPredictionDetail}>
            <RefreshCw className="h-4 w-4 mr-2" />
            重新加载
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <div className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b">
        <div className="flex items-center justify-between p-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => router.back()}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-lg font-semibold">预测详情</h1>
          <Button variant="ghost" size="icon">
            <Share2 className="h-5 w-5" />
          </Button>
        </div>
      </div>

      <ScrollArea className="h-[calc(100vh-60px)]">
        <div className="p-4 space-y-4 pb-20">
          {/* Expert Card */}
          <Card className="p-4">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <Avatar className="h-14 w-14">
                  <AvatarImage src={prediction.expert.avatar} />
                  <AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-500 text-white">
                    {prediction.expert.name.slice(0, 2)}
                  </AvatarFallback>
                </Avatar>
                
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-lg">{prediction.expert.name}</span>
                    <CheckCircle2 className="h-5 w-5 text-blue-500" />
                  </div>
                  <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <Trophy className="h-3 w-3" />
                      胜率 {prediction.expert.winRate}%
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="h-3 w-3" />
                      {prediction.expert.followerCount} 粉丝
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Match Info Card */}
          <Card className="p-4">
            <div className="flex items-center justify-between mb-3">
              <Badge variant="secondary">{prediction.match.league}</Badge>
              <div className="text-sm text-gray-600">
                {prediction.match.date} {prediction.match.time}
              </div>
            </div>

            <div className="flex items-center justify-between mb-4">
              <div className="flex-1 text-center">
                <div className="text-3xl mb-2">{prediction.match.homeTeam.logo}</div>
                <div className="font-medium">{prediction.match.homeTeam.name}</div>
              </div>
              <div className="text-2xl font-bold text-gray-400 px-4">VS</div>
              <div className="flex-1 text-center">
                <div className="text-3xl mb-2">{prediction.match.awayTeam.logo}</div>
                <div className="font-medium">{prediction.match.awayTeam.name}</div>
              </div>
            </div>
          </Card>

          {/* Confidence Card */}
          <Card className="p-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">置信度</span>
              <span className="text-3xl font-bold text-red-500">{prediction.confidence}%</span>
            </div>
          </Card>

          {/* Analysis Content - MOST IMPORTANT */}
          <Card className="p-4">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              详细分析
            </h3>
            <div className="prose prose-sm max-w-none">
              <div className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed break-words">
                {prediction.content}
              </div>
              
              {/* Content Statistics */}
              <div className="mt-4 p-3 bg-gray-50 rounded-lg text-xs text-gray-500">
                <div>总长度: {prediction.content?.length || 0} 字符</div>
                <div>中文字数: {(prediction.content?.match(/[\u4e00-\u9fff]/g) || []).length} 字</div>
                <div>数据来源: Railway API</div>
                <div>预测ID: {prediction.id}</div>
              </div>
            </div>
          </Card>

          {/* Debug Info */}
          <Card className="p-3">
            <div className="text-xs text-gray-400">
              <div>页面加载时间: {new Date().toLocaleString('zh-CN')}</div>
              <div>Fixture ID: {predictionId}</div>
            </div>
          </Card>
        </div>
      </ScrollArea>
    </div>
  );
}