import streamlit as st
import requests
import json
import os
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="知识库大模型",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API配置
API_BASE_URL = "http://localhost:8000"

def check_api_health():
    """检查API服务状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_files(files):
    """上传文件到API"""
    try:
        files_data = []
        for file in files:
            files_data.append(('files', (file.name, file.getvalue(), file.type)))
        
        response = requests.post(f"{API_BASE_URL}/upload", files=files_data)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"上传失败: {str(e)}")
        return None

def ask_question(question: str):
    """发送问题到API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question}
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"提问失败: {str(e)}")
        return None

def search_documents(query: str, k: int = 4):
    """搜索文档"""
    try:
        response = requests.get(f"{API_BASE_URL}/search", params={"query": query, "k": k})
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"搜索失败: {str(e)}")
        return None

def get_chat_history():
    """获取对话历史"""
    try:
        response = requests.get(f"{API_BASE_URL}/chat-history")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"获取对话历史失败: {str(e)}")
        return None

def clear_chat_history():
    """清除对话历史"""
    try:
        response = requests.delete(f"{API_BASE_URL}/chat-history")
        return response.status_code == 200
    except Exception as e:
        st.error(f"清除对话历史失败: {str(e)}")
        return False

def get_stats():
    """获取系统统计信息"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"获取统计信息失败: {str(e)}")
        return None

def reset_knowledge_base():
    """重置知识库"""
    try:
        response = requests.delete(f"{API_BASE_URL}/reset")
        return response.status_code == 200
    except Exception as e:
        st.error(f"重置知识库失败: {str(e)}")
        return False

# 主界面
def main():
    st.title("🤖 知识库大模型系统")
    st.markdown("---")
    
    # 检查API状态
    if not check_api_health():
        st.error("⚠️ API服务未运行，请先启动后端服务")
        st.code("python api.py")
        return
    
    # 侧边栏
    with st.sidebar:
        st.header("📊 系统状态")
        
        # 获取统计信息
        stats = get_stats()
        if stats:
            st.metric("文档总数", stats.get("total_documents", 0))
            st.info(f"嵌入模型: {stats.get('embedding_model', 'N/A')}")
        
        st.markdown("---")
        
        # 操作按钮
        st.header("🔧 系统操作")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 清除对话历史"):
                if clear_chat_history():
                    st.success("对话历史已清除")
                    st.rerun()
        
        with col2:
            if st.button("🔄 重置知识库"):
                if st.checkbox("确认重置知识库？"):
                    if reset_knowledge_base():
                        st.success("知识库已重置")
                        st.rerun()
    
    # 主内容区域
    tab1, tab2, tab3, tab4 = st.tabs(["💬 智能问答", "📁 文档管理", "🔍 文档搜索", "📋 对话历史"])
    
    with tab1:
        st.header("💬 智能问答")
        
        # 问题输入
        question = st.text_area("请输入您的问题:", height=100, placeholder="例如：请介绍一下人工智能的发展历史...")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 提问", type="primary"):
                if question.strip():
                    with st.spinner("正在思考中..."):
                        result = ask_question(question)
                        if result:
                            st.session_state.current_answer = result
                            st.success("回答完成！")
                            st.rerun()
                else:
                    st.warning("请输入问题")
        
        # 显示回答
        if 'current_answer' in st.session_state:
            result = st.session_state.current_answer
            
            st.markdown("### 🤖 AI回答")
            st.markdown(result.get("answer", ""))
            
            # 显示来源
            sources = result.get("sources", [])
            if sources:
                st.markdown("### 📚 参考来源")
                for i, source in enumerate(sources, 1):
                    with st.expander(f"来源 {i}: {source.get('file_name', '未知文件')}"):
                        st.text(source.get("content", ""))
                        st.caption(f"文件路径: {source.get('source', '未知')}")
    
    with tab2:
        st.header("📁 文档管理")
        
        # 文件上传
        st.subheader("上传文档")
        uploaded_files = st.file_uploader(
            "选择要上传的文档",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="支持的文件格式：TXT, PDF, DOCX, MD"
        )
        
        if uploaded_files:
            if st.button("📤 上传文档", type="primary"):
                with st.spinner("正在上传和处理文档..."):
                    result = upload_files(uploaded_files)
                    if result:
                        st.success(f"✅ {result.get('message', '上传成功')}")
                        st.info(f"处理了 {len(result.get('processed_files', []))} 个文件，生成了 {result.get('total_chunks', 0)} 个文档块")
                        st.rerun()
        
        # 目录上传
        st.subheader("批量上传目录")
        directory_path = st.text_input("输入目录路径:", placeholder="/path/to/documents")
        if directory_path and st.button("📁 上传目录"):
            with st.spinner("正在处理目录..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/upload-directory", json={"directory_path": directory_path})
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result.get('message', '目录上传成功')}")
                        st.info(f"生成了 {result.get('total_chunks', 0)} 个文档块")
                        st.rerun()
                    else:
                        st.error("目录上传失败")
                except Exception as e:
                    st.error(f"目录上传失败: {str(e)}")
    
    with tab3:
        st.header("🔍 文档搜索")
        
        # 搜索输入
        search_query = st.text_input("输入搜索关键词:", placeholder="搜索相关文档...")
        k_results = st.slider("返回结果数量:", min_value=1, max_value=10, value=4)
        
        if st.button("🔍 搜索", type="primary"):
            if search_query.strip():
                with st.spinner("正在搜索..."):
                    result = search_documents(search_query, k_results)
                    if result:
                        st.success(f"找到 {len(result.get('results', []))} 个相关文档")
                        
                        # 显示搜索结果
                        for i, doc in enumerate(result.get('results', []), 1):
                            with st.expander(f"文档 {i} (相似度: {doc.get('score', 0):.3f})"):
                                st.markdown(f"**文件名:** {doc.get('file_name', '未知')}")
                                st.markdown(f"**来源:** {doc.get('source', '未知')}")
                                st.markdown("**内容:**")
                                st.text(doc.get('content', ''))
            else:
                st.warning("请输入搜索关键词")
    
    with tab4:
        st.header("📋 对话历史")
        
        # 获取对话历史
        history = get_chat_history()
        if history and history.get('history'):
            for i, chat in enumerate(history['history'], 1):
                with st.expander(f"对话 {i} - {datetime.now().strftime('%H:%M:%S')}"):
                    st.markdown("**问题:**")
                    st.text(chat.get('question', ''))
                    st.markdown("**回答:**")
                    st.text(chat.get('answer', ''))
        else:
            st.info("暂无对话历史")

if __name__ == "__main__":
    main() 