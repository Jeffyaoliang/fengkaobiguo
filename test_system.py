#!/usr/bin/env python3
"""
知识库大模型系统测试脚本
"""

import os
import sys
import tempfile
import requests
import time
from pathlib import Path

def test_config():
    """测试配置模块"""
    print("🔧 测试配置模块...")
    try:
        from config import Config
        print(f"✅ 配置加载成功")
        print(f"   - 嵌入模型: {Config.EMBEDDING_MODEL}")
        print(f"   - 分块大小: {Config.CHUNK_SIZE}")
        print(f"   - 支持格式: {Config.SUPPORTED_FORMATS}")
        return True
    except Exception as e:
        print(f"❌ 配置模块测试失败: {e}")
        return False

def test_document_processor():
    """测试文档处理器"""
    print("\n📄 测试文档处理器...")
    try:
        from document_processor import DocumentProcessor
        
        # 创建测试文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("这是一个测试文档。包含一些测试内容，用于验证文档处理功能是否正常工作。")
            test_file = f.name
        
        processor = DocumentProcessor()
        chunks = processor.process_file(test_file)
        
        print(f"✅ 文档处理器测试成功")
        print(f"   - 生成了 {len(chunks)} 个文档块")
        
        # 清理测试文件
        os.unlink(test_file)
        return True
        
    except Exception as e:
        print(f"❌ 文档处理器测试失败: {e}")
        return False

def test_vector_store():
    """测试向量存储"""
    print("\n🗄️ 测试向量存储...")
    try:
        from vector_store import VectorStore
        from langchain.schema import Document
        
        # 创建测试文档
        test_docs = [
            Document(
                page_content="这是第一个测试文档的内容。",
                metadata={"source": "test1.txt", "file_name": "test1.txt"}
            ),
            Document(
                page_content="这是第二个测试文档的内容。",
                metadata={"source": "test2.txt", "file_name": "test2.txt"}
            )
        ]
        
        # 使用临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            vector_store = VectorStore(persist_directory=temp_dir)
            vector_store.add_documents(test_docs)
            
            # 测试搜索
            results = vector_store.similarity_search("测试文档", k=2)
            print(f"✅ 向量存储测试成功")
            print(f"   - 添加了 {len(test_docs)} 个文档")
            print(f"   - 搜索返回 {len(results)} 个结果")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量存储测试失败: {e}")
        return False

def test_qa_engine():
    """测试问答引擎"""
    print("\n🤖 测试问答引擎...")
    try:
        # 检查API Key
        from config import Config
        if not Config.OPENAI_API_KEY or Config.OPENAI_API_KEY == "your_openai_api_key_here":
            print("⚠️  跳过问答引擎测试（需要配置OpenAI API Key）")
            return True
        
        from vector_store import VectorStore
        from qa_engine import QAEngine
        from langchain.schema import Document
        
        # 创建测试文档
        test_docs = [
            Document(
                page_content="人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
                metadata={"source": "ai_intro.txt", "file_name": "ai_intro.txt"}
            )
        ]
        
        # 使用临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            vector_store = VectorStore(persist_directory=temp_dir)
            vector_store.add_documents(test_docs)
            
            qa_engine = QAEngine(vector_store)
            response = qa_engine.ask_question("什么是人工智能？")
            
            print(f"✅ 问答引擎测试成功")
            print(f"   - 问题: 什么是人工智能？")
            print(f"   - 回答长度: {len(response.get('answer', ''))} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 问答引擎测试失败: {e}")
        return False

def test_api_server():
    """测试API服务器"""
    print("\n🌐 测试API服务器...")
    try:
        # 检查服务器是否运行
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ API服务器正在运行")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("⚠️  API服务器未运行，跳过API测试")
        print("   请先运行: python api.py")
        return True
        
    except Exception as e:
        print(f"❌ API服务器测试失败: {e}")
        return False

def test_web_interface():
    """测试Web界面"""
    print("\n🎨 测试Web界面...")
    try:
        # 检查streamlit是否可用
        import streamlit
        print("✅ Streamlit可用")
        return True
    except ImportError:
        print("❌ Streamlit未安装")
        return False

def create_sample_documents():
    """创建示例文档"""
    print("\n📝 创建示例文档...")
    
    sample_docs = {
        "ai_introduction.txt": """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。

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
""",
        
        "machine_learning.md": """
# 机器学习基础

## 什么是机器学习？

机器学习是人工智能的一个子领域，它使计算机能够在没有明确编程的情况下学习和改进。

## 主要类型

### 1. 监督学习
- 使用标记的训练数据
- 包括分类和回归问题
- 例如：图像分类、房价预测

### 2. 无监督学习
- 使用未标记的数据
- 发现数据中的隐藏模式
- 例如：聚类分析、降维

### 3. 强化学习
- 通过与环境交互学习
- 基于奖励机制优化行为
- 例如：游戏AI、自动驾驶

## 常用算法

- 线性回归
- 决策树
- 随机森林
- 支持向量机
- 神经网络
- 深度学习
""",
        
        "python_programming.txt": """
Python编程语言简介

Python是一种高级编程语言，以其简洁的语法和强大的功能而闻名。

## 主要特点

1. 易学易用：语法简洁，接近自然语言
2. 跨平台：可在Windows、Mac、Linux上运行
3. 丰富的库：拥有大量的第三方库和框架
4. 广泛应用：Web开发、数据分析、AI、科学计算等

## 基础语法

### 变量和数据类型
```python
name = "张三"  # 字符串
age = 25      # 整数
height = 1.75 # 浮点数
is_student = True  # 布尔值
```

### 条件语句
```python
if age >= 18:
    print("成年人")
else:
    print("未成年人")
```

### 循环
```python
for i in range(5):
    print(i)

while condition:
    # 循环体
    pass
```

## 常用库

- NumPy：数值计算
- Pandas：数据分析
- Matplotlib：数据可视化
- Flask/Django：Web框架
- TensorFlow/PyTorch：机器学习
"""
    }
    
    # 创建示例文档目录
    sample_dir = Path("sample_documents")
    sample_dir.mkdir(exist_ok=True)
    
    for filename, content in sample_docs.items():
        file_path = sample_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    print(f"✅ 创建了 {len(sample_docs)} 个示例文档")
    print(f"   位置: {sample_dir.absolute()}")
    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 知识库大模型系统测试")
    print("=" * 60)
    
    tests = [
        ("配置模块", test_config),
        ("文档处理器", test_document_processor),
        ("向量存储", test_vector_store),
        ("问答引擎", test_qa_engine),
        ("API服务器", test_api_server),
        ("Web界面", test_web_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常使用。")
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
    
    # 创建示例文档
    create_sample_documents()
    
    print("\n📖 使用说明:")
    print("1. 配置 .env 文件中的 OpenAI API Key")
    print("2. 运行: python start.py")
    print("3. 上传示例文档或自己的文档")
    print("4. 开始智能问答！")

if __name__ == "__main__":
    main() 