'use client';

import React from 'react';
import { FootballBettingDetail } from '@/components/football/FootballBettingDetail';
import type { MatchDetail } from '@/types/football';

// Sample data for demonstration
const sampleMatchData: MatchDetail = {
  id: '1',
  expert: {
    id: 'expert-1',
    name: '张明球评',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=expert1',
    badge: 'elite',
    followers: 128500,
    winRate: 76.8,
    predictions: 458,
    isFollowing: false,
    description: '专注欧洲五大联赛分析，擅长大小球和让球盘口预测'
  },
  match: {
    id: 'match-1',
    homeTeam: {
      id: 'team-1',
      name: '曼彻斯特城',
      logo: 'https://api.dicebear.com/7.x/shapes/svg?seed=mancity',
      shortName: '曼城'
    },
    awayTeam: {
      id: 'team-2',
      name: '利物浦',
      logo: 'https://api.dicebear.com/7.x/shapes/svg?seed=liverpool',
      shortName: '利物浦'
    },
    dateTime: '2024-03-16T20:00:00',
    league: {
      id: 'league-1',
      name: '英超联赛',
      logo: 'https://api.dicebear.com/7.x/shapes/svg?seed=premier',
      country: '英格兰'
    },
    stadium: '伊蒂哈德球场',
    round: '第29轮',
    status: 'upcoming'
  },
  betting: {
    homeWin: {
      odds: 2.15,
      probability: 45,
      recommended: true,
      change: 'up'
    },
    draw: {
      odds: 3.40,
      probability: 28,
      recommended: false,
      change: 'stable'
    },
    awayWin: {
      odds: 3.25,
      probability: 27,
      recommended: false,
      change: 'down'
    },
    confidence: 85
  },
  analysis: {
    summary: '曼城本赛季主场表现强势，11个主场比赛取得9胜2平的不败战绩。利物浦近期状态有所起伏，客场表现不如预期。两队历史交锋中，曼城在主场占据明显优势。考虑到曼城的主场优势和近期状态，本场比赛看好主队取胜。',
    keyPoints: [
      '曼城主场11战9胜2平，进球效率极高',
      '利物浦近5场客场仅2胜，防守存在问题',
      '两队近6次交锋，曼城4胜1平1负占优',
      '曼城核心球员德布劳内伤愈复出',
      '利物浦中场多名主力缺阵'
    ],
    teamForm: {
      home: {
        team: '曼城',
        last5: ['W', 'W', 'D', 'W', 'W'],
        goals: 12,
        conceded: 3
      },
      away: {
        team: '利物浦',
        last5: ['W', 'L', 'W', 'D', 'L'],
        goals: 8,
        conceded: 7
      }
    },
    h2h: [
      {
        date: '2023-12-10',
        homeTeam: '利物浦',
        awayTeam: '曼城',
        score: '1-1',
        competition: '英超'
      },
      {
        date: '2023-04-01',
        homeTeam: '曼城',
        awayTeam: '利物浦',
        score: '4-1',
        competition: '英超'
      },
      {
        date: '2022-12-22',
        homeTeam: '曼城',
        awayTeam: '利物浦',
        score: '3-2',
        competition: '联赛杯'
      },
      {
        date: '2022-10-16',
        homeTeam: '利物浦',
        awayTeam: '曼城',
        score: '1-0',
        competition: '英超'
      },
      {
        date: '2022-04-16',
        homeTeam: '曼城',
        awayTeam: '利物浦',
        score: '2-3',
        competition: '足总杯'
      }
    ],
    injuries: {
      home: ['德布劳内(疑)', '斯通斯'],
      away: ['萨拉赫', '琼斯', '巴伊切蒂奇']
    },
    prediction: {
      homeScore: 2,
      awayScore: 1,
      confidence: 78
    }
  },
  stats: {
    possession: { home: 58, away: 42 },
    shots: { home: 15, away: 11 },
    shotsOnTarget: { home: 6, away: 4 },
    corners: { home: 7, away: 4 },
    fouls: { home: 9, away: 12 },
    xG: { home: 2.1, away: 1.3 }
  },
  engagement: {
    views: 45230,
    likes: 3842,
    saves: 892,
    comments: 156,
    tips: 28,
    publishedAt: '2024-03-16T08:00:00',
    isLiked: false,
    isSaved: false
  }
};

export default function FootballDemoPage() {
  const handleBack = () => {
    console.log('Navigate back');
    // Implement navigation logic
  };

  const handleShare = () => {
    console.log('Share content');
    // Implement share logic
  };

  return (
    <div className="min-h-screen bg-background">
      <FootballBettingDetail
        data={sampleMatchData}
        onBack={handleBack}
        onShare={handleShare}
      />
    </div>
  );
}