"""
日志工具模块
"""

import sys
from loguru import logger as loguru_logger
from agent.utils.config import config


class Logger:
    """日志包装器"""

    def __init__(self, name: str):
        self.name = name

    def info(self, message: str, **kwargs):
        """Info级别日志"""
        loguru_logger.info(f"[{self.name}] {message}", **kwargs)

    def debug(self, message: str, **kwargs):
        """Debug级别日志"""
        loguru_logger.debug(f"[{self.name}] {message}", **kwargs)

    def warning(self, message: str, **kwargs):
        """Warning级别日志"""
        loguru_logger.warning(f"[{self.name}] {message}", **kwargs)

    def error(self, message: str, **kwargs):
        """Error级别日志"""
        loguru_logger.error(f"[{self.name}] {message}", **kwargs)

    def success(self, message: str, **kwargs):
        """Success级别日志"""
        loguru_logger.success(f"[{self.name}] {message}", **kwargs)


def setup_logger():
    """配置日志系统"""
    loguru_logger.remove()  # 移除默认handler

    # 控制台输出
    loguru_logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.LOG_LEVEL
    )

    # 文件输出
    loguru_logger.add(
        "logs/sui_agent_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="7 days",
        level="DEBUG"
    )


# 初始化日志
setup_logger()
