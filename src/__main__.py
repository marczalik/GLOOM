from db import Database
from logging import getLogger
from typing import List, Optional, Tuple

class GLOOM:
    def __init__(self) -> None:
        self.logger = getLogger("logger")

    def run(self):
        cmd = None
        while cmd != "q":
            cmd = input("Pick a scenario: ")
            self._find_blockd_scenarios(cmd)

    def _find_blockd_scenarios(self, scenario: str):
        scenario_idx = self._name_to_idx(scenario)
        if scenario_idx == -1:
            return
        blocked_scenarios = Database.Database.blockers.get(scenario_idx, None)
        if blocked_scenarios is None:
            print(f"No blocked scenarios found for {scenario}...\n")
        else:
            self._print_blocked_scenarios(blocked_scenarios)
    
    def _name_to_idx(self, name: str) -> int:
        for scenario_idx, scenario_name in Database.Database.scenarios.items():
            if name.lower() == scenario_name:
                return scenario_idx
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
        

if __name__ == "__main__":
    gloom = GLOOM()
    gloom.run()