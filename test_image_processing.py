#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理功能测试脚本
"""

import streamlit as st
from PIL import Image
import os
from image_processor import image_processor

def test_image_processing():
    """测试图片处理功能"""
    st.title("🖼️ 图片处理功能测试")
    st.markdown("---")
    
    # 上传测试图片
    uploaded_file = st.file_uploader(
        "上传测试图片", 
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'webp'],
        help="支持多种图片格式，系统会自动检测图片类型并优化处理"
    )
    
    if uploaded_file is not None:
        # 显示原图
        st.subheader("📸 原图")
        image = Image.open(uploaded_file)
        st.image(image, caption=f"原图: {uploaded_file.name}", use_column_width=True)
        
        # 图片信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("图片尺寸", f"{image.size[0]} × {image.size[1]}")
        with col2:
            st.metric("图片模式", image.mode)
        with col3:
            st.metric("文件大小", f"{uploaded_file.size / 1024:.1f} KB")
        
        st.markdown("---")
        
        # 选择处理模式
        st.subheader("🔧 处理选项")
        enhancement_type = st.selectbox(
            "选择增强模式",
            ["auto", "text", "table", "formula", "diagram"],
            format_func=lambda x: {
                "auto": "🤖 自动检测",
                "text": "📝 文本优化",
                "table": "📋 表格优化", 
                "formula": "🧮 公式优化",
                "diagram": "📊 图表优化"
            }[x]
        )
        
        if st.button("🚀 开始处理"):
            with st.spinner("正在处理图片..."):
                try:
                    # 分析图片内容
                    analysis_result = image_processor.analyze_image_content(image)
                    
                    # 预处理图片
                    processed_image = image_processor.preprocess_image(image, enhancement_type)
                    
                    # 显示结果
                    st.markdown("---")
                    st.subheader("📊 分析结果")
                    
                    # 分析指标
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("检测类型", analysis_result['image_type'])
                    with col2:
                        st.metric("置信度", f"{analysis_result['confidence']:.2f}")
                    with col3:
                        st.metric("文字长度", len(analysis_result['text']))
                    with col4:
                        st.metric("表格数量", len(analysis_result['tables']))
                    
                    # 显示处理后的图片
                    st.subheader("🖼️ 处理后图片")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.image(image, caption="原图", use_column_width=True)
                    
                    with col2:
                        st.image(processed_image, caption=f"处理后 ({enhancement_type})", use_column_width=True)
                    
                    # 显示提取的文字
                    if analysis_result['text']:
                        st.subheader("📝 提取的文字")
                        st.text_area("识别结果", analysis_result['text'], height=200)
                    
                    # 显示提取的表格
                    if analysis_result['tables']:
                        st.subheader("📋 提取的表格")
                        for i, table in enumerate(analysis_result['tables']):
                            st.write(f"表格 {i+1}:")
                            st.dataframe(table, use_container_width=True)
                    
                    # 显示提取的公式
                    if analysis_result['formulas']:
                        st.subheader("🧮 提取的公式")
                        for i, formula in enumerate(analysis_result['formulas']):
                            st.code(formula, language='text')
                    
                    st.success("✅ 图片处理完成！")
                    
                except Exception as e:
                    st.error(f"❌ 处理失败: {str(e)}")
    
    # 功能说明
    st.markdown("---")
    st.subheader("📖 功能说明")
    
    with st.expander("🔍 支持的图片类型"):
        st.markdown("""
        - **文本图片**: 包含大量文字的图片，如文档截图、笔记等
        - **表格图片**: 包含表格结构的图片，如数据表、统计表等
        - **公式图片**: 包含数学公式的图片，如数学题、公式推导等
        - **图表图片**: 包含图表的图片，如柱状图、折线图、流程图等
        """)
    
    with st.expander("⚙️ 处理技术"):
        st.markdown("""
        - **图像增强**: 自适应直方图均衡化、降噪、锐化
        - **边缘检测**: Canny边缘检测、形态学操作
        - **OCR识别**: Tesseract OCR引擎，支持中英文
        - **智能分类**: 基于图像特征的自动类型检测
        - **表格识别**: 基于结构分析的表格提取
        - **公式识别**: 数学符号和表达式的识别
        """)
    
    with st.expander("🎯 应用场景"):
        st.markdown("""
        - **学习资料**: 教材截图、讲义图片、笔记照片
        - **考试题目**: 试卷图片、题目截图、答案图片
        - **数据表格**: 统计表、数据表、对比表
        - **数学公式**: 数学题、公式推导、计算过程
        - **图表分析**: 流程图、思维导图、组织结构图
        """)

if __name__ == "__main__":
    test_image_processing() 