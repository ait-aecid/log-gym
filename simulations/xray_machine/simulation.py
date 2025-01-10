
from simulations._isimulation import ISimulation
from simulations.xray_machine import methods

from backbone.msg_reader import Messages
import backbone.logs as logs

import typing as t


class XrayMachine(ISimulation):
    """
    Loading Dependencies challenge
    """
    def __init__(self) -> None:
        super().__init__(
            cases={
                "case_1": methods.case_1_xray_simple,
                "case_2": methods.case_2_xray_combine_ver_meas,
            }, 
            msg_path="simulations/xray_machine/messages.yaml"
        )

    def main(
        self, case: t.Callable[[t.Any], None], msg: Messages, do_anomaly: bool,
    ) -> None:
        logs.trace(msg.start_simulation)
        case(msg=msg, do_anomaly=do_anomaly)
        logs.trace(msg.end_simulation)