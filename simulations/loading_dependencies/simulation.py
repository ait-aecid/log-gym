
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
                "challenge_4": methods.dependencies_challenge_4,
                "challenge_5": methods.dependencies_challenge_5,
                "challenge_6": methods.dependencies_challenge_6,
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
