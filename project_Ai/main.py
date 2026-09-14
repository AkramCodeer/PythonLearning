from fastapi import FastAPI, HTTPException

from rag_service import (
    RAGServiceUnavailableError,
    answer_question,
)
from schemas import QuestionRequest, QuestionResponse

app = FastAPI(
    title="AI Support Knowledge Base",
    description="A retrieval-augmented support assistant",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post(
    "/questions",
    response_model=QuestionResponse,
)
def ask_question(request: QuestionRequest):
    try:
        return answer_question(request.question)
    except RAGServiceUnavailableError as error:
        raise HTTPException(
            status_code=503,
            detail="The AI service is temporarily unavailable.",
        ) from error
