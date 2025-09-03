'use client';

import { FootballBettingPage } from '@/components/football/FootballBettingPage';

interface PageProps {
  params: {
    id: string;
  };
}

export default function MatchDetailPage({ params }: PageProps) {
  const matchId = parseInt(params.id, 10);
  
  return <FootballBettingPage matchId={matchId} />;
}