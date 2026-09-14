def build_prompt(question: str, document: dict) -> str:
    return f"""
SOURCE:
ID: {document['id']}
Title: {document['title']}

<context>
{document['content']}
</context>

<question>
{question}
</question>
""".strip()

if __name__ == "__main__":
    sample_document = {
        "id": 1,
        "title": "Password Reset",
        "content": "Users can reset their password from the account settings page.",
    }

    prompt = build_prompt("How can I reset my password?", sample_document)
    print(prompt)
