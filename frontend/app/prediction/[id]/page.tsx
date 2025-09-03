'use client';

import React from 'react';
import { PredictionDetailPage } from '@/components/predictions/PredictionDetailPage';

interface PageProps {
  params: {
    id: string;
  };
}

export default function PredictionPage({ params }: PageProps) {
  return <PredictionDetailPage predictionId={params.id} />;
}