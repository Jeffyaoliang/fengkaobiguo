#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公网访问工具 - 多种方式启动公网访问
"""

import subprocess
import sys
import time
import requests
import socket
from pathlib import Path

def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_port(port):
    """检查端口是否被占用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def start_streamlit():
    """启动Streamlit应用"""
    print("🚀 启动Streamlit应用...")
    if check_port(8509):
        print("⚠️  端口8509已被占用，尝试使用8501...")
        port = 8501
    else:
        port = 8509
    
    cmd = f"streamlit run simple_web.py --server.port {port} --server.address 0.0.0.0"
    print(f"📡 启动命令: {cmd}")
    print(f"🌐 本地访问: http://localhost:{port}")
    print(f"🌐 局域网访问: http://{get_local_ip()}:{port}")
    
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n⏹️  应用已停止")

def show_access_options():
    """显示访问选项"""
    print("\n" + "="*50)
    print("🌐 公网访问方式选择")
    print("="*50)
    print("1. 本地访问 (localhost)")
    print("2. 局域网访问 (同一网络)")
    print("3. 使用ngrok (需要注册)")
    print("4. 使用Cloudflare Tunnel (推荐)")
    print("5. 使用localtunnel (免费)")
    print("6. 使用serveo (免费)")
    print("7. 使用playit.gg (游戏隧道)")
    print("8. 使用frp (自建服务器)")
    print("="*50)

def install_localtunnel():
    """安装localtunnel"""
    print("📦 安装localtunnel...")
    try:
        subprocess.run("npm install -g localtunnel", shell=True, check=True)
        print("✅ localtunnel安装成功")
        return True
    except:
        print("❌ localtunnel安装失败，请先安装Node.js")
        return False

def start_localtunnel(port=8509):
    """启动localtunnel"""
    print("🚀 启动localtunnel...")
    cmd = f"lt --port {port}"
    print(f"📡 命令: {cmd}")
    try:
        subprocess.run(cmd, shell=True)
    except KeyboardInterrupt:
        print("\n⏹️  localtunnel已停止")

def show_manual_setup():
    """显示手动设置说明"""
    print("\n" + "="*50)
    print("🔧 手动设置公网访问")
    print("="*50)
    print("1. 路由器端口转发:")
    print("   - 登录路由器管理界面")
    print("   - 找到端口转发设置")
    print("   - 添加规则: 外部端口8509 -> 内部IP:端口8509")
    print("   - 获取公网IP: https://whatismyipaddress.com/")
    print("   - 访问: http://公网IP:8509")
    print()
    print("2. 云服务器部署:")
    print("   - 购买云服务器 (阿里云/腾讯云/华为云)")
    print("   - 上传项目文件")
    print("   - 安装依赖: pip install -r requirements.txt")
    print("   - 启动: streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0")
    print("   - 配置安全组开放8509端口")
    print()
    print("3. 使用Docker部署:")
    print("   - 创建Dockerfile")
    print("   - 构建镜像: docker build -t qa-system .")
    print("   - 运行容器: docker run -p 8509:8509 qa-system")
    print("="*50)

def main():
    """主函数"""
    print("🎯 知识库大模型问答系统 - 公网访问工具")
    print("="*50)
    
    # 检查必要文件
    if not Path("simple_web.py").exists():
        print("❌ 找不到simple_web.py文件")
        return
    
    show_access_options()
    
    while True:
        choice = input("\n请选择访问方式 (1-8, q退出): ").strip()
        
        if choice == 'q':
            print("👋 再见!")
            break
        elif choice == '1':
            print("🌐 本地访问模式")
            start_streamlit()
        elif choice == '2':
            print("🌐 局域网访问模式")
            start_streamlit()
        elif choice == '3':
            print("🌐 ngrok模式")
            if Path("ngrok.exe").exists():
                subprocess.run("ngrok.exe http 8509", shell=True)
            else:
                print("❌ 找不到ngrok.exe，请先下载")
        elif choice == '4':
            print("🌐 Cloudflare Tunnel模式")
            print("📖 请访问: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/local/")
        elif choice == '5':
            print("🌐 localtunnel模式")
            if install_localtunnel():
                start_localtunnel()
        elif choice == '6':
            print("🌐 serveo模式")
            print("📡 命令: ssh -R 80:localhost:8509 serveo.net")
        elif choice == '7':
            print("🌐 playit.gg模式")
            print("📖 请访问: https://playit.gg/")
        elif choice == '8':
            print("🌐 frp模式")
            print("📖 请访问: https://github.com/fatedier/frp")
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 