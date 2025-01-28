
from simulations._isimulation import ISimulation
from simulations.access_resource import methods

from backbone.msg_reader import Messages
import backbone.logs as logs

import typing as t


class AccessResources(ISimulation):
    """
    Access Resource challenge
    """
    def __init__(self) -> None:
        super().__init__(
            cases={
                "challenge_1": methods.resources_challenge_1,
                "challenge_2": methods.resources_challenge_2,
                "challenge_3": methods.resources_challenge_3,
            }, 
            msg_path="simulations/access_resource/messages.yaml"
        )

    def main(
        self, 
        case: t.Callable[[t.Any], None], 
        msg: Messages, 
        do_anomaly: bool, 
        client_n: int | None = None
    ) -> None:
        
        config = methods.ConfigResource()
        config.do_anomaly = do_anomaly

        logs.trace(msg.start_process)
        case(config=config, msg=msg)
        logs.warning(msg.ajusting)
        logs.trace(msg.end_process)

