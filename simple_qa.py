import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import re
from openai import OpenAI
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 阶跃API配置
STEPFUN_API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
STEPFUN_BASE_URL = "https://api.stepfun.com/v1"
DEEPSEEK_API_KEY = "sk-4b2302a7e26541ac8513325953e61317"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

def simple_sentence_split(text: str) -> List[str]:
    """简单的中文分句"""
    sents = re.split(r'[。！？!?]', text)
    return [s.strip() for s in sents if s.strip()]

def extract_qa_pairs_from_text(text: str) -> List[Dict]:
    """从文档自动生成问题-答案-位置索引（简单规则版）"""
    sents = simple_sentence_split(text)
    qa_pairs = []
    for idx, sent in enumerate(sents):
        # 只对较长句子生成问题
        if len(sent) >= 8:
            # 问题模板：这句话的主要内容是什么？
            question = f"这句话的主要内容是什么？"
            answer = sent
            # 计算在原文中的起止索引
            start_idx = text.find(sent)
            end_idx = start_idx + len(sent)
            qa_pairs.append({
                "question": question,
                "answer": answer,
                "start_idx": start_idx,
                "end_idx": end_idx
            })
    return qa_pairs

class SimpleKnowledgeBase:
    def __init__(self, data_dir: str = "./knowledge_base"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.documents = []
        self.load_documents()
    def load_documents(self):
        try:
            docs_file = self.data_dir / "documents.json"
            if docs_file.exists():
                with open(docs_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                logger.info(f"加载了 {len(self.documents)} 个文档")
        except Exception as e:
            logger.error(f"加载文档失败: {e}")
            self.documents = []
    def save_documents(self):
        try:
            docs_file = self.data_dir / "documents.json"
            with open(docs_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
            logger.info("文档保存成功")
        except Exception as e:
            logger.error(f"保存文档失败: {e}")
    def add_document(self, content: str):
        qa_pairs = extract_qa_pairs_from_text(content)
        doc = {
            "id": len(self.documents) + 1,
            "content": content,
            "qa_pairs": qa_pairs
        }
        self.documents.append(doc)
        self.save_documents()
        logger.info(f"添加文档，自动生成{len(qa_pairs)}个问答对")
    def get_all_documents(self) -> List[Dict]:
        return self.documents
    def delete_document(self, doc_id: int) -> bool:
        for i, doc in enumerate(self.documents):
            if doc['id'] == doc_id:
                del self.documents[i]
                self.save_documents()
                logger.info(f"删除文档 ID: {doc_id}")
                return True
        return False

class SimpleQAEngine:
    def __init__(self):
        self.knowledge_base = SimpleKnowledgeBase()
    def add_document(self, content: str):
        self.knowledge_base.add_document(content)
    def get_documents(self) -> List[Dict]:
        return self.knowledge_base.get_all_documents()
    def get_all_qa_pairs(self) -> List[Dict]:
        """获取所有文档的所有问答对"""
        qa_list = []
        for doc in self.knowledge_base.get_all_documents():
            for qa in doc.get('qa_pairs', []):
                qa_list.append({
                    "doc_id": doc["id"],
                    "question": qa["question"],
                    "answer": qa["answer"],
                    "start_idx": qa["start_idx"],
                    "end_idx": qa["end_idx"]
                })
        return qa_list

def call_llm_api(content, model_type="deepseek", max_questions=5):
    if model_type == "deepseek":
        client = OpenAI(
            api_key="sk-4b2302a7e26541ac8513325953e61317",
            base_url="https://api.deepseek.com"
        )
        model = "deepseek-chat"
    else:
        client = OpenAI(
            api_key="5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4",
            base_url="https://api.stepfun.com/v1"
        )
        model = "step-1-8k"
    prompt = (
        f"你是一个专业的知识问答生成专家。请根据以下文档内容，生成{max_questions}个高质量的问答对，要求如下：\n"
        "1. 问题需覆盖理解、应用、分析等不同层次，避免表面化和机械式提问。\n"
        "2. 问题要有深度，能考察对内容的真正理解和实际应用能力。\n"
        "3. 答案要准确、简明、专业。\n"
        f"请严格只输出如下JSON数组格式，每个元素包含question和answer字段，不要输出多余解释：\n"
        f"[{{'question': '问题1', 'answer': '答案1'}}, ...]（共{max_questions}组）\n"
        "文档内容如下：\n"
        + content
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个专业的知识问答生成专家。"},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    raw = response.choices[0].message.content
    # 尝试直接解析
    try:
        return json.loads(raw)
    except Exception:
        import re
        # 去除markdown代码块等包裹
        raw_clean = re.sub(r'^```[a-zA-Z]*', '', raw).strip()
        raw_clean = re.sub(r'```$', '', raw_clean).strip()
        # 尝试正则提取JSON数组
        match = re.search(r'(\[.*\])', raw_clean, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).replace("'", '"'))
            except Exception:
                pass
        return [{"question": "AI输出格式异常（请检查大模型返回内容）", "answer": "未能正确解析AI返回的考题与答案，请尝试减少输入内容或优化提示词。"}]

# 示例用法：
if __name__ == "__main__":
    content = "请介绍一下人工智能的发展历程"
    print("DeepSeek结果：", call_llm_api(content, model_type="deepseek"))
    print("StepFun结果：", call_llm_api(content, model_type="stepfun"))

__all__ = ["SimpleQAEngine", "generate_qa_pairs_with_stepfun", "generate_qa_pairs_with_deepseek", "generate_qa_pairs"] 