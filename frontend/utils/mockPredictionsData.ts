import { PredictionItem, ExpertProfile, TabType, FilterType } from '@/types/predictions';

const expertNames = [
  '老韩评球', '西西看球', '每日一推计划', '贺冠首方',
  '代红', '白羊', '内幕爆析', '鼎蜂', '皇牌', '山口组谨洋'
];

const leagues = ['日职联', '英超', '西甲', '德甲', '意甲', '法甲', '中超', '荷甲'];

const teams = [
  { name: '浦项制铁', logo: '🔴' },
  { name: '全北现代', logo: '🟢' },
  { name: '蔚山现代', logo: '🔵' },
  { name: '长崎航海', logo: '⚓' },
  { name: '山口雷诺法', logo: '🟣' },
  { name: '利物浦', logo: '🔴' },
  { name: '曼城', logo: '🔵' },
  { name: '皇家马德里', logo: '⚪' },
  { name: '巴塞罗那', logo: '🔴' },
  { name: '拜仁慕尼黑', logo: '🔴' },
];

export function generateMockExperts(): ExpertProfile[] {
  return expertNames.slice(0, 8).map((name, index) => ({
    id: `expert-${index + 1}`,
    name,
    avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`,
    winStreak: [14, 12, 10, 9, 8, 7, 6, 5][index] || 5,
    isVerified: index < 5,
    followerCount: Math.floor(Math.random() * 10000) + 1000,
    predictionCount: Math.floor(Math.random() * 500) + 100,
  }));
}

export function generateMockPredictions(
  pageSize: number,
  page: number,
  options?: {
    tab?: TabType;
    filter?: FilterType;
    expertId?: string | null;
  }
): PredictionItem[] {
  // Simulate end of data
  if (page > 5) return [];

  const predictions: PredictionItem[] = [];
  const startIndex = (page - 1) * pageSize;

  for (let i = 0; i < pageSize; i++) {
    const expertIndex = (startIndex + i) % expertNames.length;
    const teamIndices = [
      Math.floor(Math.random() * teams.length),
      Math.floor(Math.random() * teams.length)
    ];
    
    const homeTeam = teams[teamIndices[0]];
    const awayTeam = teams[teamIndices[1] === teamIndices[0] ? (teamIndices[1] + 1) % teams.length : teamIndices[1]];

    const badges = [];
    
    // Add badges based on filter
    if (options?.filter === 'streak' || Math.random() > 0.5) {
      badges.push({
        type: 'streak' as const,
        text: `${Math.floor(Math.random() * 10) + 5}连红`,
      });
    }
    
    if (options?.filter === 'returns' || Math.random() > 0.5) {
      badges.push({
        type: 'returnRate' as const,
        text: `近10场回报率${Math.floor(Math.random() * 500) + 200}%`,
      });
    }
    
    if (Math.random() > 0.5) {
      badges.push({
        type: 'hitRate' as const,
        text: `近15中${Math.floor(Math.random() * 5) + 10}`,
      });
    }

    const titles = [
      `18:00韩K1联比分推荐，浦项制铁 VS 全北现代`,
      `中日法红！比利亚富埃尔 VS 赫罗纳`,
      `火爆必杀！近10中10！状态火火火！信心推荐！`,
      `白乙+韩K+荷甲，早场组三串一`,
      `日职乙，长崎航海 VS 山口雷诺法`,
      `初始必后市玩的数盘，日本精彩小单！`,
    ];

    const descriptions = [
      '浦项制铁 vs 全北现代',
      '比利亚富埃尔 vs 赫罗纳',
      '长崎航海 vs 山口雷诺法',
      'FC东京 vs 京都不死鸟',
      '水晶宫 vs 诺丁汉森林',
      '海伦芬 vs 特温特',
    ];

    predictions.push({
      id: `prediction-${startIndex + i + 1}`,
      expert: {
        id: `expert-${expertIndex + 1}`,
        name: expertNames[expertIndex],
        avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${expertNames[expertIndex]}`,
        isVerified: expertIndex < 5,
        badges,
      },
      confidence: 100,
      title: titles[i % titles.length],
      description: descriptions[i % descriptions.length],
      match: {
        homeTeam,
        awayTeam,
        league: leagues[Math.floor(Math.random() * leagues.length)],
        time: `${Math.floor(Math.random() * 12) + 10}:${Math.random() > 0.5 ? '00' : '30'}`,
        date: `08-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
      },
      viewCount: Math.floor(Math.random() * 500) + 100,
      postedTime: new Date(Date.now() - Math.random() * 3600000 * 24).toISOString(),
      commentCount: Math.floor(Math.random() * 50),
      likeCount: Math.floor(Math.random() * 200),
      isLiked: Math.random() > 0.7,
      isSaved: Math.random() > 0.8,
    });
  }

  // Filter by expertId if provided
  if (options?.expertId) {
    return predictions.filter(p => p.expert.id === options.expertId);
  }

  return predictions;
}