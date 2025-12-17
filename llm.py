# 导入OpenAI客户端库
from openai import OpenAI
# 导入os库，用于读取环境变量
import os
# 导入logging库，用于记录日志
import logging
# 导入Optional类型，便于类型注解
from typing import Optional

from sympy import content

# 获取当前模块的logger日志对象
logger = logging.getLogger(__name__)
# 从环境变量获取OPENAI_BASE_URL，若未设置则使用默认地址
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com")
# 从环境变量获取OPENAI_API_KEY，若未设置则使用默认测试key（生产环境必须配置！）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_DEEP", "sk-08eff3175bbb4741a6c957650e2c0bc0")
# 从环境变量获取模型名称，若未设置则使用默认模型名
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "deepseek-chat")

# 全局OpenAI客户端实例，初始为None，延迟初始化
_client: Optional[OpenAI] = None

def _get_client() -> OpenAI:
    """
    获取OpenAI客户端实例（单例模式）
    返回:
        OpenAI: 客户端实例
    """
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY 未设置。请设置环境变量 OPENAI_API_KEY 或在代码中配置。"
            )
        # 使用指定的base_url和api_key初始化OpenAI客户端
        _client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)
        # 记录客户端初始化成功的日志
        logger.info(f"OpenAI客户端已初始化，base_url: {OPENAI_BASE_URL}")
    return _client

# 定义调用大模型的函数

def invoke(prompt:str, model:Optional[str] = None, temperature: float = 0.7) -> str:
    """
    调用大模型生成回复
    参数:
        prompt (str): 输入的提示词
        model (str, optional): 模型名称，默认使用环境变量或默认值
        temperature (float): 生成温度，默认0.7
    返回:
        str: 大模型生成的回复内容
    异常:
        ValueError: API密钥未设置
        Exception: API调用失败
    """
    try:
        # 获取OpenAI客户端对象
        client = _get_client()
        # 如果model参数为空，则使用默认模型名
        model_name = model or MODEL_NAME
        # 记录调式日志，显示模型名和prompt长度
        logger.debug(f"调用大模型，model:{model_name},prompt长度：{len(prompt)}")
        # 调用OpenAi聊天模型接口生成回复
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
            temperature=temperature,
        )
        print(f"大模型回复response：{response}")
        content = response.choices[0].message.content
        # 记录调式日志，标记恢复内容的长度
        logger.debug(f"大模型回复生成成功，长度：{len(content) if content else 0}")
        return content or ""
    except ValueError as e:
        logger.error(f"配置错误：{str(e)}")
        raise
    except Exception as e:
        logger.error(f"调用大模型失败：{str(e)}")
        raise

