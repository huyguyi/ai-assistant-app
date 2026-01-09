"""
持久化记忆库 - 向量数据库+关系型记忆
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from agent.utils.config import config
from agent.utils.logger import Logger

# ChromaDB导入（如果不可用则使用纯内存模式）
try:
    from chromadb import ChromaDB, Collection
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    ChromaDB = None
    Collection = None


logger = Logger(__name__)


class MemoryStore:
    """持久化记忆库"""

    def __init__(self):
        """初始化记忆库"""
        self.chroma_client = None
        self.collection = None
        self.relational_memory: Dict[str, Dict[str, Any]] = {}

        if CHROMA_AVAILABLE:
            self._init_chroma()
        else:
            logger.warning("ChromaDB不可用，将使用纯内存模式")

    def _init_chroma(self):
        """初始化ChromaDB客户端"""
        try:
            self.chroma_client = ChromaDB(
                host=config.CHROMA_HOST,
                port=config.CHROMA_PORT
            )

            self.collection = self.chroma_client.get_or_create_collection(
                name="sui_agent_memories"
            )

            logger.info("ChromaDB初始化成功")
        except Exception as e:
            logger.warning(f"ChromaDB初始化失败: {e}")

    async def add(
        self,
        content: str,
        metadata: Dict[str, Any],
        importance: float = 0.5
    ) -> str:
        """添加记忆"""
        memory_id = f"mem_{datetime.now().timestamp()}_{hash(content)}"

        memory = {
            'id': memory_id,
            'content': content,
            'metadata': {
                **metadata,
                'importance': importance,
                'timestamp': datetime.now().isoformat()
            },
            'timestamp': datetime.now()
        }

        # 存储到关系型记忆
        self.relational_memory[memory_id] = memory

        # 存储到向量数据库
        if self.collection:
            try:
                self.collection.add(
                    ids=[memory_id],
                    documents=[content],
                    metadatas=[memory['metadata']]
                )
            except Exception as e:
                logger.warning(f"向量存储失败: {e}")

        logger.debug(f"记忆已添加: {memory_id}")
        return memory_id

    async def semantic_search(
        self,
        query: str,
        limit: int = 10,
        min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """语义检索"""
        if not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit * 2  # 获取更多候选，然后过滤
            )
        except Exception as e:
            logger.error(f"语义检索失败: {e}")
            return []

        memories = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                memory_id = results['ids'][0][i]
                metadata = results['metadatas'][0][i]

                # 检查重要性阈值
                if metadata.get('importance', 0) < min_importance:
                    continue

                memory = self.relational_memory.get(memory_id)
                if memory:
                    memories.append(memory)

        logger.debug(f"语义检索完成，找到 {len(memories)} 条记忆")
        return memories[:limit]

    async def search_by_metadata(
        self,
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """按元数据检索"""
        results = []

        for memory in self.relational_memory.values():
            match = True
            for key, value in filters.items():
                if memory['metadata'].get(key) != value:
                    match = False
                    break

            if match:
                results.append(memory)

        logger.debug(f"元数据检索完成，找到 {len(results)} 条记忆")
        return results

    async def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """获取记忆"""
        return self.relational_memory.get(memory_id)

    async def cleanup_old_memories(
        self,
        days: int = 30,
        min_importance: float = 0.3
    ) -> int:
        """清理旧记忆"""
        cutoff = datetime.now() - timedelta(days=days)
        deleted_count = 0

        for memory_id, memory in list(self.relational_memory.items()):
            if (
                memory['timestamp'] < cutoff and
                memory['metadata'].get('importance', 0) < min_importance
            ):
                del self.relational_memory[memory_id]

                if self.collection:
                    try:
                        self.collection.delete(ids=[memory_id])
                    except Exception as e:
                        logger.warning(f"向量删除失败: {e}")

                deleted_count += 1

        logger.info(f"清理旧记忆完成，删除 {deleted_count} 条")
        return deleted_count

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        by_importance = {}

        for memory in self.relational_memory.values():
            importance = memory['metadata'].get('importance', 0.5)
            key = f"{importance:.1f}"
            by_importance[key] = by_importance.get(key, 0) + 1

        return {
            'total': len(self.relational_memory),
            'by_importance': by_importance
        }


# 全局实例
_memory_store_instance = None

def get_memory_store():
    """获取记忆库实例"""
    global _memory_store_instance
    if _memory_store_instance is None:
        _memory_store_instance = MemoryStore()
    return _memory_store_instance


memory_store = get_memory_store()
