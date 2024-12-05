
from process.resources import methods
from backbone.msg_reader import Messages
from utils import blue, purple

from tqdm import tqdm
import time
import backbone.logs as logs

from typing import Tuple



cases = {
    "case_1": methods.case1_init_resource,
    "case_2": methods.case2_init_resource,
    "case_3": methods.case3_init_resource,
}


def main(case: str, msg: Messages, config: methods.ConfigResource) -> None:
    logs.trace(msg.start_process)
    case_method = cases[case]
    case_method(config=config, msg=msg)
    logs.warning(msg.ajusting)
    logs.trace(msg.end_process)


def start_simulation(
    do_anomaly: bool, case: str, num_sim: int, version: int
) -> Tuple[str, str]:
    
    config = methods.ConfigResource()
    config.do_anomaly = do_anomaly
    msg_path = "process/resources/messages.yaml"
    msg = Messages.from_file(msg_path, version=version)

    print(purple("Start simulation"))
    start = time.time()
    for _ in tqdm(range(num_sim)):
        main(case=case, msg=msg, config=config)
    end = time.time() - start

    report = f"{purple('Process simulation report')}\n"
    report += f"    - {blue('Case')}: {cases[case].__name__}\n"
    report += f"    - {blue('Description')}: {cases[case].__doc__.replace('\n', '')}\n"
    report += f"    - {blue('Logs version')} {version}\n"
    report += f"    - {blue('Number of simulations')} {num_sim}\n"
    report += f"    - {blue('Do anomalies')}: {'Yes' if do_anomaly else 'No'}\n"
    report += f"    - {blue('Logs stored in file')}: {'Yes' if logs.store_logs else 'No'}\n"
    report += f"    - {blue('Logs file')}: {logs.path_logs}\n"
    report += f"    - {blue('Total time simulation')}: {end}\n"

    return report, msg_path