#!/usr/bin/env python3
"""
知识库大模型系统演示脚本
"""

import os
import sys
from pathlib import Path

def demo_basic_qa():
    """演示基本问答功能"""
    print("=" * 50)
    print("🤖 知识库大模型系统演示")
    print("=" * 50)
    
    try:
        # 导入必要的模块
        from config import Config
        from document_processor import DocumentProcessor
        from vector_store import VectorStore
        from qa_engine import QAEngine
        
        print("✅ 系统模块加载成功")
        
        # 检查API Key
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠️  请先在 .env 文件中配置 OpenAI API Key")
            print("   然后重新运行演示")
            return
        
        # 创建示例文档
        sample_content = """
人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。

AI的主要应用领域包括：
1. 机器学习：通过算法让计算机从数据中学习
2. 自然语言处理：让计算机理解和生成人类语言
3. 计算机视觉：让计算机理解和处理图像
4. 机器人技术：结合硬件和软件创建智能机器人

人工智能的发展经历了几个重要阶段：
- 1950年代：AI概念的提出和图灵测试
- 1960-1970年代：专家系统的兴起
- 1980-1990年代：机器学习的快速发展
- 2000年代至今：深度学习和大数据驱动的AI革命

机器学习是AI的一个重要子领域，它使计算机能够在没有明确编程的情况下学习和改进。
常见的机器学习算法包括：线性回归、决策树、随机森林、支持向量机、神经网络等。
"""
        
        # 创建临时文档
        temp_file = "temp_demo.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print("\n📄 处理示例文档...")
        
        # 处理文档
        processor = DocumentProcessor()
        chunks = processor.process_file(temp_file)
        print(f"✅ 文档处理完成，生成了 {len(chunks)} 个文档块")
        
        # 初始化向量存储
        print("\n🗄️ 初始化向量存储...")
        vector_store = VectorStore()
        vector_store.add_documents(chunks)
        print("✅ 文档已添加到向量存储")
        
        # 初始化问答引擎
        print("\n🤖 初始化问答引擎...")
        qa_engine = QAEngine(vector_store)
        print("✅ 问答引擎初始化完成")
        
        # 演示问答
        print("\n" + "=" * 50)
        print("💬 开始智能问答演示")
        print("=" * 50)
        
        questions = [
            "什么是人工智能？",
            "AI有哪些主要应用领域？",
            "人工智能的发展经历了哪些阶段？",
            "什么是机器学习？",
            "请介绍一下机器学习的常见算法"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n❓ 问题 {i}: {question}")
            print("-" * 40)
            
            response = qa_engine.ask_question(question)
            answer = response.get('answer', '抱歉，我无法回答这个问题。')
            
            print(f"🤖 回答: {answer}")
            
            # 显示来源
            sources = response.get('sources', [])
            if sources:
                print(f"📚 参考来源: {len(sources)} 个文档")
        
        # 演示搜索功能
        print("\n" + "=" * 50)
        print("🔍 文档搜索演示")
        print("=" * 50)
        
        search_query = "机器学习"
        print(f"🔍 搜索关键词: {search_query}")
        
        search_results = qa_engine.search_documents(search_query, k=3)
        print(f"✅ 找到 {len(search_results)} 个相关文档")
        
        for i, doc in enumerate(search_results, 1):
            print(f"\n📄 文档 {i} (相似度: {doc.get('score', 0):.3f}):")
            print(f"   内容: {doc.get('content', '')[:100]}...")
        
        # 清理临时文件
        os.unlink(temp_file)
        
        print("\n" + "=" * 50)
        print("🎉 演示完成！")
        print("=" * 50)
        print("\n📖 接下来您可以:")
        print("1. 运行 'python start.py' 启动完整系统")
        print("2. 上传自己的文档进行问答")
        print("3. 使用Web界面进行交互")
        print("4. 调用API接口进行集成")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("请检查系统配置和依赖安装")

def demo_api_usage():
    """演示API使用"""
    print("\n" + "=" * 50)
    print("🌐 API使用演示")
    print("=" * 50)
    
    api_code = '''
import requests

# API基础URL
API_BASE_URL = "http://localhost:8000"

# 1. 检查服务状态
response = requests.get(f"{API_BASE_URL}/health")
print("服务状态:", response.json())

# 2. 上传文档
with open("your_document.txt", "rb") as f:
    files = {"files": ("document.txt", f, "text/plain")}
    response = requests.post(f"{API_BASE_URL}/upload", files=files)
    print("上传结果:", response.json())

# 3. 提问
question_data = {"question": "你的问题"}
response = requests.post(f"{API_BASE_URL}/ask", json=question_data)
result = response.json()
print("回答:", result["answer"])

# 4. 搜索文档
search_params = {"query": "搜索关键词", "k": 5}
response = requests.get(f"{API_BASE_URL}/search", params=search_params)
results = response.json()
print("搜索结果:", results)

# 5. 获取统计信息
response = requests.get(f"{API_BASE_URL}/stats")
stats = response.json()
print("系统统计:", stats)
'''
    
    print("📝 API使用示例代码:")
    print(api_code)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        demo_api_usage()
    else:
        demo_basic_qa() 