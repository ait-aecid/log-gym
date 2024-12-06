
from simulations.loading_dependencies import methods

from backbone.msg_reader import Messages
import backbone.logs as logs

from utils import Color

from tqdm import tqdm
import time

from typing import Tuple


cases = {
    "case_1": methods.case_1_easier_case,
    "case_2": methods.case_2_exchange_times,
    "case_3": methods.case_3_small_difference,
}


def main(case: str, msg: Messages, do_anomaly: bool) -> None:
    logs.trace(msg.start_simulation)
    case_method = cases[case]
    case_method(msg=msg, do_anomaly=do_anomaly)
    logs.trace(msg.end_simulation)


def start_simulation(
    do_anomaly: bool, case: str, num_sim: int, version: int
) -> Tuple[str, str]:
    
    msg_path = "simulations/loading_dependencies/messages.yaml"
    print(msg_path)
    msg = Messages.from_file(msg_path, version=version)

    print(Color.purple("Start simulation"))
    start = time.time()
    for _ in tqdm(range(num_sim)):
        main(case=case, msg=msg, do_anomaly=do_anomaly)
    end = time.time() - start

    report = f"{Color.purple('Process simulation report')}\n"
    report += f"    - {Color.blue('Case')}: {cases[case].__name__}\n"
    report += f"    - {Color.blue('Description')}: {cases[case].__doc__.replace('\n', '')}\n"
    report += f"    - {Color.blue('Logs version')} {version}\n"
    report += f"    - {Color.blue('Number of simulations')} {num_sim}\n"
    report += f"    - {Color.blue('Do anomalies')}: {'Yes' if do_anomaly else 'No'}\n"
    report += f"    - {Color.blue('Logs stored in file')}: {'Yes' if logs.store_logs else 'No'}\n"
    report += f"    - {Color.blue('Logs file')}: {logs.path_logs}\n"
    report += f"    - {Color.blue('Total time simulation')}: {end}\n"

    return report, msg_path