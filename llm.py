"""
核心推理引擎 - 支持国产大模型绑定
"""

import asyncio
from typing import Dict, List, Optional, Any
from openai import AsyncOpenAI
from agent.utils.config import config
from agent.utils.logger import Logger


logger = Logger(__name__)


class CoreLLMEngine:
    """核心LLM推理引擎"""

    def __init__(self, provider: Optional[str] = None):
        """初始化引擎"""
        self.provider = provider or config.CORE_LLM_PROVIDER
        self.api_config = config.get_api_config()

        self.client = AsyncOpenAI(
            api_key=self.api_config['api_key'],
            base_url=self.api_config['base_url']
        )

        logger.info(f"核心LLM引擎初始化完成: {self.provider.upper()}")

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs
    ) -> str:
        """生成文本响应"""
        try:
            response = await self.client.chat.completions.create(
                model=self.api_config['model'],
                messages=messages,
                temperature=temperature or config.DEFAULT_TEMPERATURE,
                max_tokens=max_tokens or config.DEFAULT_MAX_TOKENS,
                top_p=top_p or config.DEFAULT_TOP_P,
                **kwargs
            )

            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"LLM生成失败: {e}")
            raise

    async def generate_structured(
        self,
        messages: List[Dict[str, str]],
        schema: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """生成结构化输出（JSON）"""
        # 添加JSON格式指令
        system_prompt = f"""请严格按照以下JSON格式输出：

```json
{schema}
```

要求：
- 必须是合法的JSON格式
- 所有字段必须存在
- 数值类型和范围必须符合要求
- 不要包含任何其他文字
"""

        # 更新系统消息
        if messages and messages[0]['role'] == 'system':
            messages[0]['content'] = system_prompt + '\n\n' + messages[0]['content']
        else:
            messages.insert(0, {'role': 'system', 'content': system_prompt})

        try:
            response = await self.generate(
                messages,
                response_format={'type': 'json_object'},
                **kwargs
            )

            import json
            return json.loads(response)
        except Exception as e:
            logger.error(f"结构化生成失败: {e}")
            raise

    async def health_check(self) -> bool:
        """健康检查"""
        try:
            response = await self.generate(
                [{'role': 'user', 'content': 'Hello'}],
                max_tokens=10
            )
            return len(response) > 0
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return False


# 全局实例
_core_llm_instance = None

def get_core_llm():
    """获取核心LLM实例"""
    global _core_llm_instance
    if _core_llm_instance is None:
        _core_llm_instance = CoreLLMEngine()
    return _core_llm_instance


core_llm = get_core_llm()
