"""
Level 3: 产品经理Agent
"""

from agent.core.llm import core_llm
from agent.utils.logger import Logger


logger = Logger(__name__)


class ProductManagerAgent:
    """产品经理Agent"""

    def __init__(self):
        """初始化Agent"""
        self.system_prompt = """你是一位世界级的高级产品经理。你的核心能力包括：

1. **深度需求挖掘**：苏格拉底式追问揭示真实需求
2. **结构化需求分析**：构建用户画像和痛点矩阵
3. **逻辑严谨的产品设计**：每个功能必须追溯到痛点
4. **元认知能力**：自我反思和逻辑一致性检查

工作原则：
- 不急于给出方案，先深入理解问题
- 每个功能设计都有明确的"为什么"
- PRD文档内部逻辑要高度一致"""

    async def run_full_workflow(self, initial_requirement: str) -> dict:
        """执行完整工作流"""
        logger.info(f"启动产品经理工作流: {initial_requirement}")

        # 步骤1: 追问
        interrogation = await self._interrogation(initial_requirement)

        # 步骤2: 分析
        synthesis = await self._synthesize_analysis(interrogation['history'])

        # 步骤3: 生成PRD
        prd = await self._generate_prd(synthesis, initial_requirement)

        # 步骤4: 校验
        validation = await self._validate_prd_logic(prd)

        logger.info("产品经理工作流完成")

        return {
            'interrogation': interrogation,
            'synthesis': synthesis,
            'prd': prd,
            'validation': validation
        }

    async def _interrogation(self, initial_requirement: str) -> dict:
        """苏格拉底式追问（模拟）"""
        # 模拟5轮追问
        history = []

        questions = [
            "用户希望在哪方面省钱？（消费、理财、投资等）",
            "目标用户当前的痛点是什么？为什么需要这个App？",
            "用户目前是如何尝试解决这些问题的，效果如何？",
            "你希望用户通过使用App获得什么价值或情绪体验？",
            "App的核心差异化是什么？"
        ]

        for i, question in enumerate(questions, 1):
            answer = f"这是模拟的第{i}轮回答"
            history.append({'question': question, 'answer': answer})

        return {'rounds': len(history), 'history': history, 'is_complete': True}

    async def _synthesize_analysis(self, history: list) -> dict:
        """综合分析"""
        prompt = f"""基于以下需求追问记录，进行结构化需求分析：

{history}

请提取：
1. 用户画像（userPersonas）
2. 核心痛点（corePainPoints）：point, priority, rootCause, impact
3. 市场机会（marketOpportunities）
4. 关键成功因素（keySuccessFactors）"""

        schema = {
            "type": "object",
            "properties": {
                "userPersonas": {"type": "array", "items": {"type": "string"}},
                "corePainPoints": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "point": {"type": "string"},
                        "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                        "rootCause": {"type": "string"},
                        "impact": {"type": "string"}
                    }
                }},
                "marketOpportunities": {"type": "array", "items": {"type": "string"}},
                "keySuccessFactors": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["userPersonas", "corePainPoints", "marketOpportunities", "keySuccessFactors"]
        }

        return await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

    async def _generate_prd(self, synthesis: dict, initial_requirement: str) -> dict:
        """生成PRD文档"""
        prompt = f"""基于以下需求分析和综合信息，生成完整的PRD文档：

原始需求：{initial_requirement}

需求分析：{synthesis}

请生成完整的PRD文档，包含：
1. 项目概述（projectOverview）
2. 目标用户（targetUsers）
3. 核心痛点（corePainPoints）：point, priority, userStories
4. 功能设计（features）：name, description, mappedPainPoints, userFlow
5. 成功指标（successMetrics）"""

        schema = {
            "type": "object",
            "properties": {
                "projectOverview": {"type": "string"},
                "targetUsers": {"type": "array", "items": {"type": "string"}},
                "corePainPoints": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "point": {"type": "string"},
                        "priority": {"type": "string"},
                        "userStories": {"type": "array", "items": {"type": "string"}}
                    }
                }},
                "features": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "mappedPainPoints": {"type": "array", "items": {"type": "string"}},
                        "userFlow": {"type": "string"}
                    }
                }},
                "successMetrics": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["projectOverview", "targetUsers", "corePainPoints", "features", "successMetrics"]
        }

        return await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

    async def _validate_prd_logic(self, prd: dict) -> dict:
        """逻辑自洽校验"""
        prompt = f"""请对以下PRD文档进行逻辑自洽性检查：

PRD：{prd}

请检查：
1. 功能-痛点映射验证
2. 流程逻辑检查
3. 指标一致性检查
4. 可行性评估

返回检查结果和评分（0-100）。"""

        schema = {
            "type": "object",
            "properties": {
                "isValid": {"type": "boolean"},
                "issues": {"type": "array", "items": {
                    "type": "object",
                    "properties": {
                        "severity": {"type": "string", "enum": ["critical", "warning", "info"]},
                        "issue": {"type": "string"},
                        "suggestion": {"type": "string"}
                    }
                }},
                "score": {"type": "number"}
            },
            "required": ["isValid", "issues", "score"]
        }

        return await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

    async def execute(self, input_data: str, context: dict = None) -> dict:
        """执行任务"""
        if context and context.get('workflow') == 'full':
            return await self.run_full_workflow(input_data)
        return {'status': 'unknown task type'}
