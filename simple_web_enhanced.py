#!/usr/bin/env python3
"""
知识库问答系统Web界面 - 增强版（集成图片识别）
"""

import streamlit as st
import requests
import json
import os
from pathlib import Path
from simple_qa import call_llm_api
import pdfplumber
import re
from PIL import Image, ImageFilter
import pytesseract
from enhanced_ocr import image_processor

# 指定 tesseract 主程序路径
pytesseract.pytesseract.tesseract_cmd = r'E:\p\tesseract.exe'
# 指定 tessdata 目录（含chi_sim.traineddata）
os.environ['TESSDATA_PREFIX'] = r'E:\p\tessdata'

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

def extract_text_from_image(file):
    """从图片文件提取文本 - 使用增强OCR"""
    try:
        image = Image.open(file)
        
        # 使用增强图片处理器分析图片
        analysis_result = image_processor.analyze_image(image)
        
        # 显示分析结果
        with st.expander(f"📊 图片分析结果 - {file.name}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("图片类型", analysis_result['image_type'])
            with col2:
                st.metric("置信度", f"{analysis_result['confidence']:.2f}")
            with col3:
                st.metric("文字长度", len(analysis_result['text']))
        
        return analysis_result['text']
        
    except Exception as e:
        st.error(f"图片处理失败: {str(e)}")
        # 回退到基础OCR
        try:
            image = Image.open(file)
            image = image.convert('L')
            image = image.point(lambda x: 0 if x < 140 else 255, '1')
            image = image.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            return text.strip()
        except Exception as e2:
            st.error(f"基础OCR也失败: {str(e2)}")
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

# 图片处理选项
st.sidebar.subheader("🖼️ 图片处理选项")
image_enhancement = st.sidebar.selectbox(
    "图片增强模式",
    ["auto", "text", "table", "formula"],
    format_func=lambda x: {
        "auto": "自动检测",
        "text": "文本优化",
        "table": "表格优化", 
        "formula": "公式优化"
    }[x]
)

show_image_analysis = st.sidebar.checkbox("显示图片分析详情", value=True)

st.sidebar.info("支持PDF/文本/图片上传，智能识别文字、表格、公式，调用大模型API生成高质量考题与答案。")

st.subheader("📚 上传你的复习资料")
uploaded_files = st.file_uploader("上传PDF/TXT/图片讲义/教材/笔记（可多选）", type=["pdf", "txt", "jpg", "jpeg", "png", "bmp", "tiff", "webp"], accept_multiple_files=True)
doc_content = st.text_area("或直接粘贴重点内容：", height=200, placeholder="粘贴你的复习资料、错题本、重点笔记……")

if st.button("🚀 一键生成智能考题"):
    results = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            text = ""
            file_name = uploaded_file.name
            
            with st.spinner(f"正在处理文件: {file_name}..."):
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type.startswith("image/"):
                    text = extract_text_from_image(uploaded_file)
                else:
                    text += uploaded_file.read().decode("utf-8", errors="ignore")
            
            # 判断是否快处理
            if len(text) < 6000:
                with st.spinner(f"AI正在为【{file_name}】生成考题……"):
                    try:
                        qa_result = call_llm_api(text, model_type=model_type)
                        file_qa = [(1, qa_result)]
                        results.append((file_name, file_qa))
                    except Exception as e:
                        st.error(f"AI生成失败: {e}")
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

# 新增：图片处理演示区域
if uploaded_files and show_image_analysis:
    st.markdown("---")
    st.subheader("🖼️ 图片处理演示")
    
    for uploaded_file in uploaded_files:
        if uploaded_file.type.startswith("image/"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("原图")
                st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
            
            with col2:
                st.subheader("处理后")
                try:
                    image = Image.open(uploaded_file)
                    processed_image = image_processor.enhance_image(image, image_enhancement)
                    st.image(processed_image, caption=f"增强模式: {image_enhancement}", use_column_width=True)
                except Exception as e:
                    st.error(f"图片处理失败: {str(e)}")

st.markdown("""
<div style='color:#757575; font-size:14px;'>
    <b>Tips：</b> 本助手适合期末复习、考研、四六级、各类资格证备考等场景，支持大段资料一键生成高质量考题，助你高效掌握重点难点。
    <br><b>新增功能：</b> 智能图片识别，支持文字、表格、公式自动提取，图像质量自动增强！
</div>
""", unsafe_allow_html=True)

# 侧边栏 - 系统信息
with st.sidebar:
    st.header("⚙️ 系统信息")
    
    st.subheader("API状态")
    st.success("✅ 阶跃API: 已配置")
    st.success("✅ 图片识别: 已启用")
    
    st.subheader("快速操作")
    if st.button("🔄 清空当前问答"):
        st.session_state["last_qa"] = []
        st.rerun()
    
    if st.button("📊 查看统计"):
        st.metric("当前问答对数", len(st.session_state.get("last_qa", []))) 