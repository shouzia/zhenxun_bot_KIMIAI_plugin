from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message, MessageEvent
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from services.log import logger
from utils.manager import withdraw_message_manager
from configs.config import Config
import requests

from openai import OpenAI

# 填写KIMI的API_KEY
client = OpenAI(
    api_key = "$MOONSHOT_API_KEY",
    base_url = "https://api.moonshot.cn/v1",
)

__zx_plugin_name__ = "KIMI"
__plugin_usage__ = """
usage：
    KIMIAI
    指令：
       @机器人 你的问题
""".strip()
__plugin_des__ = "KIMIAI"
__plugin_cmd__ = ["@机器人"]
__plugin_version__ = 0.1
__plugin_author__ = 'Shouzi'
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["@机器人"],
}

xinhuo = on_message(rule=to_me(), priority=100)
@xinhuo.handle()
async def _(bot: Bot, event: Event):
    if not isinstance(event, MessageEvent):
        return

    user_input = str(event.message)  # 获取用户发送的消息内容
    if not user_input:
        return

    # 提取用户提问的内容
    user_input = user_input.strip()

    # 检查处理后的消息是否为空
    if not user_input:
        return

    answer = chat(user_input, history)
    await xinhuo.finish(answer)


history = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
]

def chat(query, history):
    history.append({
        "role": "user",
        "content": query
    })
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=history,
        temperature=0.3,
    )
    result = completion.choices[0].message.content
    history.append({
        "role": "assistant",
        "content": result
    })
    return result
