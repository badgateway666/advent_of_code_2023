import os
from typing import Any

import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def get_input(day: int) -> list[str]:
    """Get the input for the day"""
    load_dotenv()
    if os.environ.get("AOC_SESSION_COOKIE") is None:
        raise ValueError("No session cookie found. Please add it to your .env file")
    r = requests.get(
        f"https://adventofcode.com/2023/day/{day}/input",
        cookies={"session": os.environ.get("AOC_SESSION_COOKIE")},  # type: ignore
    )
    return r.text.splitlines()


def submit_answer(day: int, part: int, answer: Any) -> None:
    """Submit the answer to the AoC website"""
    load_dotenv()
    if os.environ.get("AOC_SESSION_COOKIE") is None:
        raise ValueError("No session cookie found. Please add it to your .env file")
    r = requests.post(
        f"https://adventofcode.com/2023/day/{day}/answer",
        cookies={"session": os.environ.get("AOC_SESSION_COOKIE")},  # type: ignore
        data={"level": part, "answer": answer},
    )
    if r.status_code != 200:
        raise ValueError("Something went wrong")
    
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find("article").find("p").text  # type: ignore
    print(result)
