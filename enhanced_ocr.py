#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强OCR功能模块
简化版本，不依赖复杂的外部库
"""

import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import os
import re
import streamlit as st
from typing import Dict, List

class SimpleImageProcessor:
    """简化的图片处理器"""
    
    def __init__(self):
        # 配置Tesseract路径
        self.tesseract_path = r'E:\p\tesseract.exe'
        self.tessdata_path = r'E:\p\tessdata'
        
        # 设置环境变量
        os.environ['TESSDATA_PREFIX'] = self.tessdata_path
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
    
    def enhance_image(self, image: Image.Image, method: str = 'auto') -> Image.Image:
        """
        增强图片质量
        
        Args:
            image: PIL图像对象
            method: 增强方法 ('auto', 'text', 'table', 'formula')
        
        Returns:
            增强后的图像
        """
        # 转换为RGB模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        if method == 'auto':
            method = self._detect_image_type(img_array)
        
        if method == 'text':
            return self._enhance_for_text(image)
        elif method == 'table':
            return self._enhance_for_table(image)
        elif method == 'formula':
            return self._enhance_for_formula(image)
        else:
            return self._enhance_for_text(image)
    
    def _detect_image_type(self, img_array: np.ndarray) -> str:
        """简单检测图像类型"""
        # 转换为灰度图
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # 检测边缘
        edges = cv2.Canny(gray, 50, 150)
        
        # 检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
        
        # 分析特征
        line_count = len(lines) if lines is not None else 0
        
        # 判断图像类型
        if line_count > 15:  # 很多直线，可能是表格
            return 'table'
        else:
            # 检查是否包含数学符号
            text = pytesseract.image_to_string(Image.fromarray(img_array), lang='eng')
            if any(symbol in text for symbol in ['=', '+', '-', '×', '÷', '∫', '∑', '√']):
                return 'formula'
            else:
                return 'text'
    
    def _enhance_for_text(self, image: Image.Image) -> Image.Image:
        """针对文本的图像增强"""
        # 转换为灰度图
        gray = image.convert('L')
        
        # 转换为numpy数组
        img_array = np.array(gray)
        
        # 自适应直方图均衡化
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(img_array)
        
        # 降噪
        denoised = cv2.fastNlMeansDenoising(enhanced)
        
        # 锐化
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        # 自适应二值化
        binary = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        return Image.fromarray(binary)
    
    def _enhance_for_table(self, image: Image.Image) -> Image.Image:
        """针对表格的图像增强"""
        # 转换为灰度图
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # 边缘检测
        edges = cv2.Canny(img_array, 50, 150)
        
        # 形态学操作，连接断开的线条
        kernel = np.ones((2,2), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # 查找轮廓
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 创建掩码
        mask = np.zeros_like(img_array)
        cv2.drawContours(mask, contours, -1, 255, -1)
        
        # 应用掩码
        result = cv2.bitwise_and(img_array, mask)
        
        # 增强对比度
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(result)
        
        return Image.fromarray(enhanced)
    
    def _enhance_for_formula(self, image: Image.Image) -> Image.Image:
        """针对数学公式的图像增强"""
        # 转换为灰度图
        gray = image.convert('L')
        img_array = np.array(gray)
        
        # 高斯模糊去噪
        blurred = cv2.GaussianBlur(img_array, (3,3), 0)
        
        # 自适应阈值
        binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 形态学操作，保持符号完整性
        kernel = np.ones((1,1), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return Image.fromarray(cleaned)
    
    def extract_text(self, image: Image.Image, method: str = 'auto') -> str:
        """
        提取图片中的文字
        
        Args:
            image: PIL图像对象
            method: 增强方法
        
        Returns:
            提取的文字
        """
        try:
            # 增强图像
            enhanced_image = self.enhance_image(image, method)
            
            # OCR识别
            text = pytesseract.image_to_string(enhanced_image, lang='chi_sim+eng')
            
            # 后处理文字
            text = self._post_process_text(text)
            
            return text.strip()
        
        except Exception as e:
            st.error(f"文字提取失败: {str(e)}")
            return ""
    
    def _post_process_text(self, text: str) -> str:
        """文字后处理"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符，但保留数学符号
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()\[\]{}\-+=×÷∫∑√∞≤≥≠≈±°′″πθαβγδεζηικλμνξοπρστυφχψω]', '', text)
        
        # 修复常见的OCR错误
        corrections = {
            '0': 'O', '1': 'l', '5': 'S', '8': 'B',
            'l': '1', 'O': '0', 'S': '5', 'B': '8'
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        return text
    
    def analyze_image(self, image: Image.Image) -> Dict:
        """
        分析图片内容
        
        Args:
            image: PIL图像对象
        
        Returns:
            分析结果字典
        """
        result = {
            'text': '',
            'image_type': 'unknown',
            'confidence': 0.0
        }
        
        try:
            # 检测图像类型
            img_array = np.array(image)
            image_type = self._detect_image_type(img_array)
            result['image_type'] = image_type
            
            # 提取文字
            result['text'] = self.extract_text(image, image_type)
            
            # 计算置信度
            result['confidence'] = min(len(result['text']) / 100, 1.0)
            
        except Exception as e:
            st.error(f"图像分析失败: {str(e)}")
        
        return result

# 创建全局实例
image_processor = SimpleImageProcessor() 