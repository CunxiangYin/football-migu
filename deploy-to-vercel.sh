#!/bin/bash

echo "🚀 Football-Migu Vercel 部署脚本"
echo "================================"
echo ""
echo "请先完成以下步骤："
echo "1. 在终端运行: vercel login"
echo "2. 选择 'Continue with GitHub' 并完成认证"
echo ""
read -p "已完成登录？(y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "开始部署前端..."
    cd frontend
    
    # 设置环境变量（开发环境使用本地后端）
    export NEXT_PUBLIC_API_URL="http://localhost:8000/api/v1"
    
    # 部署到 Vercel
    vercel --prod --yes
    
    echo ""
    echo "✅ 部署完成！"
    echo ""
    echo "后续步骤："
    echo "1. 访问 https://vercel.com/dashboard 查看部署状态"
    echo "2. 在 Settings → Environment Variables 中配置生产环境 API URL"
    echo "3. 后端部署到 Railway 后，更新 NEXT_PUBLIC_API_URL"
else
    echo "请先完成 Vercel 登录后再运行此脚本"
fi