
from simulations._isimulation import ISimulation
from simulations.xray_machine import methods

from backbone.msg_reader import Messages
import backbone.logs as logs

import typing as t


class XrayMachine(ISimulation):
    """
    Loading XrayMachine challenge
    """
    def __init__(self) -> None:
        super().__init__(
            cases={
                "challenge_7": methods.medical_challenge_7,
                "challenge_8": methods.medical_challenge_8,
            }, 
            msg_path="simulations/xray_machine/messages.yaml"
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