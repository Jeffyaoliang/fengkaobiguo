import os
import chromadb
from chromadb.config import Settings
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from typing import List, Dict, Any, Optional
import logging
from config import Config

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = None, embedding_model: str = None):
        self.persist_directory = persist_directory or Config.CHROMA_PERSIST_DIRECTORY
        self.embedding_model = embedding_model or Config.EMBEDDING_MODEL
        
        # 确保目录存在
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # 设置环境变量以支持离线模式
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        
        # 初始化嵌入模型
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True},
                cache_folder="./models"  # 本地缓存目录
            )
        except Exception as e:
            logger.warning(f"无法加载指定的嵌入模型 {self.embedding_model}: {e}")
            # 使用默认的简单嵌入模型
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True},
                cache_folder="./models"
            )
        
        # 初始化向量数据库
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            client_settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        logger.info(f"向量存储初始化完成，持久化目录: {self.persist_directory}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """添加文档到向量存储"""
        if not documents:
            logger.warning("没有文档需要添加")
            return
        
        try:
            # 添加文档到向量存储
            self.vectorstore.add_documents(documents)
            
            # 持久化到磁盘
            self.vectorstore.persist()
            
            logger.info(f"成功添加 {len(documents)} 个文档到向量存储")
        except Exception as e:
            logger.error(f"添加文档到向量存储失败: {e}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """相似性搜索"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"相似性搜索完成，返回 {len(results)} 个结果")
            return results
        except Exception as e:
            logger.error(f"相似性搜索失败: {e}")
            return []
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """带分数的相似性搜索"""
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            logger.info(f"带分数的相似性搜索完成，返回 {len(results)} 个结果")
            return results
        except Exception as e:
            logger.error(f"带分数的相似性搜索失败: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """获取集合统计信息"""
        try:
            collection = self.vectorstore._collection
            count = collection.count()
            return {
                "total_documents": count,
                "persist_directory": self.persist_directory,
                "embedding_model": self.embedding_model
            }
        except Exception as e:
            logger.error(f"获取集合统计信息失败: {e}")
            return {}
    
    def delete_collection(self) -> bool:
        """删除整个集合"""
        try:
            self.vectorstore._collection.delete()
            logger.info("集合删除成功")
            return True
        except Exception as e:
            logger.error(f"删除集合失败: {e}")
            return False
    
    def reset(self) -> bool:
        """重置向量存储"""
        try:
            self.vectorstore._client.reset()
            logger.info("向量存储重置成功")
            return True
        except Exception as e:
            logger.error(f"重置向量存储失败: {e}")
            return False 