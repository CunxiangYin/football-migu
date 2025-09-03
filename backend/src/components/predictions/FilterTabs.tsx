'use client'

import React from 'react'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { FilterType } from '@/types/predictions'

interface FilterTabsProps {
  activeFilter: FilterType
  onFilterChange: (filter: FilterType) => void
}

export function FilterTabs({ activeFilter, onFilterChange }: FilterTabsProps) {
  const filters: { value: FilterType; label: string }[] = [
    { value: 'hot', label: '热门' },
    { value: 'winning_streak', label: '连红' },
    { value: 'returns', label: '回报' }
  ]

  return (
    <div className="bg-white px-4 py-2 border-b">
      <Tabs value={activeFilter} onValueChange={(value) => onFilterChange(value as FilterType)}>
        <TabsList className="grid w-full max-w-sm grid-cols-3 h-9">
          {filters.map((filter) => (
            <TabsTrigger
              key={filter.value}
              value={filter.value}
              className="data-[state=active]:bg-blue-500 data-[state=active]:text-white"
            >
              {filter.label}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
    </div>
  )
}