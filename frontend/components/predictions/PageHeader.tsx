'use client';

import React, { useState } from 'react';
import { TabType } from '@/types/predictions';
import { Button } from '@/components/ui/button';
import { X, ChevronLeft, Search, MoreVertical } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PageHeaderProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export function PageHeader({ activeTab, onTabChange }: PageHeaderProps) {
  const [showBanner, setShowBanner] = useState(true);

  const tabs: { key: TabType; label: string; badge?: string }[] = [
    { key: 'following', label: '关注' },
    { key: 'football', label: '足球' },
    { key: 'basketball', label: '篮球' },
    { key: 'traditional', label: '传统' },
    { key: 'plans', label: '计划' },
  ];

  return (
    <div className="sticky top-0 z-40 bg-white border-b">
      {/* App promotion banner */}
      {showBanner && (
        <div className="bg-blue-500 text-white px-4 py-2 flex items-center justify-between">
          <div className="flex items-center gap-2 flex-1">
            <div className="w-6 h-6 bg-white/20 rounded flex items-center justify-center">
              <span className="text-xs font-bold">V</span>
            </div>
            <p className="text-sm flex-1">
              本产品由VVApp提供 平台仅发布内容不提供彩票服务
            </p>
          </div>
          <button
            onClick={() => setShowBanner(false)}
            className="p-1 hover:bg-white/10 rounded"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Main header */}
      <div className="px-4 py-3">
        <div className="flex items-center justify-between mb-3">
          <button 
            className="p-1"
            onClick={() => window.location.href = '/coming-soon?feature=返回功能'}
          >
            <ChevronLeft className="h-6 w-6" />
          </button>
          <h1 className="text-lg font-semibold">彩经中心-结果预测</h1>
          <div className="flex items-center gap-2">
            <button 
              className="p-1"
              onClick={() => window.location.href = '/coming-soon?feature=搜索功能'}
            >
              <Search className="h-5 w-5" />
            </button>
            <button 
              className="p-1"
              onClick={() => window.location.href = '/coming-soon?feature=更多选项'}
            >
              <MoreVertical className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Tab navigation */}
        <div className="flex items-center gap-6 overflow-x-auto scrollbar-hide">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => {
                if (tab.key === 'football') {
                  onTabChange(tab.key);
                } else {
                  window.location.href = `/coming-soon?feature=${encodeURIComponent(tab.label + '预测')}`;
                }
              }}
              className={cn(
                "pb-2 px-1 relative whitespace-nowrap transition-colors",
                activeTab === tab.key
                  ? "text-blue-500 font-semibold"
                  : "text-gray-600"
              )}
            >
              <span className="flex items-center gap-1">
                {tab.label}
                {tab.badge && (
                  <span className="bg-red-500 text-white text-xs px-1 rounded">
                    {tab.badge}
                  </span>
                )}
              </span>
              {activeTab === tab.key && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500" />
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}