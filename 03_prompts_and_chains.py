# LESSON 3: Prompt Templates & Chains
# Instead of hardcoding text, templates let you build prompts dynamically.
# Chains let you connect multiple steps: template → LLM → output
#
# Run this file: python 03_prompts_and_chains.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# ─────────────────────────────────────────────
# PROMPT TEMPLATES
# A template is a reusable prompt with {placeholders}.
# Same idea as Python f-strings, but for AI prompts.
# ─────────────────────────────────────────────

# This template has one variable: {topic}
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly teacher. Explain things simply."),
    ("human", "Explain {topic} in 2 sentences, like I'm 10 years old."),
])

# Fill in the template — this does NOT call the AI yet
filled_prompt = prompt.invoke({"topic": "gravity"})
print("Filled prompt messages:")
for msg in filled_prompt.messages:
    print(f"  [{msg.type}]: {msg.content}")


# ─────────────────────────────────────────────
# THE PIPE OPERATOR: |
# This is LangChain's "chain" syntax. Read it left to right:
#   prompt | llm | output_parser
#   "fill the template, send to AI, extract the text"
# ─────────────────────────────────────────────

# StrOutputParser extracts just the text string from the AI response
output_parser = StrOutputParser()

# Build the chain by connecting the pieces with |
chain = prompt | llm | output_parser

# .invoke() runs the whole pipeline in one shot
result = chain.invoke({"topic": "black holes"})
print("\n--- Simple chain result ---")
print(result)


# ─────────────────────────────────────────────
# MULTI-VARIABLE TEMPLATES
# You can have as many {variables} as you need.
# ─────────────────────────────────────────────

review_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write helpful product reviews."),
    ("human", "Write a short review of a {product} that is {adjective}."),
])

review_chain = review_prompt | llm | output_parser

review = review_chain.invoke({
    "product": "wireless keyboard",
    "adjective": "surprisingly quiet"
})
print("\n--- Product review ---")
print(review)


# ─────────────────────────────────────────────
# WHY TEMPLATES MATTER FOR CHATBOTS
# Your chatbot will need a system prompt that defines its personality.
# Using a template means you can easily customize it per user or use case.
# ─────────────────────────────────────────────

chatbot_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are {persona}. Keep responses under 3 sentences."),
    ("human", "{user_message}"),
])

chatbot_chain = chatbot_prompt | llm | output_parser

personas = [
    ("a pirate", "What time is it?"),
    ("a Shakespearean scholar", "What time is it?"),
]

print("\n--- Same question, different personas ---")
for persona, message in personas:
    answer = chatbot_chain.invoke({"persona": persona, "user_message": message})
    print(f"\n[{persona.upper()}]: {answer}")

print("\n✓ Lesson 3 complete! You understand prompts and chains.")
print("→ Next: run python 04_chatbot_memory.py")
