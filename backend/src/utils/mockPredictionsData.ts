// Mock data generator for predictions

import { Expert, Prediction, ExpertBadge } from '@/types/predictions'

const expertNames = [
  '足彩大师', '球王预测', '红单专家', '竞彩达人', '数据分析师',
  '赢球王', '专业预测', '足球先知', '篮球专家', '综合分析'
]

const leagues = [
  { name: '英超', logo: '🏴󐁧󐁢󐁥󐁮󐁧󐁿' },
  { name: '西甲', logo: '🇪🇸' },
  { name: '德甲', logo: '🇩🇪' },
  { name: '意甲', logo: '🇮🇹' },
  { name: '法甲', logo: '🇫🇷' },
  { name: '中超', logo: '🇨🇳' },
  { name: 'NBA', logo: '🏀' },
  { name: 'CBA', logo: '🏀' }
]

const teams = {
  football: [
    '曼联', '切尔西', '利物浦', '阿森纳', '曼城',
    '皇马', '巴萨', '马竞', '拜仁', '多特蒙德',
    'AC米兰', '国际米兰', '尤文图斯', '巴黎圣日耳曼'
  ],
  basketball: [
    '湖人', '勇士', '凯尔特人', '热火', '雄鹿',
    '广东宏远', '北京首钢', '辽宁飞豹', '新疆飞虎'
  ]
}

export function generateExpertBadges(expert: Partial<Expert>): ExpertBadge[] {
  const badges: ExpertBadge[] = []
  
  if (expert.winStreak && expert.winStreak > 0) {
    badges.push({
      type: 'win_streak',
      label: `近${expert.winStreak}连红`,
      value: expert.winStreak,
      color: 'red'
    })
  }
  
  if (expert.successRate && expert.successRate > 70) {
    const recent = Math.floor(Math.random() * 10) + 10
    const hits = Math.floor(recent * expert.successRate / 100)
    badges.push({
      type: 'hit_rate',
      label: `近${recent}中${hits}`,
      value: `${hits}/${recent}`,
      color: 'yellow'
    })
  }
  
  if (Math.random() > 0.5) {
    const returnRate = Math.floor(Math.random() * 500) + 200
    badges.push({
      type: 'return_rate',
      label: `近10场回报率${returnRate}%`,
      value: `${returnRate}%`,
      color: 'gray'
    })
  }
  
  return badges
}

export function generateMockExperts(count: number = 10): Expert[] {
  return Array.from({ length: count }, (_, i) => {
    const winStreak = Math.floor(Math.random() * 15)
    const successRate = Math.floor(Math.random() * 30) + 60
    
    const expert: Partial<Expert> = {
      id: `expert-${i + 1}`,
      name: expertNames[i % expertNames.length],
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${i}`,
      isVerified: Math.random() > 0.3,
      winStreak,
      followerCount: Math.floor(Math.random() * 50000) + 1000,
      predictionCount: Math.floor(Math.random() * 1000) + 50,
      successRate
    }
    
    return {
      ...expert,
      badges: generateExpertBadges(expert)
    } as Expert
  })
}

export function generateMockPredictions(count: number = 20): Prediction[] {
  const experts = generateMockExperts(10)
  
  return Array.from({ length: count }, (_, i) => {
    const isFootball = Math.random() > 0.3
    const league = leagues[Math.floor(Math.random() * leagues.length)]
    const teamPool = isFootball ? teams.football : teams.basketball
    const homeTeam = teamPool[Math.floor(Math.random() * teamPool.length)]
    let awayTeam = teamPool[Math.floor(Math.random() * teamPool.length)]
    while (awayTeam === homeTeam) {
      awayTeam = teamPool[Math.floor(Math.random() * teamPool.length)]
    }
    
    const now = new Date()
    const matchTime = new Date(now.getTime() + Math.random() * 7 * 24 * 60 * 60 * 1000)
    const postedTime = new Date(now.getTime() - Math.random() * 24 * 60 * 60 * 1000)
    
    return {
      id: `prediction-${i + 1}`,
      expert: experts[Math.floor(Math.random() * experts.length)],
      confidence: Math.floor(Math.random() * 30) + 70,
      match: {
        id: `match-${i + 1}`,
        homeTeam,
        awayTeam,
        league: league.name,
        leagueLogo: league.logo,
        startTime: matchTime,
        odds: Math.random() * 3 + 1.5
      },
      content: `专业分析：${homeTeam} VS ${awayTeam}，根据近期状态和历史交锋记录，推荐本场比赛...`,
      predictionType: ['胜负', '让球', '大小球', '比分'][Math.floor(Math.random() * 4)],
      viewCount: Math.floor(Math.random() * 10000) + 100,
      postedAt: postedTime,
      tags: [league.name, '精选', '高赔率'].slice(0, Math.floor(Math.random() * 3) + 1)
    }
  })
}

export function getTimeAgo(date: Date): string {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

export function formatMatchTime(date: Date): string {
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  
  return `${month}-${day} ${hours}:${minutes}`
}

export function formatViewCount(count: number): string {
  if (count >= 10000) {
    return `${(count / 10000).toFixed(1)}万`
  }
  if (count >= 1000) {
    return `${(count / 1000).toFixed(1)}k`
  }
  return count.toString()
}