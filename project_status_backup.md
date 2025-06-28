# 知识库大模型问答系统 - 项目状态备份

## 📅 备份时间
2025-06-28 19:01

## 🎯 系统概述
基于Streamlit + 大模型API的智能知识库问答系统，支持文档上传、自动生成高质量问答对、公网访问等功能。

## 🚀 核心功能

### 1. 智能文档处理
- ✅ 支持PDF、TXT文件上传
- ✅ 支持多文件批量处理
- ✅ 支持直接文本粘贴
- ✅ 自动文本提取和预处理

### 2. 大模型集成
- ✅ DeepSeek API集成（推荐）
- ✅ 阶跃StepFun API集成
- ✅ 支持模型切换
- ✅ 智能问答生成

### 3. 智能分段处理
- ✅ **快版本**：文档<6000字时整体处理，极速输出
- ✅ **分段版本**：文档≥6000字时自动分段，稳健处理
- ✅ 自动长度判断和策略选择

### 4. 公网访问
- ✅ ngrok内网穿透配置
- ✅ 公网地址：https://2fae-183-209-48-229.ngrok-free.app
- ✅ 局域网访问支持

## 📁 项目结构
```
hackthon/
├── simple_web.py          # 主Web界面（已集成快处理）
├── simple_qa.py           # 大模型API调用逻辑
├── web_interface.py       # 原Web界面
├── api.py                 # API服务（有依赖问题）
├── vector_store.py        # 向量存储
├── document_processor.py  # 文档处理
├── config.py             # 配置文件
├── requirements.txt      # 依赖包
├── ngrok.exe            # 内网穿透工具
└── knowledge_base/      # 知识库数据
```

## 🔧 当前配置

### API配置
```python
# DeepSeek API
DEEPSEEK_API_KEY = "sk-4b2302a7e26541ac8513325953e61317"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# 阶跃StepFun API
STEPFUN_API_KEY = "5LHfDtyA4XFX5ObOqZtIrz0UlOMcYEn2hvy0FQdhT113enLNiLySnSWndOzz75ir4"
STEPFUN_BASE_URL = "https://api.stepfun.com/v1"
```

### 分段阈值
- 快处理阈值：6000字符
- 分段大小：6000字符

### 端口配置
- Streamlit默认端口：8501-8508（已被占用）
- 当前使用端口：8509
- ngrok Web界面：http://127.0.0.1:4040

## 🌐 访问地址

### 本地访问
- Local URL: http://localhost:8509
- Network URL: http://192.168.68.158:8509

### 公网访问
- ngrok地址：https://2fae-183-209-48-229.ngrok-free.app
- 状态：在线，延迟62ms

## 🚀 启动命令

### 1. 启动Streamlit应用
```bash
streamlit run simple_web.py --server.port 8509
```

### 2. 启动ngrok隧道
```bash
.\ngrok.exe http 8509
```

## 📊 系统状态

### ✅ 正常功能
- Web界面运行正常
- 大模型API调用正常
- 文件上传处理正常
- 智能分段/快处理正常
- 公网访问正常

### ⚠️ 已知问题
- api.py因sentence-transformers依赖问题无法启动
- 部分端口被占用（8501-8508）

### 📈 使用统计
- ngrok连接数：388
- 活跃连接：42
- 平均延迟：0.81ms

## 🎯 核心特性

### 1. 智能处理策略
```python
# 快处理逻辑（已集成）
if len(text) < 6000:
    # 整体调用，极速输出
    qa_result = call_llm_api(text, model_type=model_type)
else:
    # 分段处理，稳健可靠
    segments = split_text(text, max_chars=6000)
```

### 2. 多模型支持
- DeepSeek：更强的理解能力
- StepFun：稳定的API服务

### 3. 健壮性设计
- AI输出格式异常自动处理
- 网络错误重试机制
- 分段失败容错处理

## 🔄 最近更新

### 2025-06-28 更新内容
1. ✅ 集成"快版本"自动分段/整体处理逻辑
2. ✅ 优化用户体验，短文档极速处理
3. ✅ 保持长文档分段处理的稳定性
4. ✅ 完善错误处理和用户提示

## 📝 使用说明

### 快速开始
1. 启动Streamlit：`streamlit run simple_web.py --server.port 8509`
2. 启动ngrok：`.\ngrok.exe http 8509`
3. 访问公网地址或本地地址
4. 上传文档或粘贴内容
5. 选择大模型，一键生成考题

### 功能特点
- 🚀 短文档（<6000字）：整体处理，秒级输出
- 📚 长文档（≥6000字）：智能分段，稳健处理
- 🌐 公网访问：随时随地使用
- 🤖 多模型：灵活选择API

## 🎉 项目亮点

1. **智能处理**：自动判断文档长度，选择最优处理策略
2. **用户体验**：短文档极速响应，长文档稳定可靠
3. **技术架构**：模块化设计，易于扩展和维护
4. **部署灵活**：支持本地、局域网、公网多种访问方式

---

**备份完成时间**：2025-06-28 19:01  
**系统状态**：✅ 正常运行  
**公网访问**：✅ 可用  
**核心功能**：✅ 全部正常 