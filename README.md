# Python + LangChain: Chatbot Learning Path

A hands-on curriculum to go from zero Python to building real AI chatbots.

## Setup (do this first)

```bash
pip install langchain langchain-openai python-dotenv
```

Create a `.env` file in this folder:
```
OPENAI_API_KEY=your-key-here
```

## Lessons

| File | What you learn |
|------|---------------|
| [01_python_basics.py](01_python_basics.py) | Variables, functions, lists, dicts, classes |
| [02_langchain_intro.py](02_langchain_intro.py) | What LangChain is, calling an LLM for the first time |
| [03_prompts_and_chains.py](03_prompts_and_chains.py) | Prompt templates, chaining steps together |
| [04_chatbot_memory.py](04_chatbot_memory.py) | Conversation history, stateful chatbot |
| [05_chatbot_final.py](05_chatbot_final.py) | A complete, interactive terminal chatbot |

## How to run a lesson

```bash
python 01_python_basics.py
```

Work through each file top to bottom. Every concept has a comment explaining *why*, not just *what*.
