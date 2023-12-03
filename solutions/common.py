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


def get_challenge(day: int, include_part_two: bool = False) -> dict[str, str]:
    """Get the challenge text for the day"""
    load_dotenv()
    if os.environ.get("AOC_SESSION_COOKIE") is None:
        raise ValueError("No session cookie found. Please add it to your .env file")
    r = requests.get(
        f"https://adventofcode.com/2023/day/{day}",
        cookies={"session": os.environ.get("AOC_SESSION_COOKIE")},  # type: ignore
    )
    soup = BeautifulSoup(r.text, "html.parser")
    articles = soup.find_all("article")
    part_1 = articles[0]

    title = part_1.find("h2").text.replace("-", "").strip()  # type: ignore
    text_1 = [p.text.strip() for p in part_1.find_all("p")]  # type: ignore
    example_1 = part_1.find("pre").text.splitlines()  # type: ignore
    challenge = {
        "title": title,
        "challenge_text_part_one": text_1,
        "example_1": example_1,
    }

    if include_part_two:
        if len(articles) < 2:
            raise ValueError(f"Part two of day {day} doesn't seem to be unlocked yet")
        part_2 = articles[1]
        text_2 = [p.text.strip() for p in part_2.find_all("p")]
        example_2 = part_2.find("pre").text.splitlines()

        challenge["challenge_text_part_two"] = text_2
        challenge["example_2"] = example_2

    return challenge


def request_problem_summary(
    day: int, store=True, include_part_two=False
) -> dict[str, Any]:
    """Get the problem summary for the day"""
    load_dotenv()
    if os.environ.get("OPENAI_API_KEY") is None:
        raise ValueError("No openai api key found. Please add it to your .env file")

    challenge = get_challenge(day=day, include_part_two=include_part_two)
    challenge["input"] = get_input(day=day)  # type: ignore

    messages = [
        {
            "role": "system",
            "content": "You are an coding assistant who is supporting a programmer, working on the advent of code challenges in python.",
        },
        {"role": "user", "content": "The following is the current challenge text:"},
        {"role": "system", "content": "\n".join(challenge["challenge_text_part_one"])},
        {"role": "user", "content": "The following is the first example:"},
        {"role": "system", "content": "\n".join(challenge["example_1"])},
        {
            "role": "user",
            "content": "The following is an excerpt from the challenge input:",
        },
        {"role": "system", "content": "\n".join(challenge["input"][:10])},
    ]

    if include_part_two:
        messages.extend(
            [
                {
                    "role": "user",
                    "content": "The following is the second part of the challenge:",
                },
                {
                    "role": "system",
                    "content": "\n".join(challenge["challenge_text_part_two"]),
                },
                {"role": "user", "content": "The following is the second example:"},
                {"role": "system", "content": "\n".join(challenge["example_2"])},
            ]
        )

    messages.extend(
        [
            {
                "role": "user",
                "content": "Please extract important information and summarize them. Provide the summary in markdown format with an introduction and a conclusion, and a list of bullet points in between. Also, mention things to watch out for.",
            },
        ]
    )

    openai_client = Client()
    completion = openai_client.chat.completions.create(model="gpt-4", messages=messages)
    ic(completion)

    challenge["summary"] = completion.choices[0].message.content  # type: ignore

    if store:
        if not os.path.exists("summaries"):
            os.mkdir("summaries")
        p = os.path.join("summaries", f"challenge_{day}.md")
        with open(p, "w") as f:
            f.write("# " + challenge["title"] + "\n\n")
            f.write("## Part One\n\n")
            f.write("\n\n".join(challenge["challenge_text_part_one"]) + "\n\n")
            f.write("## Example\n\n")
            f.write("```\n")
            f.write("\n".join(challenge["example_1"]) + "\n")
            f.write("```\n\n")

            if include_part_two:
                f.write("## Part Two\n\n")
                f.write("\n\n".join(challenge["challenge_text_part_two"]) + "\n\n")
                f.write("## Example\n\n")
                f.write("```\n")
                f.write("\n".join(challenge["example_2"]) + "\n")
                f.write("```\n\n")

            f.write("## Input\n\n")
            f.write("```\n")
            f.write("\n".join(challenge["input"]) + "\n\n")
            f.write("```\n\n")
            f.write(challenge["summary"])  # type: ignore

    return challenge
