from backbone.msg_reader import Messages
import backbone.logs as logs

from utils import Color

from abc import ABC, abstractmethod

from tqdm import tqdm
import typing as t
import time


class ISimulation(ABC):
    def __init__(
        self, 
        cases: t.Dict[str, t.Callable[[t.Any], None]],
        msg_path: str = ""
    ) -> None:
        self.cases = cases
        self.msg_path = msg_path

    @abstractmethod
    def main(
        self, case: t.Callable[[t.Any], None], msg: Messages, do_anomaly: bool
    ) -> None:
        pass

    def start_simulation(
        self, do_anomaly: bool, case: str, num_sim: int, version: int
    ) -> t.Tuple[str, str]:
        
        msg = Messages.from_file(self.msg_path, version=version)

        print(Color.purple("Start simulation"))
        start = time.time()
        for _ in tqdm(range(num_sim)):
            self.main(case=self.cases[case], msg=msg, do_anomaly=do_anomaly)
        end = time.time() - start

        report = f"{Color.purple('Process simulation report')}\n"
        report += f"    - {Color.blue('Case')}: {self.cases[case].__name__}\n"
        report += f"    - {Color.blue('Description')}: {self.cases[case].__doc__.replace('\n', '')}\n"
        report += f"    - {Color.blue('Logs version')} {version}\n"
        report += f"    - {Color.blue('Number of simulations')} {num_sim}\n"
        report += f"    - {Color.blue('Do anomalies')}: {'Yes' if do_anomaly else 'No'}\n"
        report += f"    - {Color.blue('Logs stored in file')}: {'Yes' if logs.store_logs else 'No'}\n"
        report += f"    - {Color.blue('Logs file')}: {logs.path_logs}\n"
        report += f"    - {Color.blue('Total time simulation')}: {end}\n"

        return report, self.msg_path