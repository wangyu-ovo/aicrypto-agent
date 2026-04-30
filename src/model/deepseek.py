import openai
import httpx
import os
import dotenv
from typing import Dict, Any
dotenv.load_dotenv()

from .base_model import BaseModel

class DeepSeekModel(BaseModel):
    def __init__(self, model_config: Dict[str, Any], system_prompt: str):
        super().__init__(model_config)
        self.init_client()
        self.system_prompt = system_prompt
        self.init_prompt()
        self.is_reasoning = model_config['is_reasoning']
        
    def init_client(self):
        if self.client_type == 'tencent':
            self.client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                        base_url="https://api.lkeap.cloud.tencent.com/v1")
        elif self.client_type == 'deepseek':
            self.client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                                        base_url="https://api.deepseek.com",
                                        http_client=httpx.Client(verify=False))
        else:
            raise ValueError(f"Invalid client type: {self.client_type}")    
    
    def init_prompt(self):
        if self.system_prompt:
            self.messages = [
            {"role": "system", "content": self.system_prompt},
        ]
        else:
            self.messages = []
    
    def get_response(self) -> str:
        completion = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=self.messages,
                    max_tokens=8192,
                )
        thinking = completion.choices[0].message.reasoning_content if self.is_reasoning else ""
        answer = completion.choices[0].message.content
        return {
            'thinking': thinking,
            'answer': answer
        }
