import json
from typing import List, Union
from pydantic import BaseModel, Field
from llm_coding_workflows.models import Program, Review
from llm_coding_workflows.utils.completions import (
    create_json_completion,
    create_text_completion,
)
from pprint import pprint
from llm_coding_workflows.utils.prompts import (
    create_prompt,
    create_prompt_with_history,
    program_prompt,
    reviewer_prompt,
)
from llm_coding_workflows.utils.pydantic_models_to_grammar import (
    generate_gbnf_grammar_and_documentation,
)


def write_program(host: str, problem: str, review: Review | None, history: List):
    tools = [Program]
    gbnf_grammar, documentation = generate_gbnf_grammar_and_documentation(
        pydantic_model_list=tools
    )
    system_message = "You are an advanced AI, that is very good at solving python programming problems think through the problem carefully and document your thought process ONLY as the chain of thought, after thinking write a python program to solve the given problem"

    if review:
        prompt = create_prompt(system_message, problem)
    else:
        prompt = create_prompt_with_history(system_message, problem, history, "write")

    json_data = create_json_completion(host, prompt, gbnf_grammar)
    program = Program(**json_data)
    return program


def review_program(host: str, program: Program, history: List):
    tools = [Review]
    gbnf_grammar, documentation = generate_gbnf_grammar_and_documentation(
        pydantic_model_list=tools
    )
    system_message = "You are an advanced AI, that is very good at reviewing programming problems look at the solution carefully and document your thought process on how good the solution is and potential provements as the chain of thought, after thinking, write a list of recommendations to improve the solution and give the solution a score between 0 and 10"
    prompt = create_prompt_with_history(
        system_message, program_prompt(program), history, "review"
    )
    json_data = create_json_completion(host, prompt, gbnf_grammar)
    review = Review(**json_data)
    return review


def solve_problem(host: str, prompt: str):
    num_passes = 0
    history = []
    review = None
    while True:
        if history and review:
            program = write_program(host, problem, review, history)
        else:
            program = write_program(host, problem, review, history)
            history.append({"key": "prompt", "natural": prompt})

        history.append(
            {
                "key": "write",
                "response": json.dumps(program.model_dump()),
                "natural": program_prompt(program),
            }
        )

        if num_passes == 2:  # manually do two passes
            return (history, program)
        review = review_program(host, program, history)
        history.append(
            {
                "action": "review",
                "response": json.dumps(review.model_dump()),
                "natural": reviewer_prompt(review),
            }
        )

        num_passes += 1


host = "172.16.23.113:8080"
problem = """
Problem: Rabbit Population Growth

You are tasked with modeling the growth of a rabbit population. The population grows according to a specific pattern:

    At the start, you have one pair of rabbits.
    Each month, every pair of rabbits that are at least two months old produces a new pair.
    The population of rabbits in any given month is the sum of the population in the two previous months.

Write a function rabbit_population(n: int) -> int that returns the total number of rabbit pairs after n months, starting with a single pair.
Input:

    An integer n (1 ≤ n ≤ 30) representing the number of months.

Output:

    Return an integer representing the total number of rabbit pairs after n months.
"""
history, program = solve_problem(host, problem)
