from src.model.openai import OpenAIChatModel, OpenAIReasoningModel
from src.model.claude import ClaudeModel
from src.model.deepseek import DeepSeekModel
from src.model.gemini import GeminiReasoningModel
from src.model.doubao import Doubao

# from src.model.openai_reasoningmodel import OpenAIReasoningModel


MODEL_MAP = {
    "gpt-4.1": OpenAIChatModel,
    "gpt-4o": OpenAIChatModel,
    "gpt-4o-mini": OpenAIChatModel,
    "o1": OpenAIReasoningModel,
    "o4-mini": OpenAIReasoningModel,
    "o4-mini-high": OpenAIReasoningModel,
    "o4-mini-low": OpenAIReasoningModel,
    "o3": OpenAIReasoningModel,
    "o3-high": OpenAIReasoningModel,
    "o3-low": OpenAIReasoningModel,
    "o3-mini":OpenAIReasoningModel,
    "o3-mini-high":OpenAIReasoningModel,
    "o3-mini-low":OpenAIReasoningModel,
    "claude-opus-4-7": ClaudeModel,
    "claude-opus-4-7-thinking": ClaudeModel,
    "claude-3.7-sonnet": ClaudeModel,
    "claude-3.7-sonnet-thinking": ClaudeModel,
    "claude-4.0-sonnet": ClaudeModel,
    "claude-4.0-sonnet-thinking": ClaudeModel,
    'gemini-2.5-pro-preview': GeminiReasoningModel,
    'gemini-3.1-pro-preview': GeminiReasoningModel,
    'deepseek-v3': DeepSeekModel,
    'deepseek-r1': DeepSeekModel,
    'deepseek-chat': DeepSeekModel,
    'deepseek-reasoner': DeepSeekModel,
    'doubao-seed-1.6': Doubao,
    'doubao-seed-1.6-thinking': Doubao
}
