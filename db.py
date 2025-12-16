# 导入chromadb库
import chromadb
# 导入Optional类型
from typing import Optional
# 导入 logging 模块，用于记录日志
import logging

from huggingface_hub import metadata_save
# 导入 sentence_transformers 库中的 SentenceTransformer 类
from sentence_transformers import SentenceTransformer
# 导入hash计算唯一id
import hashlib

logger = logging.getLogger(__name__)
# 设置默认的集合名称
DEFAULT_COLLECTION_NAME = "rag"
# 设置默认的模型名称
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
# 设置默认的数据库文件路径
DEFAULT_DB_PATH = "./chroma_db"

# 定义全局变量 _model，用于存放 SentenceTransformer 实例，初始为 None
_model: Optional[SentenceTransformer] = None
# 定义全局变量 _client，用于存放 chromadb 的 PersistentClient 实例，初始为 None
_client: Optional[chromadb.PersistentClient] = None

def _get_model() -> SentenceTransformer:
    """
    获取嵌入模型实例（单例模式）
    返回:
        SentenceTransformer: 嵌入模型实例
    """
    # 声明使用全局变量 _model
    global _model
    if _model is None:
        logger.info(f"正在加载嵌入模型：{DEFAULT_MODEL_NAME}")
        _model = SentenceTransformer(DEFAULT_MODEL_NAME)
        logger.info("嵌入模型加载完成")
    return _model

def _get_client():
    """
    获取ChromaDB客户端实例（单例模式）
    返回:
        chromadb.PersistentClient: 客户端实例
    """
    global _client
    if _client is None:
        logger.info(f"正在初始化Chromadb客户端,路径：{DEFAULT_DB_PATH}")
        _client = chromadb.PersistentClient(path = DEFAULT_DB_PATH)
        logger.info("Chromadb客户端初始化完成")
    return _client

def save_text_to_db(text:str, collection_name:str = DEFAULT_COLLECTION_NAME, source:Optional[str] = None) -> str:
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

        # 获取全局模型实例
        model = _get_model()
        # 获取全局客户端实例
        client = _get_client()
        # 获取指定名称的集合，如果集合不存在就创建集合
        collection = client.get_or_create_collection(collection_name)
        # 使用文本内容的哈希值生成唯一的文本ID（）
        # text.encode() 将字符串转换为字节串（bytes）
        # hexdigest() 转换为十六进制字符串
        text_id = hashlib.md5(text.encode()).hexdigest()
        # 检查数据库中是否已存在相同的ID
        existing = collection.get(ids = [text_id])
        if existing and existing.get("ids"):
            logger.debug(f"文本已存在，跳过保存，id={text_id}")
            return text_id
        # 生成文本的 embedding，模型处理结果为 ndarray，通过tolist 转换为列表
        embedding = model.encode([text])[0].tolist()
        # 向集合中添加文本、元数据、ID以及embedding
        collection.add(
            documents = [text],
            metadatas = [{"source": source or "document"}],
            ids = [text_id],
            embeddings = [embedding]
        )
        # 记录成功保存的调试日志，包含文本id和集合名称
        logger.debug(f"文本已保存到ChromaDB，id={text_id}, collection={collection_name}")
        # 返回本次保存的文本ID
        return text_id
    except Exception as e:
        # 记录错误日志并输出异常信息
        logger.error(f"保存文本到数据库失败：{str(e)}")
        raise

