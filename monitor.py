"""
Level 1: 智能客服监控Agent
"""

import json
from agent.core.llm import core_llm
from agent.utils.logger import Logger


logger = Logger(__name__)


class CustomerMonitorAgent:
    """智能客服监控Agent"""

    def __init__(self):
        """初始化Agent"""
        self.system_prompt = """你是一位世界级的智能客服监控专家。你的核心能力包括：

1. **双流实时融合分析**：
   - 对话流：分析用户查询意图、情绪倾向、问题类别和解决状态
   - 指标流：分析系统延迟、错误率、知识库命中率等指标
   - 融合模块：结合对话语义和系统状态，进行联合推理

2. **智能预警机制**：
   - 检测异常模式（如：用户情绪负面 + 知识库命中率骤降）
   - 识别新未知问题
   - 预测潜在升级风险

分析原则：
- 精准识别：基于多维度特征进行分类
- 预警及时：在问题升级前主动触发告警
- 持续优化：将每次对话转化为知识库资产"""

    async def analyze_conversation(
        self,
        user_query: str,
        ai_response: str,
        system_state: dict
    ) -> dict:
        """分析单次对话"""
        prompt = f"""请分析以下客服对话和系统状态，返回结构化分析结果：

用户查询：{user_query}

AI回答：{ai_response}

系统状态向量：
- 延迟：{system_state['latency']}ms
- 错误率：{system_state['error_rate']*100}%
- 知识库命中率：{system_state['knowledge_base_hit_rate']*100}%
- 活跃对话数：{system_state['active_conversations']}
- 平均响应时间：{system_state['average_response_time']}ms

请从以下维度进行分析：
1. 用户意图识别（intent类别）
2. 情绪分析（positive/neutral/negative）
3. 问题分类（category）
4. 解决状态判断（in_progress/resolved/escalated）
5. 判断是否需要触发预警（alert_triggered: boolean）
6. 如果需要预警，说明原因（alert_reason）
7. 推荐的应对措施（recommendedActions数组）"""

        schema = {
            "type": "object",
            "properties": {
                "intent": {"type": "string"},
                "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
                "category": {"type": "string"},
                "status": {"type": "string", "enum": ["in_progress", "resolved", "escalated"]},
                "confidence": {"type": "number"},
                "alert_triggered": {"type": "boolean"},
                "alert_reason": {"type": "string"},
                "recommendedActions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["intent", "sentiment", "category", "status", "confidence", "alert_triggered"]
        }

        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': prompt}
        ]

        analysis = await core_llm.generate_structured(messages, schema)

        logger.info(f"对话分析完成: {analysis['category']}, 情绪: {analysis['sentiment']}")

        return analysis

    async def execute(self, input_data: str, context: dict = None) -> dict:
        """执行任务"""
        if context and 'type' == 'single_conversation':
            return await self.analyze_conversation(
                input_data,
                context.get('ai_response', ''),
                context.get('system_state', {})
            )
        return {'status': 'unknown task type'}
