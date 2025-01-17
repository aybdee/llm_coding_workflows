from pydantic import BaseModel, Field


class Program(BaseModel):
    chain_of_thought: str = Field(
        ..., description="Your thought process for solving the problem using code"
    )
    program: str = Field(
        ..., description="a python program to complete the required task"
    )


class Review(BaseModel):
    chain_of_thought: str = Field(
        ..., description="Your thought process for reviewing the code problem"
    )
    recommendations: str = Field(
        ...,
        description="a list of recommended recommended changes to make to the program",
    )

    score: int = Field(
        ..., description="a number between 0 and 1 for how good the solution is"
    )
