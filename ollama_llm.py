import requests
import json
import random
import re

default_prompt = ''''''
    
class Ollama:
    def __init__(self, model_name="deepseek-r1:7b", base_url="http://localhost:11434", prompt=None):
        """初始化qwen模型
        
        Args:
            model_name (str): Ollama模型名称，默认为qwen3:4b
            base_url (str): Ollama服务地址，默认为http://localhost:11434
            prompt (str): 系统提示词，默认为None
        """
        self.model_name = model_name
        self.base_url = base_url
        self.initialize(prompt)
        
    def initialize(self, prompt=None):
        """重置对话，清空历史消息。如果有提示，添加提示。
        
        Args:
            prompt (str): 提示信息，默认为 None。
            
        Returns:
            None
        """
        if prompt:
            self.messages = [{"role": "system", "content": prompt}]
        else:
            self.messages = [{"role": "system", "content": default_prompt}]
            
    def chat(self, prompt):
        """与Ollama模型对话

        Args:
            prompt (str): 用户输入
            
        Returns:
            str: 模型回复（去除思考过程）
        """
        self.messages.append({"role": "user", "content": prompt})
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": self.messages,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "seed": random.randint(0, 1000)
            }
        }
        
        try:
            # 发送请求到Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            full_reply = result["message"]["content"]
            
            # 保存完整对话历史
            self.messages.append({"role": "assistant", "content": full_reply})
            
            # 提取最终回复内容（去除思考过程）
            final_reply = self._extract_final_reply(full_reply)
            return final_reply
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            return "抱歉，我现在无法回复，请稍后再试。"
            
    def _extract_final_reply(self, full_reply):
        """从完整回复中提取最终回复内容（去除思考过程）
        
        Args:
            full_reply (str): 包含思考过程的完整回复
            
        Returns:
            str: 去除思考过程后的最终回复
        """
        # 使用正则表达式移除<think>和</think>之间的内容
        final_reply = re.sub(r'<think>.*?</think>', '', full_reply, flags=re.DOTALL)
        # 清理多余的空行和空格
        final_reply = re.sub(r'\n\s*\n', '\n', final_reply).strip()
        return final_reply
