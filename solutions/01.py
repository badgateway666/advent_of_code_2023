import re

from icecream import ic

from common import get_input, submit_answer


def calc_calibration_sum(lines: list[str]) -> int:
    pattern = re.compile(r"\D")
    stripped_input = [re.sub(pattern, "", line) for line in lines]
    calibration_numbers = [int(line[0] + line[-1]) for line in stripped_input]
    return sum(calibration_numbers)


def preprocess_lines(lines: list[str]) -> list[str]:
    replacements = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    preprocessed_lines = []
    for line in lines:
        for key, value in replacements.items():
            line = line.replace(key, f"{key[0]}{value}{key[-1]}")
        preprocessed_lines.append(line)
    return preprocessed_lines


def run_part_one() -> None:
    lines = get_input(day=1)
    result = ic(calc_calibration_sum(lines))
    submit_answer(day=1, part=1, answer=result)


def run_part_two() -> None:
    lines = get_input(day=1)
    preprocessed_lines = preprocess_lines(lines)
    result = ic(calc_calibration_sum(preprocessed_lines))
    submit_answer(day=1, part=2, answer=result)


if __name__ == "__main__":
    result = run_part_two()
