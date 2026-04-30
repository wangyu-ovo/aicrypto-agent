from google import genai
from google.genai import types
import os
from typing import Dict, Any
from src.model.base_model import BaseModel

class GeminiReasoningModel(BaseModel):
    def __init__(self, model_config: Dict[str, Any], system_prompt: str):
        super().__init__(model_config)
        self.init_client()
        self.system_prompt = system_prompt
        self.init_prompt()

    def init_client(self):
        if self.client_type == 'google':
            self.client = genai.Client(
                api_key=os.environ.get("GOOGLE_API_KEY")
            )
        else:
            raise ValueError(f"Invalid client type: {self.client_type}")    
    
        
    def init_prompt(self):
        if self.system_prompt:
            self.generate_content_config = types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                max_output_tokens = 65535,
                thinking_config=types.ThinkingConfig(include_thoughts=True))
    
        else:
            self.generate_content_config = types.GenerateContentConfig(
                max_output_tokens = 65535,
                thinking_config=types.ThinkingConfig(include_thoughts=True)
            )
        
        self.messages = []
    
    
    def add_assistant_message(self, message: str):
        self.messages.append(
            types.Content(
                    role="model",
                    parts=[
                        types.Part.from_text(text=message)
                        ]
                    )
            
        )
    
    def add_user_message(self, message: str):
        self.messages.append(
            types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=message)
                        ]
                    )
            
        )
    
    def get_response(self) -> str:
        response =  self.client.models.generate_content(
            model = self.deployment,
            contents = self.messages,
            config = self.generate_content_config,
            )
        # Initialise placeholders in case the API does not return "thought" parts.
        thinking = ""
        answer = ""

        for part in response.candidates[0].content.parts:
            # Skip empty parts
            if not part.text:
                continue

            # Gemini marks internal chain-of-thought with the "thought" flag.
            if getattr(part, "thought", False):
                thinking += part.text
            else:
                answer += part.text

        return {
            'thinking': thinking,
            'answer': answer
        }

    # ------------------------------------------------------------------
    # Persistence helpers for TaskRunner resume functionality
    # ------------------------------------------------------------------

    def dump_messages(self):  # type: ignore[override]
        """Return a JSON-serialisable representation of the message list."""
        serialised = []
        for msg in self.messages:
            if not hasattr(msg, "role"):
                continue
            role = msg.role
            text = ""
            if getattr(msg, "parts", None):
                part = msg.parts[0]
                text = getattr(part, "text", "")
            serialised.append({"role": role, "content": text})
        return serialised

    def load_messages(self, messages):  # type: ignore[override]
        """Restore messages previously produced by dump_messages."""
        from google.genai import types  # local import to avoid issues if lib absent

        rebuilt = []
        for m in messages or []:
            if not isinstance(m, dict):
                continue
            role = m.get("role")
            if role == "assistant": # Add this check
                role = "model"
            content = m.get("content", "")
            rebuilt.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=content)],
                )
            )
        self.messages = rebuilt
