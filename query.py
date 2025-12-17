# 导入sentence_transformers库中的SentenceTransformer类
from sentence_transformers import SentenceTransformer
# 导入chromadb
import chromadb
# 从typing库导入List和Optional类型
from typing import List, Optional
# 导入logging库用于日志记录
import logging
# 导入llm模块（自定义的大模型API封装）
import llm
# 配置日志：设置日志等级为INFO,指定日志格式
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s %(message)s]"
)

logger = logging.getLogger(__name__)
# 默认集合名称，存储块的标签名
DEFAULT_COLLECTION_NAME = "rag"
# 默认嵌入模型名称
DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
# 默认chroma数据路径
DEFAULT_DB_PATH = "./chroma_db"
# 默认检索返回文本块数目
DEFAULT_N_RESULTS = 3

# 全局SentenceTransformer模型实例
_model: Optional[SentenceTransformer] = None
# 全局Chromadb客户端实例
_client: Optional[chromadb.PersistentClient] = None
# 全局Chromadb集合实例
_collection: Optional[chromadb.Collection] = None

def _get_model():
    global _model
    if _model is None:
        logger.info(f"正在加载嵌入模型：{DEFAULT_MODEL_NAME}")
        _model = SentenceTransformer(DEFAULT_MODEL_NAME)
        logger.info("模型加载完成")

    return _model

def _get_client():
    global _client
    if _client is None:
        logger.info(f"正在初始化ChromaDB客户端，路径：{DEFAULT_DB_PATH}")
        _client = chromadb.PersistentClient(path=DEFAULT_DB_PATH)
        logger.info(f"Chromadb客户端初始化完成")
    return _client

def _get_collection(collection_name:str = DEFAULT_COLLECTION_NAME):
    global _collection
    if _collection is None:
        client = _get_client()
        logger.info(f"正在获取或创建集合：{collection_name}")
        _collection = client.get_or_create_collection(collection_name)
        logger.info(f"集合{collection_name} 已准备就绪")
    return _collection

# 将query字符串转为embedding向量
def get_query_embedding(query:str) -> List[float]:
    """
    将查询文本转换为embedding向量

    参数:
        query (str): 查询文本

    返回:
        List[float]: embedding向量
    """
    # 打印debug信息，开始向量化
    logger.debug("正在将Query转为向量")
    model = _get_model()
    embedding = model.encode(query).tolist()
    logger.debug(f"Query向量化完成，向量维度：{len(embedding)}")
    return embedding

# 向量检索，返回最相关的文本块列表
def retrieve_related_chunks(
        query_embedding: List[float],
        n_results: int = DEFAULT_N_RESULTS,
        collection_name:str = DEFAULT_COLLECTION_NAME
) -> List[str]:
    """
     向量检索，返回最相关的文本块列表

    参数:
        query_embedding (List[float]): 查询向量
        n_results (int): 返回的结果数量，默认为3
        collection_name (str): 集合名称，默认为 "rag"

    返回:
        List[str]: 最相关的文本块列表

    异常:
        ValueError: 未检索到相关内容
    """
    try:
        logger.info(f"正在进行向量检索，返回最相关的{n_results}个文本块")
        collection = _get_collection(collection_name)
        results = collection.query(
            query_embeddings = [query_embedding],
            n_results= n_results
        )
        print(f"从数据库查到的原始结果：{results}")
        related_chunks = results.get("documents")
        # 检查是否检索到相关内容
        if not related_chunks or not related_chunks[0]:
            logger.warning("未检索到相关内容，请先入库或检查数据库！")
            raise ValueError("未检索到相关内容，请先入库或检查数据库！")
        # 打印检索到的文本块数量
        logger.info(f"成功检索到{len(related_chunks[0])}个相关文本块")
        # 返回第一个结果list（按设计，一个query只查一个batch，取[0]即可）
        return related_chunks[0]

    except Exception as e:
        logger.error(f"向量检索失败：{str(e)}")
        raise

def query_rag(
        query: str,
        n_results: int = DEFAULT_N_RESULTS,
        collection_name:str = DEFAULT_COLLECTION_NAME
) -> str:
    """
    RAG查询主函数：向量检索 + LLM生成答案

    参数:
        query (str): 用户查询问题
        n_results (int): 检索的文档块数量，默认为3
        collection_name (str): 集合名称，默认为 "rag"

    返回:
        str: LLM生成的答案

    异常:
        ValueError: 检索失败或未找到相关内容
    """
    try:
        # 打印RAG查询日志
        logger.info(f"开始RAG查询：{query}")
        # 步骤1：将查询文本转为向量
        quer_embedding = get_query_embedding(query)
        # 步骤2：基于query embedding做向量检索
        related_chunks = retrieve_related_chunks(
            quer_embedding,
            n_results,
            collection_name
        )
        # 步骤3：将检索到的文本块合并为上下文，拼接prompt
        context = "\n".join(related_chunks)
        prompt = f"已知信息：\n{context}\n\n请根据上述内容回答用户问题：{query}"
        # 打印构建的prompt长度
        logger.debug(f"Prompt已构建，长度: {len(prompt)}")
        # 步骤4：调用llm.invoke（大语言模型调用）生成最终答案
        logger.info("正在调用大模型生成答案...")
        answer = llm.invoke(prompt)
        # 打印答案生成完成
        logger.info("答案生成完成")

        # 返回模型生成的答案
        return answer
    except ValueError as e:
        logger.error(f"RAG查询失败：{str(e)}")
        raise
    except Exception as e:
        logger.error(f"RAG查询过程中发生错误：{str(e)}")
        raise

if __name__ == "__main__":
    query = "红楼梦的作者是谁？"
    logger.info(f"用户查询：{query}")
    try:
        # 进行RAG查询，设置n_results为10
        answer = query_rag(query)
        # 打印结果
        print("\n【答案】\n", answer)
    except ValueError as e:
        # 捕获未找到相关内容的错误，打印提示
        print(f"\n【错误】\n{str(e)}")
    except Exception as e:
        # 捕获程序异常，打印日志并提示
        logger.exception("程序执行失败")
        print(f"\n【错误】\n程序执行失败: {str(e)}")