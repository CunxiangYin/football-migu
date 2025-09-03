# 足球赛事分析系统

一个完整的足球赛事预测和分析系统，包含前端展示和后端API服务。

## 🚀 技术栈

### 前端
- **Next.js 14** - React框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **shadcn/ui** - UI组件库
- **React Query** - 数据获取和状态管理
- **Axios** - HTTP客户端

### 后端
- **FastAPI** - Python Web框架
- **SQLAlchemy** - ORM
- **SQLite** - 数据库（开发环境）
- **Pydantic** - 数据验证

## 📁 项目结构

```
football-migu/
├── backend/                # 后端服务
│   ├── main.py            # FastAPI应用入口
│   ├── models/             # 数据库模型
│   ├── schemas/            # Pydantic模式
│   ├── services/           # 业务逻辑
│   ├── api/               # API路由
│   └── requirements.txt   # Python依赖
├── frontend/              # 前端应用
│   ├── app/              # Next.js应用目录
│   ├── components/       # React组件
│   ├── lib/             # 工具函数和API客户端
│   ├── types/           # TypeScript类型定义
│   └── package.json     # Node依赖
└── start.sh            # 一键启动脚本
```

## 🛠️ 安装和运行

### 快速启动（推荐）

```bash
# 赋予执行权限
chmod +x start.sh

# 一键启动前后端服务
./start.sh
```

### 手动启动

#### 后端服务

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python start_server.py
```

后端服务将运行在 http://localhost:8000

#### 前端服务

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将运行在 http://localhost:3000

## 📚 API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎯 主要功能

### 用户端功能
- 📊 **赛事列表** - 查看即将进行的比赛
- 🔍 **赛事详情** - 深入了解比赛信息
- 💰 **投注赔率** - 实时赔率展示
- 📈 **数据分析** - 球队数据对比
- 👨‍💼 **专家预测** - 专业分析师推荐
- 📜 **历史交锋** - 往期对战记录
- 💬 **互动功能** - 点赞、收藏、评论

### 数据特性
- 实时数据更新
- 乐观UI更新
- 响应式设计
- 数据缓存优化

## 🔧 开发命令

### 前端
```bash
npm run dev        # 开发模式
npm run build      # 构建生产版本
npm run start      # 运行生产版本
npm run lint       # 代码检查
```

### 后端
```bash
python main.py              # 启动服务器
python seed_simple.py       # 填充测试数据
pytest tests/              # 运行测试
```

## 📱 移动端优化

- 完全响应式设计
- 触摸友好的交互
- 优化的移动端性能
- PWA支持（可安装为应用）

## 🌐 环境变量

### 前端 (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 后端 (.env)
```
DATABASE_URL=sqlite:///./football.db
SECRET_KEY=your-secret-key
```

## 📦 部署

### 使用Docker

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up
```

### 传统部署

1. 后端：使用Gunicorn + Nginx
2. 前端：使用Vercel或Netlify

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

MIT License

## 👥 联系方式

如有问题或建议，请创建Issue或联系开发团队。

---

**注意**: 本系统仅供学习和参考使用，不构成任何投资建议。