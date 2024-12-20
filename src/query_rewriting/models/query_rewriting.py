from pydantic import BaseModel

class QuestionRewriting(BaseModel):
    query: str
    rewriting_query: str