# Agent 模块 - 核心逻辑

这是燧石Agent系统的核心逻辑代码模块。

## 目录结构

```
agent/
├── __init__.py           # 包初始化
├── core/                 # 核心模块
│   ├── __init__.py
│   ├── llm.py          # 核心推理引擎
│   ├── memory.py       # 持久化记忆库
│   └── orchestrator.py # Agent协调框架
├── tools/               # 工具模块
│   ├── __init__.py
│   └── registry.py     # 工具注册表
├── agents/              # 专业Agent
│   ├── __init__.py
│   ├── monitor.py      # Level 1: 客服监控
│   ├── rednote.py      # Level 2: 小红书创作
│   └── product.py      # Level 3: 产品经理
└── utils/               # 工具函数
    ├── __init__.py
    ├── config.py       # 配置管理
    └── logger.py      # 日志工具
```

## 核心组件

### 1. 核心推理引擎 (llm.py)
- 支持国产大模型（Qwen/DeepSeek/GLM）
- 文本生成、流式输出、结构化输出
- 统一的OpenAI兼容接口

### 2. 持久化记忆库 (memory.py)
- ChromaDB向量数据库
- 语义检索和元数据检索
- 自动记忆分级和清理

### 3. 工具系统 (tools/)
- 搜索、代码执行、数据库查询
- HTTP请求、文件读写、数学计算
- 可扩展的工具注册机制

### 4. Agent协调框架 (orchestrator.py)
- 任务分解与规划
- 多Agent角色调度
- 工作流执行管理

## 使用示例

```python
from agent.core.llm import CoreLLMEngine
from agent.agents.monitor import CustomerMonitorAgent

# 初始化引擎
engine = CoreLLMEngine()

# 创建Agent
monitor = CustomerMonitorAgent()

# 执行任务
result = await monitor.analyze_conversation(user_query, ai_response, system_state)
```

## 设计原则

1. **国产核心**：所有推理由单一国产大模型驱动
2. **能力延伸**：围绕核心模型构建扩展系统
3. **架构适配**：最大化挖掘模型潜力
4. **模块化**：清晰的模块划分和依赖关系
