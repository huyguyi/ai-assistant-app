"""
Level 2: 小红书RedNote-Agent
"""

from agent.core.llm import core_llm
from agent.utils.logger import Logger


logger = Logger(__name__)


class RedNoteAgent:
    """小红书创作Agent"""

    def __init__(self):
        """初始化Agent"""
        self.system_prompt = """你是一位世界级的小红书营销专家。你的核心能力包括：

1. **爆款笔记深度分析**：主题聚类、情感倾向、流行句式、高频词汇
2. **内容策略规划**：切入点、目标人群、情感基调
3. **爆款文案生成**：符合小红书语境、恰当emoji和话题标签
4. **内循环优化**：自我评审并修订文案

创作原则：
- 真实感：模拟真实用户的口吻
- 价值感：提供有用信息或情感价值
- 参与感：设计引发评论和互动的钩子"""

    async def run_full_workflow(self, search_query: str, product_info: dict) -> dict:
        """执行完整工作流"""
        logger.info(f"启动小红书创作工作流: {search_query}")

        # 步骤1-2: 分析
        analysis = await self._analyze_trending_notes(search_query)

        # 步骤3: 策略
        strategy = await self._plan_content_strategy(analysis, product_info)

        # 步骤4: 生成
        draft = await self._generate_draft(strategy, product_info)

        # 步骤5: 优化
        optimized = await self._optimize_draft(draft, analysis)

        logger.info("小红书创作工作流完成")

        return {
            'search_query': search_query,
            'analysis': analysis,
            'strategy': strategy,
            'draft': draft,
            'optimized_draft': optimized
        }

    async def _analyze_trending_notes(self, search_query: str) -> dict:
        """分析爆款笔记（模拟）"""
        prompt = f"""请针对搜索关键词"{search_query}"进行爆款内容分析，返回结构化分析：

分析维度：
1. 热门话题（trendingTopics）
2. 流行形式（popularFormats）
3. 流行句式（commonPhrases）
4. 情感基调（emotionalTone）
5. 互动模式（engagementPatterns）"""

        schema = {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "trendingTopics": {"type": "array", "items": {"type": "string"}},
                "popularFormats": {"type": "array", "items": {"type": "string"}},
                "commonPhrases": {"type": "array", "items": {"type": "string"}},
                "emotionalTone": {"type": "string"},
                "engagementPatterns": {"type": "string"},
                "recommendations": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["summary", "trendingTopics", "recommendations"]
        }

        messages = [
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': prompt}
        ]

        return await core_llm.generate_structured(messages, schema)

    async def _plan_content_strategy(self, analysis: dict, product_info: dict) -> dict:
        """制定内容策略"""
        prompt = f"""基于以下分析，制定内容策略：

分析结果：{analysis}

产品信息：{product_info}

请制定策略：
1. 切入点（angle）
2. 目标人群（targetAudience）
3. 情感基调（emotionalTone）
4. 核心信息（keyMessages）
5. 推荐标签（suggestedTags）"""

        schema = {
            "type": "object",
            "properties": {
                "angle": {"type": "string"},
                "targetAudience": {"type": "string"},
                "emotionalTone": {"type": "string"},
                "keyMessages": {"type": "array", "items": {"type": "string"}},
                "suggestedTags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["angle", "targetAudience", "keyMessages", "suggestedTags"]
        }

        return await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

    async def _generate_draft(self, strategy: dict, product_info: dict) -> dict:
        """生成文案初稿"""
        prompt = f"""生成小红书文案：

策略：{strategy}
产品：{product_info['name']}
功能：{', '.join(product_info.get('features', []))}

要求：
- 标题：吸引眼球，30字以内
- 正文：800-1200字，符合小红书风格
- 标签：5-8个热门标签"""

        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "content": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title", "content", "tags"]
        }

        return await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

    async def _optimize_draft(self, draft: dict, analysis: dict) -> dict:
        """自检与优化"""
        prompt = f"""请对以下文案进行优化：

初稿：{draft}

爆款分析参考：{analysis}

请指出问题并提供优化后的版本。"""

        schema = {
            "type": "object",
            "properties": {
                "optimized": {"type": "boolean"},
                "improvements": {"type": "array", "items": {"type": "string"}},
                "finalDraft": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "content": {"type": "string"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "required": ["optimized", "improvements", "finalDraft"]
        }

        result = await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

        return result['finalDraft']

    async def execute(self, input_data: str, context: dict = None) -> dict:
        """执行任务"""
        if context and context.get('workflow') == 'full':
            return await self.run_full_workflow(input_data, context.get('product_info', {}))
        return {'status': 'unknown task type'}
