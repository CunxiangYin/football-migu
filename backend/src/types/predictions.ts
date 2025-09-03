// Type definitions for expert predictions

export interface Expert {
  id: string
  name: string
  avatar: string
  isVerified: boolean
  winStreak: number
  badges: ExpertBadge[]
  followerCount: number
  predictionCount: number
  successRate: number
}

export interface ExpertBadge {
  type: 'win_streak' | 'hit_rate' | 'return_rate'
  label: string
  value: string | number
  color: 'red' | 'yellow' | 'gray'
}

export interface Prediction {
  id: string
  expert: Expert
  confidence: number
  match: MatchInfo
  content: string
  predictionType: string
  viewCount: number
  postedAt: Date
  tags: string[]
  odds?: number
}

export interface MatchInfo {
  id: string
  homeTeam: string
  awayTeam: string
  league: string
  leagueLogo?: string
  startTime: Date
  odds?: number
  score?: string
}

export type FilterType = 'hot' | 'winning_streak' | 'returns'
export type TabType = 'following' | 'football' | 'basketball' | 'traditional' | 'plans'

export interface PredictionsFilter {
  type: FilterType
  tab: TabType
  search?: string
}