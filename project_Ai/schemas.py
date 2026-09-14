from pydantic import BaseModel, ConfigDict, Field, field_validator


class QuestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(max_length=500)

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned_value = value.strip()

        if len(cleaned_value) < 3:
            raise ValueError("Question must be at least 3 characters long.")

        return cleaned_value


class SourceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str


class QuestionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str
    answer: str
    source: SourceResponse | None = None
    similarity: float | None = Field(
        default=None,
        ge=-1,
        le=1,
    )
