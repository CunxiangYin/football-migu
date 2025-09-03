# Expert Predictions List Page Design Document

## Overview
Create a comprehensive expert predictions list page for displaying sports betting predictions from verified experts, featuring expert profiles, prediction cards, and filtering capabilities.

## Component Architecture

### 1. Main Components
- `ExpertPredictionsPage` - Main page container
- `ExpertProfilesSection` - Horizontal scrolling expert profiles
- `PredictionCard` - Individual prediction card component
- `FilterTabs` - Tab-based filtering system
- `PageHeader` - Header with navigation and promotion banner

### 2. Data Models

```typescript
interface Expert {
  id: string
  name: string
  avatar: string
  isVerified: boolean
  winStreak: number
  badges: ExpertBadge[]
  followerCount: number
}

interface ExpertBadge {
  type: 'win_streak' | 'hit_rate' | 'return_rate'
  label: string
  value: string | number
  color: 'red' | 'yellow' | 'gray'
}

interface Prediction {
  id: string
  expert: Expert
  confidence: number
  match: MatchInfo
  content: string
  viewCount: number
  postedAt: Date
  tags: string[]
}

interface MatchInfo {
  id: string
  homeTeam: string
  awayTeam: string
  league: string
  startTime: Date
  odds?: number
}
```

### 3. Features
- **Horizontal Expert Profiles**: Scrollable expert avatars with win streak badges
- **Filter System**: Hot, Winning Streak, Returns filters
- **Prediction Cards**: Rich content cards with expert info and match details
- **Infinite Scroll**: Load more predictions as user scrolls
- **Pull to Refresh**: Refresh predictions list
- **Responsive Design**: Mobile-first approach

### 4. UI Components from shadcn/ui
- `Card`, `CardContent`, `CardHeader` - For prediction cards
- `Avatar`, `AvatarImage`, `AvatarFallback` - For expert profiles
- `Badge` - For expert badges and tags
- `Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` - For navigation and filters
- `ScrollArea` - For horizontal scrolling
- `Button` - For action buttons
- `Skeleton` - For loading states

### 5. State Management
- Use React hooks for local state
- Implement custom hooks for data fetching
- Use React Query or SWR for server state management

### 6. Performance Optimizations
- Virtualized list for large datasets
- Image lazy loading
- Memoization for expensive computations
- Debounced scroll handlers

### 7. Styling Approach
- Tailwind CSS for utility classes
- CSS variables for theming
- Consistent spacing using Tailwind's spacing scale
- Mobile-first responsive design

## Implementation Plan
1. Set up page structure and routing
2. Create data models and mock data generator
3. Implement expert profiles section
4. Build prediction card component
5. Add filtering and sorting logic
6. Implement infinite scroll and pull-to-refresh
7. Add loading and error states
8. Optimize performance and accessibility