# 🚀 部署指南 - Football Prediction System

## 快速部署

### 方式1：Docker部署（推荐）

```bash
# 1. 克隆代码
git clone https://github.com/your-username/football-migu.git
cd football-migu

# 2. 修改配置
# 编辑 docker-compose.yml，更新域名和环境变量

# 3. 启动服务
docker-compose up -d

# 4. 查看状态
docker-compose ps
```

### 方式2：使用部署脚本

```bash
# 给脚本执行权限
chmod +x deploy.sh

# Docker部署
./deploy.sh docker

# 或 PM2部署
./deploy.sh pm2

# 或 Systemd部署
./deploy.sh systemd
```

## 服务器要求

- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Debian 10+
- **内存**: 最少 2GB RAM
- **CPU**: 2核心以上
- **存储**: 10GB 可用空间
- **Python**: 3.9+
- **Node.js**: 18+
- **开放端口**: 80, 443, 8000, 3000

## 详细部署步骤

### 1. 准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y git curl wget nginx

# 安装 Docker (如果使用Docker部署)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 Python
sudo apt install -y python3.9 python3-pip python3-venv

# 安装 PM2 (如果使用PM2部署)
sudo npm install -g pm2
```

### 2. 配置防火墙

```bash
# UFW防火墙配置
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 8000/tcp  # Backend API
sudo ufw allow 3000/tcp  # Frontend (开发时)
sudo ufw enable
```

### 3. 配置环境变量

#### 后端配置 (backend/.env.production)
```env
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
DATABASE_URL=sqlite:///football_betting.db
SECRET_KEY=your-strong-secret-key-here
BACKEND_CORS_ORIGINS=["http://your-domain.com", "https://your-domain.com"]
```

#### 前端配置 (frontend/.env.production)
```env
NEXT_PUBLIC_API_URL=http://your-domain.com/api/v1
NEXT_PUBLIC_APP_URL=http://your-domain.com
```

### 4. 配置Nginx

```bash
# 编辑Nginx配置
sudo nano /etc/nginx/sites-available/football

# 添加以下内容（修改your-domain.com为你的域名）
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # API代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 前端代理
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/football /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL证书配置（HTTPS）

```bash
# 安装 Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo systemctl enable certbot.timer
```

## 部署方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| Docker | 环境隔离，易于管理 | 需要Docker知识 | 推荐生产环境 |
| PM2 | 进程管理方便，自动重启 | 需要手动配置环境 | 中小型部署 |
| Systemd | 系统级服务，稳定 | 配置较复杂 | 传统部署 |

## 监控和维护

### 查看日志

```bash
# Docker日志
docker-compose logs -f backend
docker-compose logs -f frontend

# PM2日志
pm2 logs football-backend
pm2 logs football-frontend

# Systemd日志
sudo journalctl -u football-backend -f
sudo journalctl -u football-frontend -f
```

### 重启服务

```bash
# Docker
docker-compose restart

# PM2
pm2 restart all

# Systemd
sudo systemctl restart football-backend
sudo systemctl restart football-frontend
```

### 备份数据

```bash
# 备份数据库
cp backend/football_betting.db backup/football_betting_$(date +%Y%m%d).db

# 备份整个项目
tar -czf football-backup-$(date +%Y%m%d).tar.gz football-migu/
```

## 性能优化

### 1. 启用Gzip压缩

在nginx.conf中添加：
```nginx
gzip on;
gzip_types text/plain application/json application/javascript text/css;
```

### 2. 配置缓存

前端静态资源缓存：
```nginx
location /_next/static {
    expires 365d;
    add_header Cache-Control "public, immutable";
}
```

### 3. 数据库优化

考虑迁移到PostgreSQL或MySQL：
```python
# backend/.env.production
DATABASE_URL=postgresql://user:pass@localhost/football_db
```

## 故障排查

### 问题1：端口被占用
```bash
# 查看端口占用
sudo lsof -i :8000
sudo lsof -i :3000

# 结束进程
sudo kill -9 <PID>
```

### 问题2：权限错误
```bash
# 修复权限
sudo chown -R $USER:$USER /path/to/football-migu
chmod +x deploy.sh
chmod +x start.sh
```

### 问题3：依赖安装失败
```bash
# 清理缓存
npm cache clean --force
pip cache purge

# 重新安装
rm -rf node_modules package-lock.json
npm install

rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 安全建议

1. **修改默认密钥**: 更新所有配置文件中的SECRET_KEY
2. **限制CORS**: 配置正确的CORS允许域名
3. **使用HTTPS**: 配置SSL证书
4. **定期更新**: 保持系统和依赖包更新
5. **备份策略**: 定期备份数据库和配置文件
6. **监控告警**: 设置系统监控和异常告警

## 联系支持

如遇到问题，请查看：
- 项目文档: README.md
- API文档: http://your-domain.com/docs
- GitHub Issues: https://github.com/your-username/football-migu/issues