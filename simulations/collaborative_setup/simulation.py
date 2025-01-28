from simulations.collaborative_setup import methods
from simulations._isimulation import ISimulation

from backbone.msg_reader import Messages
import backbone.logs as logs

import typing as t


class CollaborativeSetup(ISimulation):
    """
    Loading Dependencies challenge
    """
    def __init__(self) -> None:
        super().__init__(
            cases={
                "challenge_9": methods.collaborative_challenge_9,
                "challenge_10": methods.collaborative_challenge_10,
            }, 
            msg_path="simulations/collaborative_setup/messages.yaml",
            multiple_clients=3,
        )

    def main(
        self, 
        case: t.Callable[[t.Any], None], 
        msg: Messages, 
        do_anomaly: bool, 
        client_n: int | None = None
    ) -> None:
        logs.trace(msg.start_simulation)
        case(msg=msg, do_anomaly=do_anomaly, client_n=client_n)
        logs.trace(msg.end_simulation)