export interface ExpertProfile {
  id: string;
  name: string;
  avatar: string;
  winStreak: number;
  isVerified: boolean;
  followerCount: number;
  predictionCount: number;
}

export interface PredictionBadge {
  type: 'streak' | 'hitRate' | 'returnRate';
  text: string;
  value?: string;
}

export interface TeamInfo {
  name: string;
  logo?: string;
}

export interface PredictionItem {
  id: string;
  expert: {
    id: string;
    name: string;
    avatar: string;
    isVerified: boolean;
    badges: PredictionBadge[];
  };
  confidence: number;
  title: string;
  description: string;
  match: {
    homeTeam: TeamInfo;
    awayTeam: TeamInfo;
    league: string;
    time: string;
    date: string;
  };
  viewCount: number;
  postedTime: string;
  commentCount: number;
  likeCount: number;
  isLiked?: boolean;
  isSaved?: boolean;
}

export type TabType = 'following' | 'football' | 'basketball' | 'traditional' | 'plans';
export type FilterType = 'hot' | 'streak' | 'returns';