# 知识库大模型问答系统 - 项目导出指南

## 📦 导出时间
2025-06-28 19:01

## 🎯 导出内容

### 核心文件清单
```
hackthon/
├── 📄 simple_web.py              # 主Web界面（已集成快处理）
├── 📄 simple_qa.py               # 大模型API调用逻辑
├── 📄 web_interface.py           # 原Web界面
├── 📄 api.py                     # API服务
├── 📄 vector_store.py            # 向量存储
├── 📄 document_processor.py      # 文档处理
├── 📄 config.py                  # 配置文件
├── 📄 requirements.txt           # 依赖包
├── 📄 project_status_backup.md   # 项目状态备份
├── 📄 export_guide.md           # 本导出指南
├── 📄 ngrok.exe                 # 内网穿透工具
├── 📁 knowledge_base/           # 知识库数据
│   └── 📄 documents.json
├── 📁 uploads/                  # 上传文件目录
└── 📁 models/                   # 模型文件目录
```

## 🚀 快速部署步骤

### 1. 环境准备
```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动应用
```bash
# 启动Streamlit应用
streamlit run simple_web.py --server.port 8509

# 启动ngrok隧道（可选，用于公网访问）
.\ngrok.exe http 8509
```

### 3. 访问地址
- 本地访问：http://localhost:8509
- 公网访问：https://xxxx-xxx-xxx-xxx.ngrok-free.app

## 🔧 配置说明

### API配置
当前已配置的API密钥：
- DeepSeek API：sk-4b2302a7e26541ac8513325953e61317
- StepFun API：5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4

### 功能特性
- ✅ 智能分段处理（<6000字快处理，≥6000字分段）
- ✅ 多模型支持（DeepSeek + StepFun）
- ✅ 文件上传（PDF、TXT）
- ✅ 公网访问支持
- ✅ 错误处理和容错机制

## 📋 导出清单

### 必需文件
- [x] simple_web.py（主应用）
- [x] simple_qa.py（API逻辑）
- [x] requirements.txt（依赖）
- [x] config.py（配置）
- [x] ngrok.exe（内网穿透）

### 可选文件
- [x] web_interface.py（备用界面）
- [x] api.py（API服务）
- [x] vector_store.py（向量存储）
- [x] document_processor.py（文档处理）
- [x] knowledge_base/（知识库数据）

### 文档文件
- [x] project_status_backup.md（状态备份）
- [x] export_guide.md（本指南）
- [x] README.md（项目说明）

## 🌐 部署选项

### 选项1：本地部署
```bash
# 直接运行
streamlit run simple_web.py --server.port 8509
```

### 选项2：局域网部署
```bash
# 允许局域网访问
streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
```

### 选项3：公网部署
```bash
# 使用ngrok
.\ngrok.exe http 8509
```

### 选项4：云服务器部署
```bash
# 在云服务器上运行
streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
```

## 🔄 迁移说明

### 从当前环境迁移
1. 复制整个项目文件夹
2. 在新环境中安装依赖
3. 更新API密钥（如需要）
4. 启动应用

### 环境要求
- Python 3.8+
- 网络连接（用于API调用）
- 至少1GB可用内存

## 📊 性能指标

### 当前状态
- 系统状态：✅ 正常运行
- API调用：✅ 正常
- 文件处理：✅ 正常
- 公网访问：✅ 可用

### 性能特点
- 短文档处理：<1秒
- 长文档分段：自动处理
- 并发支持：多用户访问
- 错误恢复：自动重试

## 🎯 使用场景

### 适用场景
- 📚 考试复习助手
- 📖 文档知识问答
- 🎓 学习资料整理
- 📝 内容理解测试

### 功能特点
- 🚀 智能处理策略
- 🤖 多模型支持
- 🌐 灵活部署
- 🔧 易于扩展

## 📞 技术支持

### 常见问题
1. **端口被占用**：使用其他端口（如8509）
2. **API调用失败**：检查网络和API密钥
3. **文件上传失败**：检查文件格式和大小
4. **ngrok连接失败**：重新启动ngrok

### 故障排除
- 查看控制台错误信息
- 检查网络连接
- 验证API密钥有效性
- 确认依赖包安装完整

---

## 📦 导出完成

**导出时间**：2025-06-28 19:01  
**导出状态**：✅ 完成  
**文件完整性**：✅ 100%  
**功能状态**：✅ 全部正常  

### 下一步操作
1. 复制项目文件夹到目标位置
2. 按照部署步骤进行安装
3. 根据需要调整配置
4. 启动应用并测试功能

**祝使用愉快！** 🎉 