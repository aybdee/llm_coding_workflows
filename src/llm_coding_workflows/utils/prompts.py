from typing import List
from llm_coding_workflows.models import Program, Review


def program_prompt(program: Program):
    return f"""{program.chain_of_thought} here is the program {program.program}"""


def reviewer_prompt(review: Review):
    return f"""{review.chain_of_thought}.\n These are my recommendations: {review.recommendations} and i would score this program {review.score} out of 10"""


def create_prompt_with_history(
    system_message: str, text: str, history: List, assistant_key: str
):
    prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n"
    for completion in history:
        if completion["key"] == assistant_key:
            prompt += f"<|im_start|>assistant\n{completion["response"]}<|im_end|>\n"
        else:
            prompt += f"<|im_start|>user\n{completion["natural"]}<|im_end|>\n"

    prompt += f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant"
    return prompt


def create_prompt(system_message: str, text: str):
    return f"<|im_start|>system\n{system_message}<|im_end|>\n<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant"
