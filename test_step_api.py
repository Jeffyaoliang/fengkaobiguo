#!/usr/bin/env python3
"""
测试阶跃API连接
"""

import requests
import json

# 阶跃API配置
STEP_API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
BASE_URL = "https://api.stepfun.com/v1"

def test_step_api():
    """测试阶跃API连接"""
    headers = {
        "Authorization": f"Bearer {STEP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 测试数据
    test_data = {
        "model": "step-1",
        "messages": [
            {"role": "user", "content": "你好，请简单回复一下。"}
        ],
        "max_tokens": 100,
        "temperature": 0.3
    }
    
    # 测试不同的端点
    endpoints = [
        f"{BASE_URL}/chat/completions",
        f"{BASE_URL}/completions", 
        f"{BASE_URL}/v1/chat/completions",
        "https://api.stepfun.com/chat/completions",
        "https://api.stepfun.com/v1/chat/completions"
    ]
    
    print("🔍 开始测试阶跃API连接...")
    print(f"API Key: {STEP_API_KEY[:10]}...")
    print(f"Base URL: {BASE_URL}")
    print("-" * 50)
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"测试端点 {i}: {endpoint}")
        try:
            response = requests.post(endpoint, headers=headers, json=test_data, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 成功! 响应: {result}")
                return True
            elif response.status_code == 404:
                print("❌ 404 - 端点不存在")
            elif response.status_code == 401:
                print("❌ 401 - 认证失败，请检查API Key")
            elif response.status_code == 403:
                print("❌ 403 - 权限不足")
            else:
                print(f"❌ 错误: {response.text}")
                
        except requests.exceptions.Timeout:
            print("⏰ 超时")
        except requests.exceptions.ConnectionError:
            print("🔌 连接错误")
        except Exception as e:
            print(f"❌ 异常: {str(e)}")
        
        print("-" * 30)
    
    print("❌ 所有端点测试失败")
    return False

def test_file_upload():
    """测试文件上传功能"""
    print("\n📁 测试文件上传功能...")
    
    headers = {
        "Authorization": f"Bearer {STEP_API_KEY}"
    }
    
    # 创建一个测试文件
    test_content = "这是一个测试文档，用于验证阶跃API的文件上传功能。"
    
    files = {
        "file": ("test.txt", test_content, "text/plain")
    }
    
    data = {
        "purpose": "file-extract"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/files", headers=headers, files=files, data=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 文件上传成功! 响应: {result}")
            return True
        else:
            print(f"❌ 文件上传失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 文件上传异常: {str(e)}")
        return False

if __name__ == "__main__":
    print("🤖 阶跃API测试工具")
    print("=" * 50)
    
    # 测试聊天API
    chat_success = test_step_api()
    
    # 测试文件上传
    upload_success = test_file_upload()
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"聊天API: {'✅ 成功' if chat_success else '❌ 失败'}")
    print(f"文件上传: {'✅ 成功' if upload_success else '❌ 失败'}")
    
    if not chat_success and not upload_success:
        print("\n💡 建议:")
        print("1. 检查API Key是否正确")
        print("2. 检查网络连接")
        print("3. 查看阶跃API文档确认正确的端点")
        print("4. 确认API Key有足够的权限") 