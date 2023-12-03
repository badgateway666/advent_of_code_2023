import re

from icecream import ic

from common import get_input, submit_answer


def parse_single_draw(draw):
    greens = re.findall(r"(\d+) green", draw)
    reds = re.findall(r"(\d+) red", draw)
    blues = re.findall(r"(\d+) blue", draw)

    result = {
        "red": sum([int(red) for red in reds]) or 0,
        "green": sum([int(green) for green in greens]) or 0,
        "blue": sum([int(blue) for blue in blues]) or 0,
    }

    return result


def parse_single_game(line):
    line = line.split(":")[1]  # Remove the Game ID

    draws = line.split(";")
    parsed_draws = [parse_single_draw(draw) for draw in draws]

    result = {
        "max_red": max([draw["red"] for draw in parsed_draws]),
        "max_green": max([draw["green"] for draw in parsed_draws]),
        "max_blue": max([draw["blue"] for draw in parsed_draws]),
    }

    return result


def determine_possible_games(parsed_lines):
    max_red = 12
    max_green = 13
    max_blue = 14

    possible_game_ids = []
    for idx, line in enumerate(parsed_lines):
        if (
            line["max_red"] <= max_red
            and line["max_green"] <= max_green
            and line["max_blue"] <= max_blue
        ):
            possible_game_ids.append(idx + 1)

    return sum(possible_game_ids)


def determine_power(parsed_lines):
    result_sum = 0
    for line in parsed_lines:
        result = (
            max(int(line["max_red"]), 1)
            * max(int(line["max_green"]), 1)
            * max(int(line["max_blue"]), 1)
        )
        result_sum += result
    return result_sum


def run_part_two() -> None:
    lines = ic(get_input(day=2))
    parsed_lines = [parse_single_game(line) for line in lines]  # type: ignore
    sum_of_powers = ic(determine_power(parsed_lines))
    submit_answer(day=2, part=2, answer=sum_of_powers)


def run_part_one() -> None:
    lines = ic(get_input(day=2))
    parsed_lines = [parse_single_game(line) for line in lines]  # type: ignore
    sum_possible_games = ic(determine_possible_games(parsed_lines))
    submit_answer(day=2, part=1, answer=sum_possible_games)


if __name__ == "__main__":
    run_part_two()
