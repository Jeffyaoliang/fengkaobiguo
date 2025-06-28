# 🎓 逢考必过 · AI考试复习助手

基于Streamlit + 大模型API的智能知识库问答系统，支持文档上传、自动生成高质量问答对、公网访问等功能。

## ✨ 核心特性

- 🚀 **智能处理策略**：短文档（<6000字）极速处理，长文档自动分段
- 🤖 **多模型支持**：DeepSeek + StepFun API，灵活切换
- 📚 **文档处理**：支持PDF、TXT文件上传和文本粘贴
- 🌐 **公网访问**：ngrok内网穿透，随时随地使用
- 🔧 **易于部署**：一键启动，无需复杂配置

## 🚀 快速开始

### 1. 环境准备
```bash
# 克隆项目
git clone <your-repo-url>
cd hackthon

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

### 3. 访问应用
- 本地访问：http://localhost:8509
- 公网访问：https://2fae-183-209-48-229.ngrok-free.app

## 📋 功能说明

### 智能文档处理
- **快处理模式**：文档少于6000字时，整体调用大模型API，极速输出
- **分段模式**：文档超过6000字时，自动分段处理，确保不超限
- **多文件支持**：支持批量上传多个文件，分别处理

### 大模型集成
- **DeepSeek API**：更强的理解能力，推荐使用
- **StepFun API**：稳定的API服务，备选方案
- **智能切换**：Web界面支持模型选择

### 公网访问
- **ngrok集成**：内置内网穿透工具
- **一键部署**：支持本地、局域网、公网多种访问方式
- **实时监控**：可查看访问统计和连接状态

## 🔧 配置说明

### API配置
当前已预配置的API密钥：
```python
# DeepSeek API
DEEPSEEK_API_KEY = "sk-4b2302a7e26541ac8513325953e61317"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# StepFun API
STEPFUN_API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
STEPFUN_BASE_URL = "https://api.stepfun.com/v1"
```

### 分段配置
- 快处理阈值：6000字符
- 分段大小：6000字符
- 可根据需要调整

## 📁 项目结构
```
hackthon/
├── simple_web.py              # 主Web界面（已集成快处理）
├── simple_qa.py               # 大模型API调用逻辑
├── web_interface.py           # 原Web界面
├── api.py                     # API服务
├── vector_store.py            # 向量存储
├── document_processor.py      # 文档处理
├── config.py                  # 配置文件
├── requirements.txt           # 依赖包
├── ngrok.exe                 # 内网穿透工具
├── knowledge_base/           # 知识库数据
├── uploads/                  # 上传文件目录
└── models/                   # 模型文件目录
```

## 🎯 使用场景

### 考试复习
- 📚 上传教材、讲义、笔记
- 🎯 自动生成高质量考题
- 📝 帮助理解重点难点

### 知识问答
- 📖 文档内容智能问答
- 🔍 快速查找关键信息
- 💡 深度理解知识点

### 学习辅助
- 🎓 学习资料整理
- 📋 知识点梳理
- 🧠 记忆强化训练

## 🌐 部署选项

### 本地部署
```bash
streamlit run simple_web.py --server.port 8509
```

### 局域网部署
```bash
streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
```

### 公网部署
```bash
# 使用ngrok
.\ngrok.exe http 8509

# 或使用云服务器
streamlit run simple_web.py --server.port 8509 --server.address 0.0.0.0
```

## 📊 性能指标

- **短文档处理**：<1秒
- **长文档分段**：自动处理，无超限问题
- **并发支持**：多用户同时访问
- **错误恢复**：自动重试机制

## 🔄 最近更新

### 2025-06-28
- ✅ 集成"快版本"自动分段/整体处理逻辑
- ✅ 优化用户体验，短文档极速处理
- ✅ 保持长文档分段处理的稳定性
- ✅ 完善错误处理和用户提示

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

## 📄 许可证

本项目采用 MIT 许可证。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**项目状态**：✅ 正常运行  
**最后更新**：2025-06-28  
**版本**：v1.0.0  

**祝学习愉快！** 🎉 