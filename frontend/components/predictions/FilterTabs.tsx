'use client';

import React from 'react';
import { FilterType } from '@/types/predictions';
import { cn } from '@/lib/utils';

interface FilterTabsProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
}

export function FilterTabs({ activeFilter, onFilterChange }: FilterTabsProps) {
  const filters: { key: FilterType; label: string }[] = [
    { key: 'hot', label: '热门' },
    { key: 'streak', label: '连红' },
    { key: 'returns', label: '回报' },
  ];

  return (
    <div className="bg-white border-b px-4 py-2">
      <div className="flex items-center gap-4">
        {filters.map((filter) => (
          <button
            key={filter.key}
            onClick={() => onFilterChange(filter.key)}
            className={cn(
              "px-4 py-1.5 rounded-full text-sm font-medium transition-all",
              activeFilter === filter.key
                ? "bg-blue-500 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            )}
          >
            {filter.label}
          </button>
        ))}
      </div>
    </div>
  );
}