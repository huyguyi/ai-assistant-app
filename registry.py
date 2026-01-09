"""
工具注册表 - 统一管理所有可用工具
"""

import asyncio
import json
from typing import Dict, Any, Callable, Optional
from agent.utils.logger import Logger


logger = Logger(__name__)


class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        """初始化注册表"""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_default_tools()
        logger.info(f"工具注册表初始化完成: {len(self.tools)}个工具")

    def register(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any],
        handler: Callable
    ):
        """注册工具"""
        if name in self.tools:
            logger.warning(f"工具 {name} 已存在，将被覆盖")

        self.tools[name] = {
            'name': name,
            'description': description,
            'parameters': parameters,
            'handler': handler
        }

        logger.debug(f"工具已注册: {name}")

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """获取工具"""
        return self.tools.get(name)

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """获取所有工具"""
        return self.tools.copy()

    def get_definitions(self) -> List[Dict[str, Any]]:
        """获取工具的OpenAI Function Calling格式"""
        return [
            {
                'type': 'function',
                'function': {
                    'name': tool['name'],
                    'description': tool['description'],
                    'parameters': tool['parameters']
                }
            }
            for tool in self.tools.values()
        ]

    async def execute(
        self,
        name: str,
        arguments: Dict[str, Any]
    ) -> Any:
        """执行工具"""
        tool = self.tools.get(name)

        if not tool:
            raise ValueError(f"工具 {name} 不存在")

        try:
            logger.info(f"执行工具: {name}", arguments=arguments)
            result = await tool['handler'](arguments)
            logger.debug(f"工具执行完成: {name}")
            return result
        except Exception as e:
            logger.error(f"工具执行失败: {name}, 错误: {e}")
            raise

    def _register_default_tools(self):
        """注册默认工具集"""
        # 搜索工具
        self.register(
            name='search_web',
            description='在网络上搜索信息',
            parameters={
                'type': 'object',
                'properties': {
                    'query': {
                        'type': 'string',
                        'description': '搜索查询'
                    },
                    'num_results': {
                        'type': 'number',
                        'description': '返回结果数量',
                        'default': 10
                    }
                },
                'required': ['query']
            },
            handler=lambda args: self._mock_search(args)
        )

        # HTTP请求工具
        self.register(
            name='http_request',
            description='发送HTTP请求',
            parameters={
                'type': 'object',
                'properties': {
                    'url': {'type': 'string', 'description': '请求的URL'},
                    'method': {
                        'type': 'string',
                        'enum': ['GET', 'POST', 'PUT', 'DELETE'],
                        'description': 'HTTP方法'
                    },
                    'headers': {'type': 'object', 'description': '请求头'},
                    'body': {'type': 'object', 'description': '请求体'}
                },
                'required': ['url', 'method']
            },
            handler=lambda args: self._mock_http_request(args)
        )

        # 数学计算工具
        self.register(
            name='calculate',
            description='执行数学计算',
            parameters={
                'type': 'object',
                'properties': {
                    'expression': {
                        'type': 'string',
                        'description': '数学表达式，如 "2 + 3 * 4"'
                    }
                },
                'required': ['expression']
            },
            handler=lambda args: self._mock_calculate(args)
        )

    async def _mock_search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """模拟搜索（实际场景应调用真实搜索API）"""
        await asyncio.sleep(0.5)
        return {
            'results': [
                {'title': '示例结果1', 'url': 'https://example.com/1', 'snippet': '搜索结果摘要1'},
                {'title': '示例结果2', 'url': 'https://example.com/2', 'snippet': '搜索结果摘要2'}
            ],
            'query': args.get('query'),
            'timestamp': '2024-01-09T10:00:00Z'
        }

    async def _mock_http_request(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """模拟HTTP请求（实际场景应发送真实请求）"""
        await asyncio.sleep(0.3)
        return {
            'status': 200,
            'data': {'message': 'Mock response'},
            'headers': {'content-type': 'application/json'}
        }

    async def _mock_calculate(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """模拟数学计算（实际场景应使用安全计算）"""
        expression = args.get('expression', '')
        try:
            result = eval(expression)
            return {'expression': expression, 'result': result}
        except Exception as e:
            return {'expression': expression, 'error': str(e)}


# 全局实例
_tool_registry_instance = None

def get_tool_registry():
    """获取工具注册表实例"""
    global _tool_registry_instance
    if _tool_registry_instance is None:
        _tool_registry_instance = ToolRegistry()
    return _tool_registry_instance


tool_registry = get_tool_registry()
