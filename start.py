#!/usr/bin/env python3
"""
知识库大模型系统启动脚本
"""

import os
import sys
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """设置环境变量"""
    # 设置离线模式
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['TRANSFORMERS_OFFLINE'] = '1'
    
    # 创建必要的目录
    Path("./models").mkdir(exist_ok=True)
    Path("./chroma_db").mkdir(exist_ok=True)
    Path("./uploads").mkdir(exist_ok=True)
    
    logger.info("环境设置完成")

def test_basic_imports():
    """测试基本导入"""
    try:
        import chromadb
        import langchain
        import streamlit
        import fastapi
        logger.info("所有基本依赖导入成功")
        return True
    except ImportError as e:
        logger.error(f"导入失败: {e}")
        return False

def test_vector_store():
    """测试向量存储"""
    try:
        from vector_store import VectorStore
        vector_store = VectorStore()
        logger.info("向量存储初始化成功")
        return True
    except Exception as e:
        logger.error(f"向量存储初始化失败: {e}")
        return False

def main():
    """主函数"""
    logger.info("开始启动知识库大模型系统...")
    
    # 设置环境
    setup_environment()
    
    # 测试基本导入
    if not test_basic_imports():
        logger.error("基本依赖测试失败，请检查安装")
        return False
    
    # 测试向量存储
    if not test_vector_store():
        logger.error("向量存储测试失败")
        return False
    
    logger.info("系统启动测试完成，所有组件正常")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 系统启动测试成功！")
        print("现在可以运行以下命令启动服务：")
        print("1. 启动API服务: python api.py")
        print("2. 启动Web界面: streamlit run web_interface.py")
    else:
        print("\n❌ 系统启动测试失败，请检查错误信息")
        sys.exit(1) 