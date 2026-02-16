from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    match_score: int = Field(description="Score from 0-100")
    missing_keywords: list[str] = Field(description="List of top 3 missing keywords")
    sentence_to_improve: str = Field(
        description="The original sentence found in the resume"
    )
    recommended_improvement: str = Field(
        description="The improved version of that sentence"
    )
    reasoning: str = Field(description="Why the improvement was recommended")
