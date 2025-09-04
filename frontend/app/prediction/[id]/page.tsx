'use client';

import React from 'react';
import { PredictionDetailPage } from '@/components/predictions/PredictionDetailPageNew';

interface PageProps {
  params: {
    id: string;
  };
}

export default function PredictionPage({ params }: PageProps) {
  return <PredictionDetailPage predictionId={params.id} />;
}