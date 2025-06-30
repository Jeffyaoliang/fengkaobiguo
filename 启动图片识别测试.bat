@echo off
chcp 65001 >nul
echo 🖼️ 图片识别功能测试启动器
echo ================================================
echo.
echo 选择要启动的应用:
echo 1. 主应用 (simple_web.py) - 完整功能
echo 2. 图片处理测试 (test_image_processing.py) - 专门测试图片功能
echo 3. 退出
echo.

set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" goto main_app
if "%choice%"=="2" goto test_app
if "%choice%"=="3" goto exit
echo 无效选择，请重新输入
goto start

:main_app
echo.
echo 🚀 启动主应用...
echo 📡 访问地址: http://localhost:8509
echo.
streamlit run simple_web.py --server.port 8509
goto start

:test_app
echo.
echo 🧪 启动图片处理测试...
echo 📡 访问地址: http://localhost:8501
echo.
streamlit run test_image_processing.py --server.port 8501
goto start

:exit
echo 👋 再见!
pause 