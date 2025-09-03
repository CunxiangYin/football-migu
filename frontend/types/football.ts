export interface Expert {
  id: number;
  name: string;
  avatar?: string;
  badges: string[];
  recent_record: string;
  win_rate: number;
  consecutive_wins: number;
  follower_count: number;
  is_following?: boolean;
}

export interface Team {
  id: string;
  name: string;
  logo?: string;
  logo_url?: string;
  short_name?: string;
  code?: string;
  country?: string;
}

export interface Match {
  id: string;
  home_team: Team;
  away_team: Team;
  league: string;
  league_name?: string;
  match_date: string;
  match_time: string;
  kickoff_time?: string;
  status: 'upcoming' | 'live' | 'finished' | 'scheduled';
}

export interface BettingOdds {
  home_win: number;
  draw: number;
  away_win: number;
  recommended: 'home' | 'draw' | 'away';
  confidence: number;
}

export interface Analysis {
  match_analysis: string;
  recent_form: {
    home_team: string;
    away_team: string;
  };
  h2h_history: Array<{
    date: string;
    home_team: string;
    away_team: string;
    score: string;
  }>;
  team_news: {
    home_team: string;
    away_team: string;
  };
  score_prediction: string;
}

export interface Statistics {
  home_team_stats: {
    recent_form: string[];
    goals_scored: number;
    goals_conceded: number;
    clean_sheets: number;
    btts_percentage: number;
    avg_goals_per_match: number;
    win_percentage: number;
  };
  away_team_stats: {
    recent_form: string[];
    goals_scored: number;
    goals_conceded: number;
    clean_sheets: number;
    btts_percentage: number;
    avg_goals_per_match: number;
    win_percentage: number;
  };
}

export interface Engagement {
  views: number;
  likes: number;
  comments: number;
  tips: number;
  user_liked?: boolean;
  user_saved?: boolean;
}

export interface MatchDetail extends Match {
  expert?: Expert;
  betting_odds?: BettingOdds;
  analysis?: Analysis;
  statistics?: Statistics;
  engagement?: Engagement;
  predictions?: Array<{
    expert: Expert;
    prediction: string;
    confidence: number;
    reasoning: string;
  }>;
}