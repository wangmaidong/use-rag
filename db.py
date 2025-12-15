import chromadb
from chromadb import PersistentClient
from typing import Optional
import logging
from sentence_transformers import SentenceTransformer
logger = logging.getLogger(__name__)
# 设置默认的集合名称
DEFAULT_COLLECTION_NAME = "rag"
# 设置默认的模型名称
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
# 设置默认的数据库文件路径
DEFAULT_DB_PATH = "./chroma_db"

_model:Optional[SentenceTransformer] = None
_client:Optional[chromadb.PersistentClient] = None

def _get_model() -> SentenceTransformer:
    """
    获取嵌入模型实例（单例模式）
    返回:
        SentenceTransformer: 嵌入模型实例
    """
    global _model
    if _model is None:
        logger.info(f"正在加载嵌入模型：{DEFAULT_MODEL_NAME}")
        _model = SentenceTransformer(DEFAULT_MODEL_NAME)
        logger.info("嵌入模型加载完成")
    return _model

def _get_client() -> chromadb.PersistentClient:
    """
    获取ChromaDB客户端实例（单例模式）
    返回:
        chromadb.PersistentClient: 客户端实例
    """
    global _client
    if _client is None:
        # 记录开始初始化客户端的日志，并输出路径信息
        logger.info(f"正在初始化ChromaDB客户端，路径: {DEFAULT_DB_PATH}")
        _client = chromadb.PersistentClient(path=DEFAULT_DB_PATH)
        # 记录客户端初始化完成的日志
        logger.info("ChromaDB客户端初始化完成")
    return _client

def save_text_to_db(text: str, collection_name: str = DEFAULT_COLLECTION_NAME, source:Optional[str] = None) -> str:
    """
    将文本保存到ChromaDB指定集合中，使用sentence_transformers生成embedding。

    参数:
        text (str): 要保存的文本
        collection_name (str): 集合名称，默认为 "rag"
        source (str, optional): 数据来源标识，默认为 "document"

    返回:
        str: 保存的文本ID

    异常:
        Exception: 保存失败
    """
    try:
        # 如果文本为空或者全是空白字符，直接记录警告并返回空字符串
        if not text or not text.strip():
            logger.warning("尝试保存空文本，已跳过")
            return ""
        model = _get_model()
        client = _get_client()
        collection = client.get_or_create_collection(collection_name)
        text_id = str
    except Exception as e:
        logger.error(f"保存文本到数据库失败: {str(e)}")
        raise