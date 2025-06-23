# Memory and Context Usage

## Overview
This project supports two parallel interfaces for memory and context:

- **LangChain Native:** For direct use with LangChain chains/agents.
- **Custom/Modular:** For custom, modular, or serializable workflows (e.g., RAG, LangGraph).

## LangChain Native

```
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
chain = LLMChain(llm=..., memory=memory)
```

## Custom/Modular

```
from memory.custom.custom_memory import CustomMemory
memory = CustomMemory()
memory.save(...)
data = memory.to_data()
```

## Rationale
- Use LangChain memory/context for rapid prototyping and native LangChain workflows.
- Use custom memory/context for advanced, distributed, or serializable workflows.
- This split avoids confusion and keeps each interface simple and clear. 