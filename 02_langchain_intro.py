# LESSON 2: LangChain Introduction — Your First LLM Call
# LangChain is a framework that makes it easy to build apps with AI models.
# Think of it as a set of LEGO bricks for AI.
#
# Run this file: python 02_langchain_intro.py

import os
from dotenv import load_dotenv

# Load the OPENAI_API_KEY from your .env file
load_dotenv()

# ─────────────────────────────────────────────
# WHAT IS AN LLM?
# LLM = Large Language Model (e.g. GPT-4, Claude, Gemini)
# It's the AI brain. You send it text, it sends text back.
# LangChain gives you a simple, consistent way to talk to any LLM.
# ─────────────────────────────────────────────

from langchain_openai import ChatOpenAI

# Create an LLM object — this is your connection to GPT
llm = ChatOpenAI(
    model="gpt-4o-mini",    # cheap and fast model, great for learning
    temperature=0.7,        # 0 = robotic/predictable, 1 = creative/random
)

# ─────────────────────────────────────────────
# MAKING YOUR FIRST CALL
# .invoke() sends a message and returns the response.
# ─────────────────────────────────────────────

print("Sending a message to the AI...")
response = llm.invoke("What is LangChain in one sentence?")

# The response is an AIMessage object (a class from LangChain)
print(type(response))           # <class 'langchain_core.messages.ai.AIMessage'>
print(response.content)         # The actual text answer


# ─────────────────────────────────────────────
# MESSAGE TYPES
# LangChain uses different message types to simulate a real conversation:
#   HumanMessage  = what the user says
#   AIMessage     = what the AI responds
#   SystemMessage = background instructions for the AI (invisible to user)
# ─────────────────────────────────────────────

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful cooking assistant. Be concise."),
    HumanMessage(content="How do I boil an egg?"),
]

response = llm.invoke(messages)
print("\n--- Cooking assistant response ---")
print(response.content)


# ─────────────────────────────────────────────
# WHY USE LANGCHAIN INSTEAD OF THE OPENAI LIBRARY DIRECTLY?
#
# Without LangChain (raw OpenAI SDK):
#   client.chat.completions.create(model="gpt-4o-mini", messages=[...])
#
# With LangChain:
#   llm.invoke(messages)
#
# Same result — but LangChain gives you:
#   • Prompt templates (Lesson 3)
#   • Conversation memory (Lesson 4)
#   • Chains (combine multiple steps)
#   • Agents (AI that uses tools)
#   • Easy model swapping (switch OpenAI → Anthropic with 1 line change)
# ─────────────────────────────────────────────

print("\n✓ Lesson 2 complete! You called an LLM for the first time.")
print("→ Next: run python 03_prompts_and_chains.py")
