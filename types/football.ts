// Football Betting Detail Type Definitions

export interface Team {
  id: string;
  name: string;
  logo: string;
  shortName?: string;
}

export interface League {
  id: string;
  name: string;
  logo: string;
  country?: string;
}

export interface Expert {
  id: string;
  name: string;
  avatar: string;
  badge: 'verified' | 'pro' | 'elite';
  followers: number;
  winRate: number;
  predictions: number;
  isFollowing: boolean;
  description?: string;
}

export interface Match {
  id: string;
  homeTeam: Team;
  awayTeam: Team;
  dateTime: string;
  league: League;
  stadium: string;
  round?: string;
  status: 'upcoming' | 'live' | 'finished';
}

export interface OddsOption {
  odds: number;
  probability: number;
  recommended: boolean;
  change?: 'up' | 'down' | 'stable';
}

export interface BettingOdds {
  homeWin: OddsOption;
  draw: OddsOption;
  awayWin: OddsOption;
  confidence: number; // 0-100
}

export interface TeamForm {
  team: string;
  last5: ('W' | 'D' | 'L')[];
  goals: number;
  conceded: number;
}

export interface H2HMatch {
  date: string;
  homeTeam: string;
  awayTeam: string;
  score: string;
  competition: string;
}

export interface Analysis {
  summary: string;
  keyPoints: string[];
  teamForm: {
    home: TeamForm;
    away: TeamForm;
  };
  h2h: H2HMatch[];
  injuries: {
    home: string[];
    away: string[];
  };
  prediction: {
    homeScore: number;
    awayScore: number;
    confidence: number;
  };
}

export interface Statistics {
  possession: { home: number; away: number };
  shots: { home: number; away: number };
  shotsOnTarget: { home: number; away: number };
  corners: { home: number; away: number };
  fouls: { home: number; away: number };
  xG: { home: number; away: number };
}

export interface Engagement {
  views: number;
  likes: number;
  saves: number;
  comments: number;
  tips: number;
  publishedAt: string;
  isLiked: boolean;
  isSaved: boolean;
}

export interface MatchDetail {
  id: string;
  expert: Expert;
  match: Match;
  betting: BettingOdds;
  analysis: Analysis;
  stats: Statistics;
  engagement: Engagement;
}