from ollama_llm import Ollama
from wxauto import WeChat
import time
import os
from dotenv import load_dotenv

# 读取相关环境变量
load_dotenv()

# 初始化Ollama模型
ollama = Ollama(
    model_name=os.getenv('OLLAMA_MODEL', 'deepseek-r1:7b'),
    base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),  # 默认本地地址
    prompt="你是一个小助理，用简洁利落的话回复人们的各种问题，回答时以txt纯文字格式，不要啰啰嗦嗦，风格像人在微信聊天那样，不要像个人机。在回复时，请将你的思考过程放在<think>和</think>标签之间，只将最终回复内容放在标签之外。"
)

# 初始化微信
wx = WeChat()

# 指定监听目标
listen_list = [
    '小号',
    '文件传输助手'
]
for i in listen_list:
    wx.AddListenChat(who=i)  # 添加监听对象

# 持续监听消息，有消息则对接Ollama模型进行回复
wait = 1  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        msg = msgs.get(chat)   # 获取消息内容
        for i in msg:
            if i.type == 'friend':
                # ===================================================
                # 处理消息逻辑
                reply = ollama.chat(i.content)
                # ===================================================
        
                # 回复消息
                chat.SendMsg(reply)  # 回复
    time.sleep(wait)
