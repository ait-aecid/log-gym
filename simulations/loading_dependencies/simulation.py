
from simulations._isimulation import ISimulation
from simulations.loading_dependencies import methods

from backbone.msg_reader import Messages
import backbone.logs as logs

import typing as t


class LoadingDependencies(ISimulation):
    """
    Loading Dependencies challenge
    """
    def __init__(self) -> None:
        super().__init__(
            cases={
                "case_1": methods.case_1_easier_case,
                "case_2": methods.case_2_exchange_times,
                "case_3": methods.case_3_small_difference,
            }, 
            msg_path="simulations/loading_dependencies/messages.yaml"
        )

    def main(
        self, 
        case: t.Callable[[t.Any], None], 
        msg: Messages, 
        do_anomaly: bool, 
        client_n: int | None = None
    ) -> None:
        logs.trace(msg.start_simulation)
        case(msg=msg, do_anomaly=do_anomaly)
        logs.trace(msg.end_simulation)
