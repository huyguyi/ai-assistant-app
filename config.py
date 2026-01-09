"""
配置管理模块
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """系统配置类"""

    # 核心LLM配置
    CORE_LLM_PROVIDER = os.getenv('CORE_LLM_PROVIDER', 'qwen').lower()

    # Qwen配置
    QWEN_API_KEY = os.getenv('QWEN_API_KEY', os.getenv('CORE_LLM_API_KEY', ''))
    QWEN_API_BASE = os.getenv('QWEN_API_BASE',
        os.getenv('CORE_LLM_API_BASE', 'https://dashscope.aliyuncs.com/compatible-mode/v1'))

    # DeepSeek配置
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
    DEEPSEEK_API_BASE = os.getenv('DEEPSEEK_API_BASE', 'https://api.deepseek.com/v1')

    # GLM配置
    GLM_API_KEY = os.getenv('GLM_API_KEY', '')
    GLM_API_BASE = os.getenv('GLM_API_BASE', 'https://open.bigmodel.cn/api/paas/v4')

    # ChromaDB配置
    CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
    CHROMA_PORT = int(os.getenv('CHROMA_PORT', '8000'))

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # 默认参数
    DEFAULT_TEMPERATURE = float(os.getenv('DEFAULT_TEMPERATURE', '0.7'))
    DEFAULT_MAX_TOKENS = int(os.getenv('DEFAULT_MAX_TOKENS', '2000'))
    DEFAULT_TOP_P = float(os.getenv('DEFAULT_TOP_P', '0.9'))

    @classmethod
    def get_api_config(cls):
        """获取当前API配置"""
        provider = cls.CORE_LLM_PROVIDER

        if provider == 'qwen':
            return {
                'api_key': cls.QWEN_API_KEY,
                'base_url': cls.QWEN_API_BASE,
                'model': 'qwen-max'
            }
        elif provider == 'deepseek':
            return {
                'api_key': cls.DEEPSEEK_API_KEY,
                'base_url': cls.DEEPSEEK_API_BASE,
                'model': 'deepseek-chat'
            }
        elif provider == 'glm':
            return {
                'api_key': cls.GLM_API_KEY,
                'base_url': cls.GLM_API_BASE,
                'model': 'glm-4'
            }
        else:
            raise ValueError(f"不支持的模型提供商: {provider}")

    @classmethod
    def validate(cls):
        """验证配置"""
        config = cls.get_api_config()

        if not config['api_key']:
            raise ValueError("未配置API Key")

        return True


config = Config()
