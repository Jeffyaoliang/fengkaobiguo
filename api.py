from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
import logging
from pathlib import Path

from config import Config
from document_processor import DocumentProcessor
from vector_store import VectorStore
from qa_engine import QAEngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="知识库大模型API",
    description="基于向量数据库和大语言模型的知识库问答系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化组件
vector_store = VectorStore()
document_processor = DocumentProcessor(
    chunk_size=Config.CHUNK_SIZE,
    chunk_overlap=Config.CHUNK_OVERLAP
)
qa_engine = QAEngine(vector_store)

# 确保上传目录存在
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

# Pydantic模型
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: List[dict]
    question: str

class UploadResponse(BaseModel):
    message: str
    processed_files: List[str]
    total_chunks: int

class StatsResponse(BaseModel):
    total_documents: int
    persist_directory: str
    embedding_model: str

@app.get("/")
async def root():
    """根路径"""
    return {"message": "知识库大模型API服务正在运行"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "知识库大模型API"}

@app.post("/upload", response_model=UploadResponse)
async def upload_documents(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    """上传文档"""
    try:
        processed_files = []
        total_chunks = 0
        
        for file in files:
            # 检查文件格式
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in Config.SUPPORTED_FORMATS:
                continue
            
            # 保存文件
            file_path = os.path.join(Config.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            processed_files.append(file.filename)
            
            # 处理文档
            chunks = document_processor.process_file(file_path)
            if chunks:
                vector_store.add_documents(chunks)
                total_chunks += len(chunks)
        
        return UploadResponse(
            message=f"成功处理 {len(processed_files)} 个文件",
            processed_files=processed_files,
            total_chunks=total_chunks
        )
    
    except Exception as e:
        logger.error(f"上传文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"上传文档失败: {str(e)}")

@app.post("/upload-directory")
async def upload_directory(directory_path: str):
    """上传整个目录的文档"""
    try:
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=400, detail="目录不存在")
        
        chunks = document_processor.process_directory(directory_path)
        if chunks:
            vector_store.add_documents(chunks)
        
        return {
            "message": f"成功处理目录: {directory_path}",
            "total_chunks": len(chunks)
        }
    
    except Exception as e:
        logger.error(f"上传目录失败: {e}")
        raise HTTPException(status_code=500, detail=f"上传目录失败: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """提问"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="问题不能为空")
        
        response = qa_engine.ask_question(request.question)
        return QuestionResponse(**response)
    
    except Exception as e:
        logger.error(f"提问失败: {e}")
        raise HTTPException(status_code=500, detail=f"提问失败: {str(e)}")

@app.get("/search")
async def search_documents(query: str, k: int = 4):
    """搜索相关文档"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="搜索查询不能为空")
        
        results = qa_engine.search_documents(query, k)
        return {"query": query, "results": results}
    
    except Exception as e:
        logger.error(f"搜索文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索文档失败: {str(e)}")

@app.get("/chat-history")
async def get_chat_history():
    """获取对话历史"""
    try:
        history = qa_engine.get_chat_history()
        return {"history": history}
    
    except Exception as e:
        logger.error(f"获取对话历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")

@app.delete("/chat-history")
async def clear_chat_history():
    """清除对话历史"""
    try:
        success = qa_engine.clear_memory()
        if success:
            return {"message": "对话历史已清除"}
        else:
            raise HTTPException(status_code=500, detail="清除对话历史失败")
    
    except Exception as e:
        logger.error(f"清除对话历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"清除对话历史失败: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """获取系统统计信息"""
    try:
        stats = vector_store.get_collection_stats()
        return StatsResponse(**stats)
    
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

@app.delete("/reset")
async def reset_knowledge_base():
    """重置知识库"""
    try:
        success = vector_store.reset()
        if success:
            return {"message": "知识库已重置"}
        else:
            raise HTTPException(status_code=500, detail="重置知识库失败")
    
    except Exception as e:
        logger.error(f"重置知识库失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置知识库失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=True
    ) 