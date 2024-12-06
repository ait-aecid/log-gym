
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
                "case_1": methods.case1_init_resource,
                "case_2": methods.case2_init_resource,
                "case_3": methods.case3_init_resource,
            }, 
            msg_path="simulations/access_resource/messages.yaml"
        )

    def main(
        self, case: t.Callable[[t.Any], None], msg: Messages, do_anomaly: bool,
    ) -> None:
        
        config = methods.ConfigResource()
        config.do_anomaly = do_anomaly

        logs.trace(msg.start_process)
        case(config=config, msg=msg)
        logs.warning(msg.ajusting)
        logs.trace(msg.end_process)

