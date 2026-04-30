import logging
import anthropic
import os
import dotenv
from typing import Dict, Any
from .base_model import BaseModel
dotenv.load_dotenv()



class ClaudeModel(BaseModel):
    def __init__(self, model_config: Dict[str, Any], system_prompt: str=""):
        super().__init__(model_config)
        self.system_prompt = system_prompt
        self.init_client()
        self.messages = []
        self.thinking = model_config['thinking']
    
    def init_prompt(self):
        self.messages = []
        
    def init_client(self):
        if self.client_type == 'anthropic_aws':
            self.client = anthropic.AnthropicBedrock(
                aws_region=os.getenv("AWS_REGION"),
                aws_access_key=os.getenv("AWS_ACCESS_KEY"),
                aws_secret_key=os.getenv("AWS_SECRET_KEY")
            )
        elif self.client_type == 'anthropic':
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
      
        else:
            raise ValueError(f"Invalid client type: {self.client_type}")    
    
    def get_response(self) -> str:
        if self.thinking:
            # Opus 4.7+ uses adaptive thinking; older models use enabled+budget_tokens
            if "opus-4" in self.deployment:
                thinking_param = {"type": "adaptive"}
            else:
                thinking_param = {"type": "enabled", "budget_tokens": 4000}

            with self.client.messages.stream(
                model=self.deployment,
                max_tokens=16000,
                system=self.system_prompt,
                thinking=thinking_param,
                messages=self.messages,
            ) as stream:
                thinking_started = False
                thinking = ""
                answer = ""
                response_started = False
                for event in stream:
                    # print(event)
                    if event.type == "content_block_start":
                        thinking_started = False
                        response_started = False
                    elif event.type == "content_block_delta":
                        if event.delta.type == "thinking_delta":
                            if not thinking_started:
                                thinking_started = True
                            # print(event.delta.thinking, end="", flush=True)
                            thinking += event.delta.thinking

                        elif event.delta.type == "text_delta":
                            if not response_started:
                                response_started = True
                            # print(event.delta.text, end="", flush=True)
                            answer += event.delta.text
        

            return {
                    'thinking': thinking,
                    'answer': answer
                }
            
            

                 
        else:
            response = self.client.messages.create(
                    model=self.deployment,
                    system=self.system_prompt,
                    messages=self.messages,
                    max_tokens=15000
                )
            return {
                "thinking": "",
                "answer": response.content[0].text
            }
                
        

    def dump_messages(self):  # type: ignore[override]
        return self.messages

    def load_messages(self, messages):  # type: ignore[override]
        self.messages = list(messages) if messages else []
    
    
    