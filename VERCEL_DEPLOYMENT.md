# 🚀 Vercel部署指南

## 部署架构

由于Vercel主要支持静态网站和Serverless Functions，我们需要采用混合部署策略：

1. **前端 (Next.js)** → Vercel ✅
2. **后端 (FastAPI)** → Railway/Render/Heroku 推荐

## 方案一：前端Vercel + 后端Railway（推荐）

### 1. 部署后端到Railway

Railway是一个支持Python应用的云平台，免费套餐足够测试使用。

#### 步骤：

1. 访问 [Railway](https://railway.app/)
2. 使用GitHub登录
3. 创建新项目，选择 "Deploy from GitHub repo"
4. 选择 `football-migu` 仓库
5. 添加环境变量：
```env
PORT=8000
ENVIRONMENT=production
DATABASE_URL=sqlite:///data/football_betting.db
```
6. 修改启动命令：
```bash
cd backend && pip install -r requirements.txt && python start_server.py
```
7. 部署完成后获取URL，例如：`https://football-migu.up.railway.app`

### 2. 部署前端到Vercel

#### 通过GitHub自动部署（推荐）

1. 访问 [Vercel](https://vercel.com)
2. 点击 "New Project"
3. 导入GitHub仓库 `CunxiangYin/football-migu`
4. 配置设置：
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. 添加环境变量：
   - `NEXT_PUBLIC_API_URL`: `https://football-migu.up.railway.app/api/v1`
6. 点击 "Deploy"

#### 通过CLI部署

```bash
# 安装Vercel CLI
npm i -g vercel

# 进入前端目录
cd frontend

# 部署
vercel

# 按提示操作：
# - Set up and deploy: Y
# - Which scope: 选择你的账号
# - Link to existing project: N
# - Project name: football-migu-frontend
# - Directory: ./
# - Override settings: N
```

## 方案二：前端Vercel + 后端Render

### 1. 部署后端到Render

1. 访问 [Render](https://render.com)
2. 创建新的 Web Service
3. 连接GitHub仓库
4. 配置：
   - **Name**: football-migu-api
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_server.py`
5. 添加环境变量
6. 部署

### 2. 前端部署同方案一

## 方案三：全栈Vercel（有限制）

Vercel的Serverless Functions有一些限制：
- 执行时间限制：10秒（免费版）
- 无法使用SQLite（需要外部数据库）
- 文件系统只读

如果要在Vercel部署后端，需要：

### 1. 修改数据库为PostgreSQL

使用 [Vercel Postgres](https://vercel.com/storage/postgres) 或 [Supabase](https://supabase.com)

### 2. 创建API路由

创建 `api/` 目录结构：
```
api/
├── matches/
│   └── index.py
├── predictions/
│   └── index.py
└── experts/
    └── index.py
```

### 3. 部署配置

创建 `vercel.json`：
```json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api"
    }
  ]
}
```

## 环境变量配置

### Vercel前端环境变量

在Vercel Dashboard → Settings → Environment Variables：

```env
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api/v1
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
```

### 后端环境变量（Railway/Render）

```env
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host/db  # 如果使用PostgreSQL
BACKEND_CORS_ORIGINS=["https://your-app.vercel.app"]
SECRET_KEY=your-production-secret-key
```

## 部署后配置

### 1. 更新CORS设置

编辑 `backend/main.py`：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 更新API URL

编辑 `frontend/next.config.js`：
```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/:path*',
      },
    ]
  },
}
```

## 监控和日志

### Vercel监控
- 访问：https://vercel.com/dashboard
- 查看：Functions → Logs

### Railway监控
- 访问：https://railway.app/dashboard
- 查看：Deployments → Logs

## 常见问题

### 1. CORS错误
确保后端CORS配置包含前端域名：
```python
allow_origins=["https://your-frontend.vercel.app"]
```

### 2. API连接失败
检查环境变量 `NEXT_PUBLIC_API_URL` 是否正确设置

### 3. 数据库连接问题
Vercel不支持SQLite，需要使用外部数据库服务

### 4. 构建失败
检查 `package.json` 和 `requirements.txt` 依赖是否完整

## 推荐部署组合

| 方案 | 前端 | 后端 | 数据库 | 费用 |
|------|------|------|--------|------|
| 开发测试 | Vercel | Railway | SQLite | 免费 |
| 小型生产 | Vercel | Render | PostgreSQL | ~$7/月 |
| 中型生产 | Vercel Pro | Heroku | PostgreSQL | ~$25/月 |
| 大型生产 | Vercel Enterprise | AWS/GCP | RDS | 按需 |

## 快速部署脚本

```bash
#!/bin/bash
# quick-deploy-vercel.sh

echo "🚀 Deploying to Vercel + Railway"

# Deploy backend to Railway
echo "1. Deploy backend to Railway"
echo "   Please visit: https://railway.app/new/github"
echo "   Select repository: football-migu"
echo "   Configure as Python app"
echo ""
read -p "Enter your Railway backend URL: " BACKEND_URL

# Deploy frontend to Vercel
echo "2. Deploying frontend to Vercel..."
cd frontend
vercel --prod --env NEXT_PUBLIC_API_URL=$BACKEND_URL

echo "✅ Deployment complete!"
```

## 总结

最简单的部署方案：
1. **后端** → Railway（一键部署）
2. **前端** → Vercel（自动从GitHub部署）
3. **数据库** → SQLite（开发）或 PostgreSQL（生产）

这样可以充分利用免费套餐，实现零成本部署！