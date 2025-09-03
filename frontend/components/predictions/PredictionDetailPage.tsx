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
  Users
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

interface PredictionDetailPageProps {
  predictionId: string;
}

// Mock data for demonstration
const mockPredictionDetail = {
  id: 'prediction-1',
  expert: {
    id: 'expert-1',
    name: '老韩评球',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=老韩评球',
    isVerified: true,
    badges: [
      { type: 'streak', text: '6连红' },
      { type: 'hitRate', text: '近15中13' },
    ],
    winRate: 86.7,
    followerCount: 12389,
    totalPredictions: 1567,
    recentRecord: '近10中8',
  },
  confidence: 100,
  title: '18:00韩K1联比分推荐，浦项制铁 VS 全北现代',
  content: `浦项制铁 vs 全北现代

【基本面分析】
浦项制铁本赛季表现稳定，目前联赛排名第3，主场战绩出色。最近5个主场比赛4胜1平保持不败，展现出强大的主场统治力。球队进攻火力充足，场均进球达到2.1个，防守端也相对稳固。

全北现代作为K联赛传统豪门，本赛季状态有所起伏，目前排名第5。客场表现一般，最近5个客场2胜1平2负。球队最近遭遇伤病困扰，主力中场金英权因伤缺阵，对球队中场控制力有一定影响。

【历史交锋】
两队最近10次交锋，浦项制铁3胜3平4负略处下风。但在主场对阵全北现代的最近5场比赛中，浦项制铁取得3胜2平保持不败，心理优势明显。

【盘口分析】
亚盘开出浦项制铁主让半球高水，后市水位有所下调。考虑到浦项制铁的主场优势和全北现代的客场表现，此盘口较为合理。欧赔方面，主胜赔率持续下调，显示市场对主队信心增强。

【推荐】
综合分析，本场比赛看好浦项制铁主场取胜。
推荐：浦项制铁 -0.5
比分推荐：2-1`,
  match: {
    homeTeam: { name: '浦项制铁', logo: '🔴' },
    awayTeam: { name: '全北现代', logo: '🟢' },
    league: '韩K1联',
    date: '08-27',
    time: '18:00',
    venue: '浦项钢铁体育场',
  },
  odds: {
    home: 2.28,
    draw: 3.20,
    away: 2.95,
    recommended: 'home',
  },
  statistics: {
    homeTeamForm: ['W', 'W', 'D', 'W', 'W'],
    awayTeamForm: ['L', 'W', 'D', 'W', 'L'],
    h2hLast5: [
      { date: '2024-05-15', home: '浦项制铁', away: '全北现代', score: '2-1' },
      { date: '2024-03-20', home: '全北现代', away: '浦项制铁', score: '1-1' },
      { date: '2023-11-08', home: '浦项制铁', away: '全北现代', score: '3-2' },
      { date: '2023-08-15', home: '全北现代', away: '浦项制铁', score: '2-0' },
      { date: '2023-05-10', home: '浦项制铁', away: '全北现代', score: '1-1' },
    ],
  },
  viewCount: 2258,
  likeCount: 108,
  commentCount: 16,
  postedTime: new Date(Date.now() - 6 * 3600 * 1000).toISOString(),
  isLiked: false,
  isSaved: false,
  isFollowing: false,
};

export function PredictionDetailPage({ predictionId }: PredictionDetailPageProps) {
  const router = useRouter();
  const [prediction, setPrediction] = useState<any>(null);
  const [isFollowing, setIsFollowing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchPredictionDetail = async () => {
      try {
        setIsLoading(true);
        // Fetch prediction from API
        const response = await fetch(`/api/v1/real-matches/generate-prediction/${predictionId}`, {
          method: 'POST',
        });
        
        if (!response.ok) {
          throw new Error('Failed to fetch prediction');
        }
        
        const result = await response.json();
        console.log('API Response:', result);
        console.log('Content length from API:', result.data?.content?.length);
        
        if (result.status === 'success' && result.data) {
          // Transform API response to match component structure
          const apiData = result.data;
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
            content: apiData.content || '生成中...',
            match: {
              homeTeam: { name: 'FC首尔', logo: '🔴' },
              awayTeam: { name: '蔚山现代', logo: '🔵' },
              league: 'K联赛1',
              date: new Date().toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }),
              time: '18:00',
              venue: '首尔世界杯竞技场',
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
              h2hLast5: mockPredictionDetail.statistics.h2hLast5,
            },
            viewCount: 2258,
            likeCount: 108,
            commentCount: 16,
            postedTime: new Date().toISOString(),
            isLiked: false,
            isSaved: false,
            isFollowing: false,
          };
          
          setPrediction(transformedData);
          setIsFollowing(false);
        } else {
          // Fallback to mock data if API fails
          setPrediction(mockPredictionDetail);
          setIsFollowing(mockPredictionDetail.isFollowing);
        }
      } catch (error) {
        console.error('Error fetching prediction:', error);
        // Fallback to mock data
        setPrediction(mockPredictionDetail);
        setIsFollowing(mockPredictionDetail.isFollowing);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPredictionDetail();
  }, [predictionId]);

  const handleFollow = () => {
    setIsFollowing(!isFollowing);
  };

  const handleLike = () => {
    setPrediction(prev => ({
      ...prev,
      isLiked: !prev.isLiked,
      likeCount: prev.isLiked ? prev.likeCount - 1 : prev.likeCount + 1,
    }));
  };

  const handleSave = () => {
    setPrediction(prev => ({
      ...prev,
      isSaved: !prev.isSaved,
    }));
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600">正在生成专业预测分析...</p>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">无法加载预测内容</p>
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

      <ScrollArea className="h-[calc(100vh-60px-60px)]">
        <div className="p-4 space-y-4 pb-20">
          {/* Expert Card */}
          <Card className="p-4">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Avatar className="h-14 w-14">
                    <AvatarImage src={prediction.expert.avatar} />
                    <AvatarFallback className="bg-gradient-to-br from-purple-500 to-pink-500 text-white">
                      {prediction.expert.name.slice(0, 2)}
                    </AvatarFallback>
                  </Avatar>
                  {prediction.expert.isVerified && (
                    <CheckCircle2 className="absolute -bottom-1 -right-1 h-5 w-5 text-blue-500 bg-white rounded-full" />
                  )}
                </div>
                
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-lg">{prediction.expert.name}</span>
                    {prediction.expert.badges.map((badge, idx) => (
                      <Badge
                        key={idx}
                        className={cn(
                          "text-xs",
                          badge.type === 'streak' ? 'bg-red-500' : 'bg-yellow-500',
                          'text-white'
                        )}
                      >
                        {badge.text}
                      </Badge>
                    ))}
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

              <Button
                size="sm"
                variant={isFollowing ? "default" : "outline"}
                onClick={handleFollow}
              >
                {isFollowing ? '已关注' : '关注'}
              </Button>
            </div>

            <Separator className="my-3" />

            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-purple-600">
                  {prediction.expert.totalPredictions}
                </div>
                <div className="text-xs text-gray-500">总预测</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">
                  {prediction.expert.winRate}%
                </div>
                <div className="text-xs text-gray-500">命中率</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-red-600">
                  {prediction.expert.recentRecord}
                </div>
                <div className="text-xs text-gray-500">近期战绩</div>
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

            <div className="text-center text-sm text-gray-500">
              <Calendar className="inline-block h-3 w-3 mr-1" />
              {prediction.match.venue}
            </div>
          </Card>

          {/* Odds Card */}
          <Card className="p-4">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Target className="h-4 w-4" />
              推荐投注
            </h3>
            <div className="grid grid-cols-3 gap-3">
              <Button
                variant={prediction.odds.recommended === 'home' ? 'default' : 'outline'}
                className="flex flex-col h-auto py-3"
                disabled
              >
                <span className="text-xs opacity-80">主胜</span>
                <span className="text-lg font-bold">{prediction.odds.home}</span>
              </Button>
              <Button
                variant={prediction.odds.recommended === 'draw' ? 'default' : 'outline'}
                className="flex flex-col h-auto py-3"
                disabled
              >
                <span className="text-xs opacity-80">平局</span>
                <span className="text-lg font-bold">{prediction.odds.draw}</span>
              </Button>
              <Button
                variant={prediction.odds.recommended === 'away' ? 'default' : 'outline'}
                className="flex flex-col h-auto py-3"
                disabled
              >
                <span className="text-xs opacity-80">客胜</span>
                <span className="text-lg font-bold">{prediction.odds.away}</span>
              </Button>
            </div>
            <div className="mt-3 p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">置信度</span>
                <span className="text-2xl font-bold text-red-500">{prediction.confidence}%</span>
              </div>
            </div>
          </Card>

          {/* Analysis Content */}
          <Card className="p-4">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              详细分析
            </h3>
            <div className="prose prose-sm max-w-none">
              <div className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed break-words">
                {prediction.content}
              </div>
              {/* Display content length for debugging */}
              <div className="mt-4 text-xs text-gray-400 border-t pt-2">
                文章长度: {prediction.content?.length || 0} 字符
              </div>
            </div>
          </Card>

          {/* Recent Form */}
          <Card className="p-4">
            <h3 className="font-semibold mb-3">近期状态</h3>
            <div className="space-y-3">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{prediction.match.homeTeam.name}</span>
                  <div className="flex gap-1">
                    {prediction.statistics.homeTeamForm.map((result, idx) => (
                      <Badge
                        key={idx}
                        variant={result === 'W' ? 'default' : result === 'D' ? 'secondary' : 'destructive'}
                        className="w-6 h-6 p-0 flex items-center justify-center"
                      >
                        {result}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
              <Separator />
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">{prediction.match.awayTeam.name}</span>
                  <div className="flex gap-1">
                    {prediction.statistics.awayTeamForm.map((result, idx) => (
                      <Badge
                        key={idx}
                        variant={result === 'W' ? 'default' : result === 'D' ? 'secondary' : 'destructive'}
                        className="w-6 h-6 p-0 flex items-center justify-center"
                      >
                        {result}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* H2H History */}
          <Card className="p-4">
            <h3 className="font-semibold mb-3">历史交锋</h3>
            <div className="space-y-2">
              {prediction.statistics.h2hLast5.map((match, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                  <span className="text-xs text-gray-500">{match.date}</span>
                  <span className="text-sm font-medium">
                    {match.home} {match.score} {match.away}
                  </span>
                </div>
              ))}
            </div>
          </Card>

          {/* Footer Stats */}
          <Card className="p-3">
            <div className="flex items-center justify-between text-sm text-gray-500">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {format(new Date(prediction.postedTime), 'MM-dd HH:mm')}
                </span>
                <span className="flex items-center gap-1">
                  <Eye className="h-3 w-3" />
                  {prediction.viewCount} 阅读
                </span>
              </div>
            </div>
          </Card>
        </div>
      </ScrollArea>

      {/* Bottom Action Bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-4">
        <div className="flex items-center justify-around">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleLike}
            className={prediction.isLiked ? 'text-red-500' : ''}
          >
            <Heart className={cn("h-5 w-5", prediction.isLiked && "fill-current")} />
            <span className="ml-1">{prediction.likeCount}</span>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleSave}
            className={prediction.isSaved ? 'text-yellow-500' : ''}
          >
            <Bookmark className={cn("h-5 w-5", prediction.isSaved && "fill-current")} />
          </Button>
          <Button variant="ghost" size="sm">
            <MessageCircle className="h-5 w-5" />
            <span className="ml-1">{prediction.commentCount}</span>
          </Button>
          <Button variant="default" className="px-6">
            立即投注
          </Button>
        </div>
      </div>
    </div>
  );
}