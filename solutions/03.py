import string
from typing import Optional
from icecream import ic

from common import get_input, submit_answer, request_challenge_summary


class Number:

    def __init__(self, num: int, y: int, start_x: int, end_x: int) -> None:
        self.num = num
        self.y, self.start_x, self.end_x = y, start_x, end_x

    def __repr__(self) -> str:
        return f"{self.num} at {self.y, self.start_x, self.end_x}"
    
    def includes_koords(self, koords: tuple[int, int]) -> bool:
        y, x = koords
        return self.y == y and self.start_x <= x <= self.end_x
    
    def __hash__(self) -> int:
        return hash((self.y, self.start_x, self.end_x))
    
    def __mul__(self, other: "Number") -> int:
        return self.num * other.num
    

class Schematic:

    def __init__(self, lines) -> None:
        self.dim_x = len(lines[0])
        self.dim_y = len(lines)

        self._lines = lines
        ic(lines)
        self.numbers: list[Number] = []
        self.gears = []

        self._parse_input()
        print("Parsed")

    def __getitem__(self, key: tuple[int, int]) -> str:
        y, x = key
        return self._lines[y][x]

    def __repr__(self) -> str:
        return "\n".join(self._lines)

    def _parse_input(self):
        for y, line in enumerate(self._lines):
            cur_start_x = None
            for idx, char in enumerate(line):
                if char == "*":
                    self.gears.append((y, idx))
                if char in string.digits and cur_start_x is None:
                    cur_start_x = idx
                elif char not in string.digits and cur_start_x is not None:
                    num_coords = (y, cur_start_x, idx-1)
                    num = int(line[cur_start_x:idx])
                    number = Number(num, *num_coords)
                    cur_start_x = None
                    self.numbers.append(number)
                elif idx == len(line) - 1 and cur_start_x is not None:
                    num_coords = (y, cur_start_x, idx)
                    num = int(line[cur_start_x:idx+1])
                    number = Number(num, *num_coords)
                    cur_start_x = None
                    self.numbers.append(number)

    def calc_part_number_sum(self) -> int:
        part_numbers = set()
        for number in self.numbers:
            for y in range(max(number.y-1, 0), min(number.y+2, self.dim_y)):
                for x in range(max(number.start_x-1, 0),  min(number.end_x+2, self.dim_x)):
                    if self[y, x] not in string.digits and self[y, x] != ".":
                        part_numbers.add(number)
            
        return sum([num.num for num in part_numbers])

    def calc_gear_rations(self) -> int:
        result = 0
        for gear in self.gears:
            result += self._calc_gear_ratio(gear)
        return result
    
    def _calc_gear_ratio(self, gear: tuple[int, int]) -> int:
        gear_y, gear_x = gear
        candidate_numbers = set()
        for y in range(max(gear_y-1, 0), min(gear_y+2, self.dim_y)):
            for x in range(max(gear_x-1, 0),  min(gear_x+2, self.dim_x)):
                if (y, x) == gear:
                    continue

                for number in self.numbers:
                    if number.includes_koords((y, x)):
                        candidate_numbers.add(number)

        if len(candidate_numbers) == 2:
            return candidate_numbers.pop() * candidate_numbers.pop()
        
        return 0
    

def run_part_one() -> None:
    lines = get_input(day=3)
    schematic = Schematic(lines)
    result = schematic.calc_part_number_sum()
    ic(result)
    submit_answer(day=3, part=1, answer=result)


def run_part_two() -> None:
    lines = get_input(day=3)
    schematic = Schematic(lines)
    result = schematic.calc_gear_rations()
    submit_answer(day=3, part=2, answer=result)


if __name__ == "__main__":
    run_part_one()