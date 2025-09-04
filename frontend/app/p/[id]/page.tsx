'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, RefreshCw, AlertCircle } from 'lucide-react';

interface PageProps {
  params: {
    id: string;
  };
}

export default function NewPredictionPage({ params }: PageProps) {
  const router = useRouter();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<any>({});

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Direct API call - no proxy
        const url = `https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/${params.id}`;
        console.log('Fetching from:', url);
        
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API Response:', data);
        
        if (data.status === 'success' && data.data) {
          const apiContent = data.data.content || '';
          setContent(apiContent);
          
          // Calculate stats
          const chineseChars = (apiContent.match(/[\u4e00-\u9fff]/g) || []).length;
          setStats({
            totalLength: apiContent.length,
            chineseCount: chineseChars,
            predictionId: data.data.prediction_id,
            title: data.data.title,
            expert: data.data.expert?.name,
            confidence: data.data.confidence
          });
        } else {
          throw new Error('Invalid API response');
        }
      } catch (err: any) {
        console.error('Error:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, [params.id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p>加载中...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="p-6 max-w-md">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <p className="text-center mb-4">加载失败: {error}</p>
          <Button onClick={() => window.location.reload()} className="w-full">
            <RefreshCw className="h-4 w-4 mr-2" />
            重试
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <Button variant="ghost" onClick={() => router.back()}>
            <ArrowLeft className="h-5 w-5 mr-2" />
            返回
          </Button>
          <h1 className="text-lg font-semibold">预测详情 (新版)</h1>
          <div className="w-20"></div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="bg-blue-50 border-b">
        <div className="container mx-auto px-4 py-3">
          <div className="flex flex-wrap gap-4 text-sm">
            <span>预测ID: <strong>{stats.predictionId}</strong></span>
            <span>专家: <strong>{stats.expert}</strong></span>
            <span>置信度: <strong>{stats.confidence}%</strong></span>
            <span className="text-green-600">
              文章长度: <strong>{stats.totalLength} 字符</strong>
            </span>
            <span className="text-blue-600">
              中文字数: <strong>{stats.chineseCount} 字</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-6">
        <Card className="p-6">
          <h2 className="text-xl font-bold mb-4">{stats.title || '比赛预测'}</h2>
          
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {content}
            </div>
          </div>

          {/* Footer Stats */}
          <div className="mt-6 pt-4 border-t text-xs text-gray-500">
            <p>本页面直接从Railway API获取数据，无任何缓存或mock数据</p>
            <p>Fixture ID: {params.id}</p>
            <p>加载时间: {new Date().toLocaleString('zh-CN')}</p>
          </div>
        </Card>
      </div>
    </div>
  );
}