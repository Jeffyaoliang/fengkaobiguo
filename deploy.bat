@echo off
chcp 65001 >nul
echo 🚀 知识库大模型问答系统 - 快速部署脚本
echo ================================================

:menu
echo.
echo 请选择部署方式:
echo 1. 本地启动 (推荐)
echo 2. 局域网启动
echo 3. Docker部署
echo 4. 云服务器部署指南
echo 5. 退出
echo.

set /p choice=请输入选择 (1-5): 

if "%choice%"=="1" goto local
if "%choice%"=="2" goto network
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto cloud
if "%choice%"=="5" goto exit
echo 无效选择，请重新输入
goto menu

:local
echo.
echo 🌐 启动本地服务...
echo 📡 访问地址: http://localhost:8509
echo.
streamlit run simple_web.py --server.port 8509
goto menu

:network
echo.
echo 🌐 启动局域网服务...
echo 📡 本地访问: http://localhost:8509
echo 📡 局域网访问: http://%COMPUTERNAME%:8509
echo.
streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
goto menu

:docker
echo.
echo 🐳 检查Docker是否安装...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安装，请先安装Docker Desktop
    echo 📖 下载地址: https://www.docker.com/products/docker-desktop
    goto menu
)

echo ✅ Docker已安装
echo 🏗️  构建Docker镜像...
docker build -t qa-system .

echo 🚀 启动Docker容器...
echo 📡 访问地址: http://localhost:8509
docker run -p 8509:8509 qa-system
goto menu

:cloud
echo.
echo ☁️  云服务器部署指南
echo ================================================
echo 1. 购买云服务器 (推荐阿里云/腾讯云/华为云)
echo 2. 连接服务器 (SSH)
echo 3. 安装Python和依赖:
echo    sudo apt update
echo    sudo apt install python3 python3-pip
echo    pip3 install -r requirements.txt
echo 4. 启动服务:
echo    streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
echo 5. 配置安全组开放8509端口
echo 6. 访问: http://服务器IP:8509
echo.
echo 📖 详细教程: https://docs.streamlit.io/deploy/streamlit-community-cloud
echo ================================================
pause
goto menu

:exit
echo 👋 再见!
pause 