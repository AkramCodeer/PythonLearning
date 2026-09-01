# LESSON 5: Complete Interactive Chatbot
# Everything from lessons 1-4 combined into a real chatbot you can talk to.
# This runs in your terminal — type messages and get responses.
#
# Run this file: python 05_chatbot_final.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory


# ─────────────────────────────────────────────
# CONFIGURATION — easy to customize
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful, friendly assistant named Aria.
- Be concise: keep responses to 2-3 sentences unless asked for more detail.
- Be warm and conversational.
- If you don't know something, say so honestly.
"""

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.7


# ─────────────────────────────────────────────
# BUILD THE CHATBOT AS A CLASS
# Wrapping it in a class keeps everything organized — all the chatbot's
# state (history, chain) lives in one place.
# ─────────────────────────────────────────────

class Chatbot:
    def __init__(self, system_prompt: str):
        self.llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)
        self.history = ChatMessageHistory()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{user_input}"),
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    def chat(self, user_input: str) -> str:
        response = self.chain.invoke({
            "chat_history": self.history.messages,
            "user_input": user_input,
        })
        self.history.add_user_message(user_input)
        self.history.add_ai_message(response)
        return response

    def clear_history(self):
        self.history.clear()
        print("[History cleared]")

    def show_history(self):
        if not self.history.messages:
            print("[No history yet]")
            return
        print("\n--- Conversation History ---")
        for msg in self.history.messages:
            role = "You" if msg.type == "human" else "Aria"
            print(f"[{role}]: {msg.content}")
        print("----------------------------\n")


# ─────────────────────────────────────────────
# MAIN LOOP — the interactive terminal interface
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Aria — Your AI Assistant")
    print("=" * 50)
    print("Commands:")
    print("  /clear   — clear conversation history")
    print("  /history — show full conversation")
    print("  /quit    — exit")
    print("=" * 50)
    print()

    bot = Chatbot(system_prompt=SYSTEM_PROMPT)

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Handle special commands
        if user_input == "/quit":
            print("Goodbye!")
            break
        elif user_input == "/clear":
            bot.clear_history()
            continue
        elif user_input == "/history":
            bot.show_history()
            continue

        # Get AI response
        print("Aria: ", end="", flush=True)
        response = bot.chat(user_input)
        print(response)
        print()


# This pattern means: only run main() if this file is run directly,
# not if it's imported by another file.
if __name__ == "__main__":
    main()
