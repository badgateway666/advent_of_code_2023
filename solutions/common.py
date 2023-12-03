import os
from typing import Any

from icecream import ic
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import Client

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


def request_problem_summary(day: int, store=True) -> dict[str, Any]:
    """Get the problem summary for the day"""
    load_dotenv()
    if os.environ.get("AOC_SESSION_COOKIE") is None:
        raise ValueError("No session cookie found. Please add it to your .env file")
    r = requests.get(
        f"https://adventofcode.com/2023/day/{day}",
        cookies={"session": os.environ.get("AOC_SESSION_COOKIE")},  # type: ignore
    )
    soup = BeautifulSoup(r.text, "html.parser")
    article = soup.find("article")

    title = article.find("h2").text.replace("-", "").strip() # type: ignore
    challenge_text = [ p.text.strip() for p in article.find_all("p") ] # type: ignore
    result = f"{title}\n" + "\n".join(challenge_text)

    openai_client = Client()
    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an coding assistant who is supporting a programmer, working on the advent of code challenges in python."},
            {"role": "user", "content": "The following is the current challenge text:"},
            {"role": "system", "content": result},
            {"role": "user", "content": "The following is an excerpt from the challenge input:"},
            {"role": "system", "content": "\n".join(get_input(day=day)[:10])},
            {"role": "user", "content": "Please extract important information and summarize them. Provide the summary in markdown format with an introduction and a conclusion, and a list of bullet points in between. Also, mention things to watch out for."},
        ]
    )
    ic(completion)

    problem = {
        "title": title,
        "challenge_text": challenge_text,
        "input": get_input(day=day),
        "summary": completion.choices[0].message.content,
    }

    if store:
        if not os.path.exists("summaries"):
            os.mkdir("summaries")
        p = os.path.join("summaries", f"challenge_{day}.md")
        with open(p, "w") as f:
            f.write("# " + problem["title"] + "\n\n")
            f.write("\n\n".join(problem["challenge_text"]) + "\n\n")
            f.write("## Input\n\n")
            f.write("```\n")
            f.write("\n".join(problem["input"]) + "\n\n")
            f.write("```\n\n")
            f.write(problem["summary"])

    return problem