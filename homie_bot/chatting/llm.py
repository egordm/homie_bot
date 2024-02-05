import os

from langchain_community.chat_models import ChatOllama
from transformers import PreTrainedTokenizer, AutoTokenizer

llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    temperature=0.7,
    # repeat_last_n=1024,
    # repeat_penalty=1.05,
)

tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(os.environ["TOKENIZER_MODEL"])


def token_count_fn(x: str) -> int:
    return len(tokenizer.encode(x, add_special_tokens=False))
