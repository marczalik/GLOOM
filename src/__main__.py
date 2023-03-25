import speech_recognition as sr

from db import Database
from logging import getLogger
from thefuzz import fuzz
from typing import List, Optional, Tuple


class GLOOM:
    def __init__(self) -> None:
        self.logger = getLogger("logger")

    def run(self):
        self._cli()
        
    def _cli(self):
        resp = None
        while True:
            resp = self._greeting()
            if self._do_close(resp):
                return
            choice = self._get_input(resp)
            if self._do_close(choice):
                return
            self._find_blocked_scenarios(choice)

    def _do_close(self, resp: str) -> bool:
        close = False
        if resp is None:
            close = False
        elif resp.lower() == 'q' or resp.lower() == "quit":
            close = True
        else:
            close = False
        return close 

    def _get_best_match(self, name: str) -> Tuple[int, str, int]:
        best_match: Tuple[int, str, int] = (-1, None, -1)
        for scenario_idx, scenario_name in Database.Database.scenarios.items():
            if name.lower() == scenario_name:
                best_match = (scenario_idx, scenario_name, 100)
                break
            else:
                match_ratio = fuzz.ratio(name.lower(), scenario_name)
                if match_ratio > best_match[2]:
                    best_match = (scenario_idx, scenario_name, match_ratio)

        return best_match
    
    def _get_input(self, type: int):
        if type == "1":        
            resp = input("Pick a scenario: ")       
        elif type == "2":
            pass
        return resp
    
    def _greeting(self) -> str:
        print("Enter 'q' or 'Quit' to quit")
        return self._get_type_of_iput()
        
    def _get_type_of_iput(self) -> str:
        resp = None
        while resp != "1" and resp != "2" and not self._do_close(resp):
            print("Select from the following options:")
            print("\t1. Text input")
            print("\t2. Voice input")
            resp = input("[1/2]: ")
        return resp

    def _find_blocked_scenarios(self, scenario: str):
        scenario_idx = self._name_to_idx(scenario)
        if scenario_idx == -1:
            return
        blocked_scenarios = Database.Database.blockers.get(scenario_idx, None)
        if blocked_scenarios is None:
            print(f"No blocked scenarios found for {scenario}...\n")
        else:
            self._print_blocked_scenarios(blocked_scenarios)

    def _name_to_idx(self, name: str) -> int:
        scenario_idx, scenario_name, match_ratio = self._get_best_match(name)
        if match_ratio == 100:
            return scenario_idx
        elif 80 < match_ratio < 100:
            if self._verify_close_match(scenario_name):
                return scenario_idx
            else:
                return -1
        else:
            self.logger.warning(f"Scenario {name} not found!\n")
            return -1

    def _idx_to_name(self, idx: int) -> str:
        return Database.Database.scenarios[idx]

    def _print_blocked_scenarios(self, blocks: List[Tuple[int, Optional[str]]]):
        for scenario, reason in blocks:
            name = self._idx_to_name(scenario)
            output = f"\tBlocks scenario {scenario}: {name.title()}"
            output += f" {reason}" if reason else ""
            print(output)
        print()

    def _verify_close_match(self, name: str):
        resp = input(f"Did you mean {name}? [y/n]: ")
        while resp:
            if resp.lower() == "y" or resp.lower() == "yes":
                return True
            elif resp.lower() == "n" or resp.lower() == "no":
                return False
            else:
                resp = input("Please enter [y/n]: ")


if __name__ == "__main__":
    gloom = GLOOM()
    gloom.run()
