# LESSON 4: Conversation Memory
# The problem: LLMs have NO memory by default.
# Each .invoke() call is completely independent — the AI forgets everything.
#
# The solution: manually pass the conversation history with every message.
# LangChain's ChatMessageHistory and RunnableWithMessageHistory do this for us.
#
# Run this file: python 04_chatbot_memory.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# ─────────────────────────────────────────────
# THE MEMORY PROBLEM — demonstrating it first
# ─────────────────────────────────────────────

print("=== WITHOUT MEMORY ===")
print("Turn 1:", llm.invoke("My name is Akram.").content)
print("Turn 2:", llm.invoke("What is my name?").content)
# The AI will say it doesn't know your name — each call is isolated!


# ─────────────────────────────────────────────
# MANUAL MEMORY — the simple way to understand it
# We keep a Python list of messages and grow it each turn.
# ─────────────────────────────────────────────

print("\n=== MANUAL MEMORY ===")
from langchain_core.messages import SystemMessage

history = [
    SystemMessage(content="You are a helpful assistant. Remember what the user tells you.")
]

def chat_manual(user_input):
    history.append(HumanMessage(content=user_input))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))  # save AI reply too!
    return response.content

print("Turn 1:", chat_manual("My name is Akram and I love pizza."))
print("Turn 2:", chat_manual("What's my name?"))
print("Turn 3:", chat_manual("What food do I like?"))
# Now it remembers! Because we're sending the full history each time.


# ─────────────────────────────────────────────
# LANGCHAIN'S BUILT-IN MEMORY HELPER
# ChatMessageHistory is a clean wrapper around that list.
# MessagesPlaceholder inserts the history into the prompt automatically.
# ─────────────────────────────────────────────

print("\n=== LANGCHAIN MEMORY ===")

# MessagesPlaceholder is a slot in the prompt that gets filled with history
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly assistant with a good memory."),
    MessagesPlaceholder(variable_name="chat_history"),  # ← history goes here
    ("human", "{user_input}"),
])

chain = prompt | llm | StrOutputParser()

# ChatMessageHistory stores messages in memory (RAM — lost when script ends)
chat_history = ChatMessageHistory()

def chat(user_input):
    # Run the chain, passing current history
    response = chain.invoke({
        "chat_history": chat_history.messages,
        "user_input": user_input,
    })
    # Save this exchange to history for next turn
    chat_history.add_user_message(user_input)
    chat_history.add_ai_message(response)
    return response

print("Turn 1:", chat("My favorite color is blue."))
print("Turn 2:", chat("I also have a dog named Max."))
print("Turn 3:", chat("What do you know about me so far?"))


# ─────────────────────────────────────────────
# WHAT HAPPENS TO MEMORY?
#
# The chat_history object lives in RAM — it resets when the script ends.
# For a real app, you'd save history to a database or file.
# But for learning, this is all you need.
#
# Also: history grows with every message, and LLMs have a context limit
# (max tokens). For long conversations, you'd need to summarize old messages.
# LangChain has tools for that too — but that's an advanced topic.
# ─────────────────────────────────────────────

print("\n--- Full conversation history ---")
for msg in chat_history.messages:
    role = "You" if isinstance(msg, HumanMessage) else "AI"
    print(f"[{role}]: {msg.content[:80]}...")   # truncate long messages

print("\n✓ Lesson 4 complete! You understand conversation memory.")
print("→ Next: run python 05_chatbot_final.py")
