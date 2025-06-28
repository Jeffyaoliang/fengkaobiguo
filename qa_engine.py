from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from typing import List, Dict, Any, Optional
import logging
from config import Config
from vector_store import VectorStore

logger = logging.getLogger(__name__)

class QAEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
        # 初始化大语言模型
        if not Config.OPENAI_API_KEY:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")
        
        self.llm = ChatOpenAI(
            model_name=Config.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=Config.OPENAI_API_KEY
        )
        
        # 初始化对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 自定义提示模板
        self.qa_prompt_template = """你是一个专业的AI助手，基于以下上下文信息来回答问题。

上下文信息:
{context}

问题: {question}

请基于上下文信息提供准确、详细的回答。如果上下文中没有相关信息，请明确说明无法从提供的信息中找到答案。

回答:"""
        
        self.qa_prompt = PromptTemplate(
            template=self.qa_prompt_template,
            input_variables=["context", "question"]
        )
        
        # 初始化检索问答链
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt},
            return_source_documents=True,
            verbose=True
        )
        
        logger.info("问答引擎初始化完成")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """提问并获取回答"""
        try:
            # 执行问答
            result = self.qa_chain({"question": question})
            
            # 提取源文档信息
            source_documents = []
            if result.get("source_documents"):
                for doc in result["source_documents"]:
                    source_documents.append({
                        "content": doc.page_content[:200] + "...",
                        "source": doc.metadata.get("source", "未知"),
                        "file_name": doc.metadata.get("file_name", "未知")
                    })
            
            response = {
                "answer": result.get("answer", "抱歉，我无法回答这个问题。"),
                "sources": source_documents,
                "question": question
            }
            
            logger.info(f"问题回答完成: {question}")
            return response
            
        except Exception as e:
            logger.error(f"问答过程中出现错误: {e}")
            return {
                "answer": f"抱歉，处理您的问题时出现了错误: {str(e)}",
                "sources": [],
                "question": question
            }
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        try:
            chat_history = self.memory.chat_memory.messages
            history = []
            
            for i in range(0, len(chat_history), 2):
                if i + 1 < len(chat_history):
                    history.append({
                        "question": chat_history[i].content,
                        "answer": chat_history[i + 1].content
                    })
            
            return history
        except Exception as e:
            logger.error(f"获取对话历史失败: {e}")
            return []
    
    def clear_memory(self) -> bool:
        """清除对话记忆"""
        try:
            self.memory.clear()
            logger.info("对话记忆已清除")
            return True
        except Exception as e:
            logger.error(f"清除对话记忆失败: {e}")
            return False
    
    def search_documents(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "未知"),
                    "file_name": doc.metadata.get("file_name", "未知"),
                    "score": float(score)
                })
            
            return documents
        except Exception as e:
            logger.error(f"搜索文档失败: {e}")
            return [] 