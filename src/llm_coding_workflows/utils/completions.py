import argparse
import datetime
import json
import logging
import textwrap
import sys
from pprint import pprint
from enum import Enum
from typing import Optional, Union, Dict
import requests


def serialize_completion_json(completion: str):
    completion = completion.strip()
    completion = completion[1 : len(completion) - 1].strip()
    # use intermediate marker for newline
    completion = "{" + completion.replace("\n", "     ") + "}"
    document: Dict = json.loads(completion)
    for key in document.keys():
        if isinstance(document[key], str):
            document[key] = document[key].replace("     ", "\n")
    return document


def create_text_completion(host, prompt):
    """Calls the /completion API on llama-server.
    See
    https://github.com/ggerganov/llama.cpp/tree/HEAD/examples/server#api-endpoints
    """
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    result = requests.post(
        f"http://{host}/completion", headers=headers, json=data
    ).json()
    assert data.get("error") is None, data
    logging.info("Result: %s", result)
    content = result["content"]
    return content


def create_json_completion(host, prompt, gbnf_grammar):
    """Calls the /completion API on llama-server.
    See
    https://github.com/ggerganov/llama.cpp/tree/HEAD/examples/server#api-endpoints
    """

    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "grammar": gbnf_grammar}
    result = requests.post(
        f"http://{host}/completion", headers=headers, json=data
    ).json()
    assert data.get("error") is None, data
    logging.info("Result: %s", result)
    content = result["content"]
    json_data = serialize_completion_json(content)
    print(json_data)
    return json_data
