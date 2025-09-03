import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api-client';

interface Team {
  id: number;
  name: string;
  logo: string;
}

interface League {
  id: number;
  name: string;
  country: string;
}

interface Match {
  fixture_id: number;
  date: string;
  venue: string;
  home_team: Team;
  away_team: Team;
  league: League;
  prediction?: {
    id: string;
    confidence: number;
    predicted_score: string;
  };
}

interface RealMatchesData {
  today: Match[];
  tomorrow: Match[];
}

interface UseRealMatchesReturn {
  matches: RealMatchesData;
  predictions: any[];
  experts: any[];
  isLoading: boolean;
  error: Error | null;
  refresh: () => Promise<void>;
  generatePrediction: (fixtureId: number) => Promise<void>;
}

export function useRealMatches(): UseRealMatchesReturn {
  const [matches, setMatches] = useState<RealMatchesData>({ today: [], tomorrow: [] });
  const [predictions, setPredictions] = useState<any[]>([]);
  const [experts, setExperts] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const loadMatches = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Fetch real matches using relative URL for Next.js proxy
      console.log('Fetching matches from API...');
      const matchesResponse = await fetch('/api/v1/real-matches/today-tomorrow').then(res => res.json());
      console.log('Matches response:', matchesResponse);
      if (matchesResponse.status === 'success') {
        setMatches(matchesResponse.data);
      }
      
      // Fetch predictions
      const predictionsResponse = await fetch('/api/v1/real-matches/predictions').then(res => res.json());
      if (predictionsResponse.status === 'success') {
        setPredictions(predictionsResponse.data);
      }
      
      // Fetch experts
      console.log('Fetching experts from API...');
      const expertsResponse = await fetch('/api/v1/real-matches/experts').then(res => res.json());
      console.log('Experts response:', expertsResponse);
      if (expertsResponse.status === 'success') {
        setExperts(expertsResponse.data);
      }
    } catch (err) {
      console.error('Failed to load real matches:', err);
      setError(err as Error);
      
      // Fallback to mock data
      setMatches({
        today: [
          {
            fixture_id: 1001,
            date: new Date().toISOString(),
            venue: '首尔世界杯竞技场',
            home_team: { id: 2750, name: 'FC首尔', logo: '' },
            away_team: { id: 2749, name: '蔚山现代', logo: '' },
            league: { id: 292, name: 'K联赛1', country: '韩国' }
          },
          {
            fixture_id: 1002,
            date: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
            venue: '埼玉2002体育场',
            home_team: { id: 302, name: '浦和红钻', logo: '' },
            away_team: { id: 303, name: '横滨水手', logo: '' },
            league: { id: 98, name: 'J联赛1', country: '日本' }
          }
        ],
        tomorrow: [
          {
            fixture_id: 1003,
            date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
            venue: '全州世界杯竞技场',
            home_team: { id: 2751, name: '全北现代', logo: '' },
            away_team: { id: 2748, name: '浦项制铁', logo: '' },
            league: { id: 292, name: 'K联赛1', country: '韩国' }
          },
          {
            fixture_id: 1004,
            date: new Date(Date.now() + 26 * 60 * 60 * 1000).toISOString(),
            venue: '日产体育场',
            home_team: { id: 279, name: '川崎前锋', logo: '' },
            away_team: { id: 285, name: '鹿岛鹿角', logo: '' },
            league: { id: 98, name: 'J联赛1', country: '日本' }
          }
        ]
      });
      
      // Add fallback experts data
      setExperts([
        {
          id: "1",
          name: "Dr. Michael Chen",
          nickname: "The Data Wizard",
          avatar_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=data_wizard",
          win_rate: 78.5,
          followers: 12340
        },
        {
          id: "2", 
          name: "Coach Roberto Silva",
          nickname: "The Tactician",
          avatar_url: "https://api.dicebear.com/7.x/avataaars/svg?seed=tactician",
          win_rate: 74.2,
          followers: 8765
        }
      ]);
    } finally {
      // Delay setting loading to false to ensure data is processed
      setTimeout(() => setIsLoading(false), 100);
    }
  };

  const generatePrediction = async (fixtureId: number) => {
    try {
      const response = await fetch(`/api/v1/real-matches/generate-prediction/${fixtureId}`, {
        method: 'POST'
      }).then(res => res.json());
      if (response.status === 'success') {
        // Refresh predictions
        await loadMatches();
      }
    } catch (err) {
      console.error('Failed to generate prediction:', err);
    }
  };

  useEffect(() => {
    loadMatches();
  }, []);

  const refresh = useCallback(async () => {
    await loadMatches();
  }, []);

  return {
    matches,
    predictions,
    experts,
    isLoading,
    error,
    refresh,
    generatePrediction,
  };
}