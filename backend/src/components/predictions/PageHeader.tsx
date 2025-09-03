'use client'

import React from 'react'
import { Bell, ChevronRight, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { TabType } from '@/types/predictions'

interface PageHeaderProps {
  activeTab: TabType
  onTabChange: (tab: TabType) => void
  showBanner?: boolean
  onCloseBanner?: () => void
}

export function PageHeader({ 
  activeTab, 
  onTabChange, 
  showBanner = true,
  onCloseBanner 
}: PageHeaderProps) {
  const tabs: { value: TabType; label: string }[] = [
    { value: 'following', label: '关注' },
    { value: 'football', label: '足球' },
    { value: 'basketball', label: '篮球' },
    { value: 'traditional', label: '传统' },
    { value: 'plans', label: '计划' }
  ]

  return (
    <div className="sticky top-0 z-40 bg-white shadow-sm">
      {/* Title Bar */}
      <div className="flex items-center justify-between px-4 py-3 border-b">
        <h1 className="text-lg font-semibold">彩经中心-结果预测</h1>
        <Button variant="ghost" size="icon">
          <Bell className="h-5 w-5" />
        </Button>
      </div>

      {/* Promotion Banner */}
      {showBanner && (
        <div className="relative bg-blue-500 text-white px-4 py-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 flex-1">
              <span className="text-sm">下载APP，获取更多专家预测</span>
              <ChevronRight className="h-4 w-4" />
            </div>
            {onCloseBanner && (
              <Button
                variant="ghost"
                size="icon"
                className="h-6 w-6 text-white hover:bg-blue-600"
                onClick={onCloseBanner}
              >
                <X className="h-4 w-4" />
              </Button>
            )}
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <Tabs value={activeTab} onValueChange={(value) => onTabChange(value as TabType)}>
        <TabsList className="w-full justify-start rounded-none h-12 bg-white border-b">
          {tabs.map((tab) => (
            <TabsTrigger
              key={tab.value}
              value={tab.value}
              className="flex-1 data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-blue-500 rounded-none"
            >
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
    </div>
  )
}