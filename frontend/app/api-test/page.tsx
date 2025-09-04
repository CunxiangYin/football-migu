'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export default function ApiTestPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const testApi = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Direct API call
      const response = await fetch('https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/1001', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getChineseCharCount = (text: string) => {
    return (text?.match(/[\u4e00-\u9fff]/g) || []).length;
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">API 测试页面</h1>
      
      <Card className="p-4 mb-4">
        <p className="mb-2">直接测试Railway API:</p>
        <p className="text-sm text-gray-600 mb-4">
          https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/1001
        </p>
        <Button onClick={testApi} disabled={loading}>
          {loading ? '加载中...' : '测试 API'}
        </Button>
      </Card>

      {error && (
        <Card className="p-4 mb-4 bg-red-50">
          <h2 className="font-bold text-red-700 mb-2">错误</h2>
          <p className="text-red-600">{error}</p>
        </Card>
      )}

      {result && (
        <Card className="p-4">
          <h2 className="font-bold mb-4">API 响应</h2>
          
          {result.status === 'success' && result.data ? (
            <>
              <div className="bg-green-50 p-3 rounded mb-4">
                <p className="text-green-700 font-bold mb-2">✓ 成功获取数据</p>
                <div className="space-y-1 text-sm">
                  <p>预测ID: {result.data.prediction_id}</p>
                  <p>标题: {result.data.title}</p>
                  <p>专家: {result.data.expert?.name}</p>
                  <p>置信度: {result.data.confidence}%</p>
                  <p className="font-bold text-lg">
                    文章长度: {result.data.content?.length || 0} 字符
                  </p>
                  <p className="font-bold text-lg text-blue-600">
                    中文字数: {getChineseCharCount(result.data.content)} 字
                  </p>
                </div>
              </div>

              <div className="border-t pt-4">
                <h3 className="font-bold mb-2">文章内容预览（前500字符）:</h3>
                <div className="bg-gray-50 p-3 rounded text-sm whitespace-pre-wrap">
                  {result.data.content?.substring(0, 500)}...
                </div>
              </div>

              <div className="border-t pt-4 mt-4">
                <h3 className="font-bold mb-2">文章内容预览（后500字符）:</h3>
                <div className="bg-gray-50 p-3 rounded text-sm whitespace-pre-wrap">
                  ...{result.data.content?.substring(result.data.content.length - 500)}
                </div>
              </div>
            </>
          ) : (
            <div className="text-red-600">
              <p>API返回了意外的格式</p>
              <pre className="text-xs mt-2 bg-gray-100 p-2 rounded overflow-auto">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}