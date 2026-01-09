"""
Agent协调框架 - 主控Agent
"""

import asyncio
from typing import Dict, List, Any
from agent.core.llm import core_llm
from agent.utils.logger import Logger


logger = Logger(__name__)


class CoordinatorAgent:
    """主控Agent - 协调专业Agent"""

    def __init__(self):
        """初始化协调器"""
        self.agents = {}
        logger.info("主控Agent初始化完成")

    def register_agent(self, name: str, agent: Any):
        """注册专业Agent"""
        self.agents[name] = agent
        logger.debug(f"Agent已注册: {name}")

    async def plan_workflow(
        self,
        task_description: str
    ) -> Dict[str, Any]:
        """规划工作流"""
        prompt = f"""请为以下任务规划详细的工作流：

任务描述：{task_description}

可用的Agent：
- monitor: 智能客服监控
- rednote: 小红书内容创作
- product: 产品经理

请输出工作流规划，包括：
1. 任务分解步骤
2. 每个步骤的执行Agent
3. 步骤间的依赖关系

请以JSON格式输出。"""

        schema = {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "agent": {"type": "string"},
                            "description": {"type": "string"},
                            "dependencies": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["id", "name", "agent", "description"]
                    }
                }
            },
            "required": ["steps"]
        }

        workflow = await core_llm.generate_structured(
            [{'role': 'user', 'content': prompt}],
            schema
        )

        logger.info(f"工作流规划完成: {len(workflow['steps'])}个步骤")
        return workflow

    async def execute_workflow(
        self,
        steps: List[Dict[str, Any]],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """执行工作流"""
        logger.info("开始执行工作流")

        results = {}
        completed_steps = set()
        pending_steps = steps.copy()

        max_iterations = 10
        iteration = 0

        while pending_steps and iteration < max_iterations:
            iteration += 1
            progress_made = False

            for step in pending_steps[:]:
                # 检查依赖是否完成
                dependencies = step.get('dependencies', [])
                if not all(dep in completed_steps for dep in dependencies):
                    continue

                # 执行步骤
                try:
                    logger.info(f"执行步骤: {step['name']}")
                    agent_name = step['agent']
                    agent = self.agents.get(agent_name)

                    if not agent:
                        logger.warning(f"Agent {agent_name} 不存在")
                        pending_steps.remove(step)
                        continue

                    # 执行Agent任务
                    result = await agent['execute'](
                        step.get('description', ''),
                        context
                    )

                    results[step['id']] = result
                    completed_steps.add(step['id'])
                    pending_steps.remove(step)
                    progress_made = True

                    logger.info(f"步骤完成: {step['name']}")

                except Exception as e:
                    logger.error(f"步骤失败: {step['name']}, 错误: {e}")
                    pending_steps.remove(step)

            if not progress_made:
                logger.warning("工作流无法继续，存在循环依赖")
                break

        logger.info(f"工作流执行完成: {len(completed_steps)}/{len(steps)}")
        return {'results': results, 'completed': completed_steps}
