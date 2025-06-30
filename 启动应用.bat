@echo off
chcp 65001 >nul
echo 🚀 知识库问答系统启动器
echo ================================================
echo.
echo 请选择要启动的版本:
echo 1. 稳定版 (simple_web.py) - 基础功能，稳定运行
echo 2. 增强版 (simple_web_enhanced.py) - 新增图片识别功能
echo 3. 测试版 (test_image_processing.py) - 图片处理测试
echo 4. 退出
echo.

set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" goto stable
if "%choice%"=="2" goto enhanced
if "%choice%"=="3" goto test
if "%choice%"=="4" goto exit
echo 无效选择，请重新输入
goto start

:stable
echo.
echo 🎯 启动稳定版...
echo 📡 访问地址: http://localhost:8509
echo.
streamlit run simple_web.py --server.port 8509
goto start

:enhanced
echo.
echo 🚀 启动增强版...
echo 📡 访问地址: http://localhost:8509
echo 🌟 新增功能: 智能图片识别
echo.
streamlit run simple_web_enhanced.py --server.port 8509
goto start

:test
echo.
echo 🧪 启动图片处理测试...
echo 📡 访问地址: http://localhost:8501
echo.
streamlit run test_image_processing.py --server.port 8501
goto start

:exit
echo 👋 再见!
pause 