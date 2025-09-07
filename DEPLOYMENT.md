# 🚀 足球预测系统 - 生产环境部署

## 部署状态 ✅

### 后端服务 (Railway)
- **状态**: ✅ 已上线
- **API地址**: https://web-production-ccc8.up.railway.app
- **API文档**: https://web-production-ccc8.up.railway.app/docs
- **健康检查**: https://web-production-ccc8.up.railway.app/

### 前端服务 (Vercel)
- **部署状态**: ✅ 已部署
- **访问地址**: 需在Vercel控制台解除认证保护
- **本地演示**: http://localhost:3000

### AI模型
- **版本**: Sonnet 4.0 (Claude 3.5 Sonnet V2)
- **模型ID**: claude-3-5-sonnet-20241022
- **状态**: ✅ 正常运行

## 功能验证

### API测试
```bash
# 生成预测
curl -X POST https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/1001

# 获取专家列表
curl https://web-production-ccc8.up.railway.app/api/v1/real-matches/experts
```

### 文章生成质量
- ✅ 字符数: 3000+ (超过1000-1500要求)
- ✅ 语言: 中文
- ✅ 内容质量: 专业详细
- ✅ 响应时间: 2-3秒

## 访问方式

### 1. API直接访问
```javascript
fetch('https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/1001', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(res => res.json())
.then(data => console.log(data));
```

### 2. 本地演示页面
1. 启动前端开发服务器:
   ```bash
   cd frontend
   npm run dev
   ```
2. 访问: http://localhost:3000/demo.html

### 3. 生产环境访问
由于Vercel有认证保护，需要：
1. 登录 [Vercel控制台](https://vercel.com)
2. 找到项目 `frontend`
3. 进入 Settings → Password Protection
4. 关闭认证保护

## 环境变量配置

### 后端 (Railway)
```env
ANTHROPIC_API_KEY=已配置
FOOTBALL_API_KEY=已配置
DATABASE_URL=已配置
```

### 前端 (Vercel)
```env
NEXT_PUBLIC_API_URL=https://web-production-ccc8.up.railway.app
```

## 监控和日志

### 后端监控
- Railway Dashboard: 查看实时日志和性能指标
- API健康检查: 每5分钟自动检查

### 前端监控
- Vercel Analytics: 查看访问统计
- 实时构建日志: Vercel Dashboard

## 故障排除

### 常见问题

1. **Vercel 401错误**
   - 原因: 项目启用了认证保护
   - 解决: 在Vercel控制台关闭Password Protection

2. **API响应慢**
   - 检查Railway服务状态
   - 查看API日志是否有错误

3. **文章生成失败**
   - 检查ANTHROPIC_API_KEY是否有效
   - 查看后端日志获取详细错误信息

## 更新部署

### 更新后端
```bash
git push origin main
# Railway会自动部署
```

### 更新前端
```bash
cd frontend
npx vercel --prod
```

## 联系信息

- GitHub仓库: https://github.com/CunxiangYin/football-migu
- Railway项目: web-production-ccc8
- Vercel项目: frontend

---

最后更新: 2024年1月
部署版本: v1.0.0
AI模型: Sonnet 4.0