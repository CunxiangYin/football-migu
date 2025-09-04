# 🚀 后端部署指南

## 已完成的准备工作

✅ **所有配置文件已准备就绪：**
- `railway.json` - Railway 部署配置
- `Procfile` - 启动命令配置  
- `requirements.txt` - Python 依赖
- CORS 配置已更新，支持从环境变量读取
- PORT 配置已更新，支持动态端口

## 📋 Railway 部署步骤

### 方法 1：通过 GitHub 部署（推荐）

1. **访问 Railway**
   ```
   https://railway.app
   ```

2. **登录/注册**
   - 点击 "Start a New Project"
   - 使用 GitHub 账号登录

3. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 授权 Railway 访问你的 GitHub（如果首次使用）
   - 搜索并选择 `football-migu` 仓库

4. **配置会自动应用**
   Railway 会自动检测并使用以下文件：
   - `railway.json` - 构建和部署配置
   - `Procfile` - 启动命令
   - `requirements.txt` - Python 依赖

5. **环境变量（已在 railway.json 中配置）**
   ```json
   {
     "HOST": "0.0.0.0",
     "PORT": "${{PORT}}",  // Railway 自动分配
     "ENVIRONMENT": "production",
     "DATABASE_URL": "sqlite:///data/football_betting.db",
     "BACKEND_CORS_ORIGINS": "[\"https://frontend-pgpuj3b3f-jasonyins-projects.vercel.app\", \"http://localhost:3000\"]"
   }
   ```

6. **部署完成后获取 URL**
   部署成功后，Railway 会提供一个公开 URL，例如：
   ```
   https://football-migu-production.up.railway.app
   ```

### 方法 2：通过 Railway Dashboard 手动配置

如果自动部署失败，可以手动配置：

1. **创建空项目**
   - 在 Railway Dashboard 创建 "Empty Project"

2. **添加 GitHub 仓库**
   - Settings → Connect to GitHub
   - 选择 `football-migu` 仓库

3. **配置构建设置**
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python start_server.py`

4. **添加环境变量**
   在 Variables 标签页添加：
   - `HOST`: `0.0.0.0`
   - `ENVIRONMENT`: `production`
   - `DATABASE_URL`: `sqlite:///data/football_betting.db`
   - `BACKEND_CORS_ORIGINS`: `["https://frontend-pgpuj3b3f-jasonyins-projects.vercel.app", "http://localhost:3000"]`

5. **生成域名**
   - Settings → Domains
   - 点击 "Generate Domain"

## 🔄 更新前端配置

部署成功后，需要更新 Vercel 前端的 API URL：

1. **访问 Vercel Dashboard**
   ```
   https://vercel.com/jasonyins-projects/frontend/settings/environment-variables
   ```

2. **更新环境变量**
   - 编辑 `NEXT_PUBLIC_API_URL`
   - 新值：`https://your-railway-url.railway.app/api/v1`
   - 例如：`https://football-migu-production.up.railway.app/api/v1`

3. **重新部署前端**
   ```bash
   vercel --prod --yes
   ```

## 🎯 备选部署平台

如果 Railway 不可用，可以选择：

### Render.com
1. 访问 https://render.com
2. New → Web Service
3. 连接 GitHub 仓库
4. 配置：
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start_server.py`

### Heroku
1. 需要创建 `runtime.txt` 指定 Python 版本
2. 使用 Heroku CLI 或 GitHub 集成部署

### Fly.io
1. 安装 flyctl CLI
2. 运行 `fly launch` 在项目目录
3. 配置 fly.toml

## ✅ 验证部署

部署完成后，访问以下端点验证：

- **健康检查**: `https://your-backend-url/health`
- **API 文档**: `https://your-backend-url/docs`
- **根路径**: `https://your-backend-url/`

## 🐛 故障排查

### 常见问题：

1. **端口绑定错误**
   - 确保使用环境变量 `PORT`
   - Railway 会自动分配端口

2. **CORS 错误**
   - 检查 `BACKEND_CORS_ORIGINS` 包含前端 URL
   - 确保 JSON 格式正确

3. **数据库错误**
   - SQLite 文件会自动创建
   - 确保有写入权限

4. **依赖安装失败**
   - 检查 requirements.txt 格式
   - 确保所有包版本兼容

## 📝 完整部署清单

- [x] railway.json 配置文件
- [x] Procfile 启动文件
- [x] requirements.txt 依赖文件
- [x] CORS 动态配置
- [x] PORT 动态配置
- [ ] 部署到 Railway
- [ ] 获取后端 URL
- [ ] 更新前端环境变量
- [ ] 验证 API 端点

---

**当前 Vercel 前端 URL**: https://frontend-pgpuj3b3f-jasonyins-projects.vercel.app

**等待你的 Railway 后端 URL 来完成集成！**