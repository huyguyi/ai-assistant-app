#!/usr/bin/env python3
"""
燧石Agent系统 - 主入口文件

基于国产大模型的世界级Agent系统
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from agent.core.llm import CoreLLMEngine, core_llm
from agent.core.memory import MemoryStore, memory_store
from agent.agents.monitor import CustomerMonitorAgent
from agent.agents.rednote import RedNoteAgent
from agent.agents.product import ProductManagerAgent
from agent.core.orchestrator import CoordinatorAgent
from agent.utils.logger import logger
from agent.utils.config import config


class SuiAgentSystem:
    """燧石Agent系统主类"""

    def __init__(self):
        """初始化系统"""
        self.llm_engine = None
        self.agents = {}
        self.coordinator = None

    async def initialize(self):
        """初始化系统组件"""
        logger.info("=" * 60)
        logger.info("燧石Agent系统启动")
        logger.info("=" * 60)

        # 显示配置
        provider = config.get('CORE_LLM_PROVIDER', 'qwen')
        logger.info(f"核心模型提供商: {provider.upper()}")

        # 初始化核心引擎
        try:
            self.llm_engine = CoreLLMEngine()
            health = await self.llm_engine.health_check()

            if not health:
                logger.error("核心模型健康检查失败")
                raise RuntimeError("核心模型不可用")

            logger.info("核心引擎初始化成功")
        except Exception as e:
            logger.error(f"核心引擎初始化失败: {e}")
            raise

        # 初始化记忆库
        try:
            memory_store  # 触发初始化
            logger.info("记忆库初始化成功")
        except Exception as e:
            logger.warning(f"记忆库初始化失败（将使用纯内存模式）: {e}")

        # 初始化专业Agent
        self.agents = {
            'monitor': CustomerMonitorAgent(),
            'rednote': RedNoteAgent(),
            'product': ProductManagerAgent(),
        }
        logger.info(f"初始化 {len(self.agents)} 个专业Agent")

        # 初始化协调器
        self.coordinator = CoordinatorAgent()
        logger.info("协调器初始化成功")

        logger.info("=" * 60)
        logger.info("系统初始化完成")
        logger.info("=" * 60)

    async def demo_level1(self):
        """演示Level 1: 智能客服监控"""
        logger.info("\n" + "=" * 60)
        logger.info("Level 1: 智能客服监控Agent")
        logger.info("=" * 60)

        monitor = self.agents['monitor']

        # 模拟对话
        user_query = "我的订单一直没到，客服电话也打不通，真的太失望了！"
        ai_response = "非常抱歉让您久等了，您的订单已经发货，预计明天送达，我帮您查询一下物流状态"

        system_state = {
            "latency": 150,
            "error_rate": 0.02,
            "knowledge_base_hit_rate": 0.65,
            "active_conversations": 42,
            "average_response_time": 800
        }

        logger.info(f"用户查询: {user_query}")
        logger.info(f"AI回答: {ai_response}")

        # 分析对话
        analysis = await monitor.analyze_conversation(user_query, ai_response, system_state)

        logger.info(f"\n分析结果:")
        logger.info(f"  意图: {analysis['intent']}")
        logger.info(f"  情绪: {analysis['sentiment']}")
        logger.info(f"  类别: {analysis['category']}")
        logger.info(f"  状态: {analysis['status']}")
        logger.info(f"  预警触发: {analysis['alert_triggered']}")

        if analysis['alert_triggered']:
            logger.warning(f"  预警原因: {analysis.get('alert_reason', 'N/A')}")
            logger.info(f"  推荐措施: {analysis.get('recommended_actions', [])}")

        # 保存结果
        import json
        output_path = Path('outputs/result_task1.json')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'user_query': user_query,
                'ai_response': ai_response,
                'system_state': system_state,
                'analysis': analysis
            }, f, ensure_ascii=False, indent=2)
        logger.info(f"\n结果已保存到: {output_path}")

    async def demo_level2(self):
        """演示Level 2: 小红书创作"""
        logger.info("\n" + "=" * 60)
        logger.info("Level 2: 小红书RedNote-Agent")
        logger.info("=" * 60)

        rednote = self.agents['rednote']

        search_query = "春季护肤 油皮 小红书"
        product_info = {
            "name": "清透水感保湿乳",
            "category": "护肤品",
            "features": [
                "轻质水感配方",
                "快速吸收不粘腻",
                "控油保湿双效",
                "适合油性混合性肌肤"
            ],
            "target_audience": "18-35岁油性肌肤的年轻女性"
        }

        logger.info(f"搜索关键词: {search_query}")
        logger.info(f"产品名称: {product_info['name']}")

        # 执行完整工作流
        result = await rednote.run_full_workflow(search_query, product_info)

        logger.info(f"\n文案生成完成:")
        logger.info(f"  标题: {result['optimized_draft']['title']}")
        logger.info(f"  正文长度: {len(result['optimized_draft']['content'])} 字")
        logger.info(f"  标签数量: {len(result['optimized_draft']['tags'])}")

        # 保存结果
        import json
        output_path = Path('outputs/result_task2.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"\n结果已保存到: {output_path}")

    async def demo_level3(self):
        """演示Level 3: 产品经理"""
        logger.info("\n" + "=" * 60)
        logger.info("Level 3: 产品经理Agent")
        logger.info("=" * 60)

        product = self.agents['product']

        initial_requirement = "做一个帮人省钱的App"

        logger.info(f"原始需求: {initial_requirement}")

        # 执行完整工作流
        result = await product.run_full_workflow(initial_requirement)

        logger.info(f"\nPRD生成完成:")
        logger.info(f"  项目概述: {result['prd']['project_overview'][:50]}...")
        logger.info(f"  痛点数量: {len(result['prd']['core_pain_points'])}")
        logger.info(f"  功能数量: {len(result['prd']['features'])}")
        logger.info(f"  校验得分: {result['validation']['score']}/100")

        # 保存结果
        import json
        output_path = Path('outputs/result_task3.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        logger.info(f"\n结果已保存到: {output_path}")

        # 生成PRD文档
        prd_path = Path('outputs/generated_prd_task3.md')
        self._generate_prd_document(result['prd'], prd_path)
        logger.info(f"PRD文档已保存到: {prd_path}")

    def _generate_prd_document(self, prd, output_path):
        """生成PRD Markdown文档"""
        content = f"""# {prd['project_overview']}

## 目标用户
{chr(10).join(f"- {user}" for user in prd['target_users'])}

## 核心痛点

{chr(10).join(f"- **{point['point']}** (优先级: {point['priority']}){chr(10)}  {chr(10).join(f'    - {story}' for story in point['user_stories'])}" for point in prd['core_pain_points'])}

## 功能设计

{chr(10).join(f"### {feature['name']}{chr(10)}{feature['description']}{chr(10)}- 对应痛点: {', '.join(feature['mapped_pain_points'])}{chr(10)}- 用户流程: {feature['user_flow']}" for feature in prd['features'])}

## 成功指标

{chr(10).join(f"- {metric}" for metric in prd['success_metrics'])}
"""

        output_path.write_text(content, encoding='utf-8')

    async def run_all_demos(self):
        """运行所有演示"""
        try:
            await self.initialize()

            await self.demo_level1()
            await self.demo_level2()
            await self.demo_level3()

            logger.info("\n" + "=" * 60)
            logger.info("所有演示完成!")
            logger.info("=" * 60)

        except KeyboardInterrupt:
            logger.info("用户中断")
        except Exception as e:
            logger.error(f"运行出错: {e}")
            raise


async def main():
    """主函数"""
    system = SuiAgentSystem()

    # 检查命令行参数
    import sys
    if len(sys.argv) > 1:
        task = sys.argv[1]
        await system.initialize()

        if task == 'task1':
            await system.demo_level1()
        elif task == 'task2':
            await system.demo_level2()
        elif task == 'task3':
            await system.demo_level3()
        else:
            logger.error(f"未知任务: {task}")
            logger.info("用法: python main.py [task1|task2|task3]")
    else:
        # 运行所有演示
        await system.run_all_demos()


if __name__ == "__main__":
    asyncio.run(main())
