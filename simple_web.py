#!/usr/bin/env python3
"""
知识库问答系统Web界面 - 集成阶跃API
"""

import streamlit as st
import requests
import json
import os
from pathlib import Path
from simple_qa import call_llm_api
import pdfplumber
import re

# 页面配置
st.set_page_config(page_title="逢考必过·AI考试复习助手", page_icon="🎓", layout="wide")

# 阶跃API配置
STEP_API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
BASE_URL = "https://api.stepfun.com/v1"

def upload_file_to_step(file, purpose="file-extract"):
    """上传文件到阶跃API"""
    headers = {
        "Authorization": f"Bearer {STEP_API_KEY}"
    }
    
    files = {
        "file": (file.name, file.getvalue(), file.type)
    }
    
    data = {
        "purpose": purpose
    }
    
    try:
        response = requests.post(f"{BASE_URL}/files", headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"阶跃API上传失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"上传文件时出错: {str(e)}")
        return None

def extract_text_from_pdf(file):
    """从PDF文件提取文本"""
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"PDF解析失败: {str(e)}")
        return ""

def split_text(text, max_chars=6000):
    """将文本按max_chars分段"""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# 标题
st.title("🎓 逢考必过 · AI考试复习助手")
st.markdown("""
<div style='font-size:20px; color:#1976d2; font-weight:bold;'>
    上传教材/讲义/笔记，AI自动生成高质量考题与答案，帮你高效梳理知识点，助力逢考必过！
</div>
---
""", unsafe_allow_html=True)

st.sidebar.header("🛠️ 功能区")
model_type = st.sidebar.selectbox(
    "请选择大模型API（推荐DeepSeek）",
    ["deepseek", "stepfun"],
    format_func=lambda x: "DeepSeek（更强）" if x=="deepseek" else "阶跃 StepFun"
)
st.sidebar.info("支持PDF/文本上传，自动提取内容，调用大模型API生成高质量考题与答案。无需本地模型依赖！")

st.subheader("📚 上传你的复习资料")
uploaded_files = st.file_uploader("上传PDF或TXT讲义/教材/笔记（可多选）", type=["pdf", "txt"], accept_multiple_files=True)
doc_content = st.text_area("或直接粘贴重点内容：", height=200, placeholder="粘贴你的复习资料、错题本、重点笔记……")

if st.button("🚀 一键生成智能考题"):
    results = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text = ""
            file_name = uploaded_file.name
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
            else:
                text += uploaded_file.read().decode("utf-8", errors="ignore")
            # 判断是否快处理
            if len(text) < 6000:
                # 快处理：整体调用
                with st.spinner(f"AI正在为【{file_name}】生成考题……"):
                    try:
                        qa_result = call_llm_api(text, model_type=model_type)
                        file_qa = [(1, qa_result)]
                    except Exception as e:
                        file_qa = [(1, f"生成失败：{e}")]
            else:
                # 分段处理
                segments = split_text(text, max_chars=6000)
                file_qa = []
                for seg_idx, seg in enumerate(segments):
                    if not seg.strip():
                        continue
                    with st.spinner(f"AI正在为【{file_name}】第{seg_idx+1}段生成考题……"):
                        try:
                            qa_result = call_llm_api(seg, model_type=model_type)
                            file_qa.append((seg_idx+1, qa_result))
                        except Exception as e:
                            file_qa.append((seg_idx+1, f"生成失败：{e}"))
            results.append((file_name, file_qa))
    elif doc_content.strip():
        text = doc_content.strip()
        if len(text) < 6000:
            # 快处理：整体调用
            with st.spinner(f"AI正在为粘贴内容生成考题……"):
                try:
                    qa_result = call_llm_api(text, model_type=model_type)
                    file_qa = [(1, qa_result)]
                except Exception as e:
                    file_qa = [(1, f"生成失败：{e}")]
        else:
            segments = split_text(text, max_chars=6000)
            file_qa = []
            for seg_idx, seg in enumerate(segments):
                if not seg.strip():
                    continue
                with st.spinner(f"AI正在为粘贴内容第{seg_idx+1}段生成考题……"):
                    try:
                        qa_result = call_llm_api(seg, model_type=model_type)
                        file_qa.append((seg_idx+1, qa_result))
                    except Exception as e:
                        file_qa.append((seg_idx+1, f"生成失败：{e}"))
        results.append(("粘贴内容", file_qa))
    else:
        st.warning("请上传文件或粘贴内容！")
        st.stop()
    # 展示所有结果
    for file_name, file_qa in results:
        st.success(f"🎉 【{file_name}】智能考题生成成功！")
        st.markdown("---")
        st.markdown(f"<div style='font-size:18px; color:#388e3c; font-weight:bold;'>【{file_name} · AI智能考题与答案】</div>", unsafe_allow_html=True)
        for seg_idx, qa_result in file_qa:
            st.markdown(f"<span style='color:#888;'>—— 第{seg_idx}段 ——</span>", unsafe_allow_html=True)
            if isinstance(qa_result, str):
                st.error("AI输出格式异常，原始内容如下：")
                st.code(qa_result)
            elif isinstance(qa_result, list) and qa_result and isinstance(qa_result[0], dict) and 'question' in qa_result[0]:
                for idx, qa in enumerate(qa_result, 1):
                    st.markdown(f"**Q{idx}：{qa['question']}**")
                    st.markdown(f"<span style='color:#1976d2;'>A{idx}：</span> {qa['answer']}", unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.error("AI输出格式异常，原始内容如下：")
                st.code(str(qa_result))

st.markdown("""
<div style='color:#757575; font-size:14px;'>
    <b>Tips：</b> 本助手适合期末复习、考研、四六级、各类资格证备考等场景，支持大段资料一键生成高质量考题，助你高效掌握重点难点。
</div>
""", unsafe_allow_html=True)

# 侧边栏 - 系统信息
with st.sidebar:
    st.header("⚙️ 系统信息")
    
    st.subheader("API状态")
    st.success("✅ 阶跃API: 已配置")
    
    st.subheader("快速操作")
    if st.button("🔄 清空当前问答"):
        st.session_state["last_qa"] = []
        st.rerun()
    
    if st.button("📊 查看统计"):
        st.metric("当前问答对数", len(st.session_state.get("last_qa", [])))

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🤖 知识库问答系统 | 阶跃API 智能问答</p>
    </div>
    """,
    unsafe_allow_html=True
) 