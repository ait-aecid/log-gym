from backbone.msg_reader import Messages
import backbone.logs as logs

from utils import Color

from abc import ABC, abstractmethod

from tqdm import tqdm
import typing as t
import time




def do_report(
    func: t.Callable[[t.Any], None], 
    version: int, 
    num_sim: int, 
    do_anomaly: bool, 
    time_: float
) -> str:
    
    report = f"{Color.purple('Process simulation report')}\n"
    report += f"    - {Color.blue('Case')}: {func.__name__}\n"
    report += f"    - {Color.blue('Description')}: {func.__doc__.replace('\n', '')}\n"
    report += f"    - {Color.blue('Logs version')} {version}\n"
    report += f"    - {Color.blue('Number of simulations')} {num_sim}\n"
    report += f"    - {Color.blue('Do anomalies')}: {'Yes' if do_anomaly else 'No'}\n"
    report += f"    - {Color.blue('Logs stored in file')}: {'Yes' if logs.store_logs else 'No'}\n"
    report += f"    - {Color.blue('Logs file')}: {logs.path_logs}\n"
    report += f"    - {Color.blue('Total time simulation')}: {time_}\n"

    return report


class ISimulation(ABC):
    def __init__(
        self, 
        cases: t.Dict[str, t.Callable[[t.Any], None]],
        msg_path: str = "",
        multiple_clients: int | None = None,
    ) -> None:
        self.cases = cases
        self.msg_path = msg_path
        self.multiple_clients = multiple_clients

    @abstractmethod
    def main(
        self, 
        case: t.Callable[[t.Any], None], 
        msg: Messages, 
        do_anomaly: bool,
        client_n: int | None = None
    ) -> None:
        pass

    def start_simulation(
        self, do_anomaly: bool, case: str, num_sim: int, version: int
    ) -> t.Tuple[str, str]:
        
        print(Color.purple("Start simulation"))
        start = time.time()
        if self.multiple_clients is None: 
            msg = Messages.from_file(self.msg_path, version=version)
            for _ in tqdm(range(num_sim)):
                self.main(
                    case=self.cases[case], msg=msg, do_anomaly=do_anomaly, client_n=None
                )
        else:
            for client_n in range(self.multiple_clients):
                print(Color.purple(f"- Client {client_n}"))
                msg = Messages.from_file(
                    self.msg_path, version=version, client_n=client_n
                )        
                for _ in tqdm(range(num_sim)):
                    self.main(
                        case=self.cases[case], 
                        msg=msg, 
                        do_anomaly=do_anomaly, 
                        client_n=client_n
                    )
        end = time.time() - start

        report = do_report(
            func=self.cases[case], 
            version=version, 
            num_sim=num_sim, 
            do_anomaly=do_anomaly, 
            time_=end
        )
        return report, self.msg_path