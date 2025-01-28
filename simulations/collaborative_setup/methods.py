
from backbone.msg_reader import Messages
import backbone.logs as logs

from typing import Generator
import time


class Sender:
    def __init__(
        self, do_anomaly: bool, msg: Messages, client_n: int, is_test: bool = False
    ) -> None:
        self.do_anomaly = do_anomaly
        self.msg = msg
        self.template = 1 if client_n == 0 else 2
        self.is_test = is_test

    def wait_to_send(self) -> Generator[bool, None, None]:
        wait_amount = 10 if self.do_anomaly else 4
        for _ in range(wait_amount):
            logs.info(self.msg.waiting)
            if not self.is_test:
                time.sleep(0.05)
            yield True
        yield False

    def send_package(self) -> None:
        if self.do_anomaly:
            logs.info(self.msg[f"template_{self.template}_error"])
        else:
            logs.info(self.msg[f"template_{self.template}_send_file"])
        

def collaborative_challenge_9(do_anomaly: bool, msg: Messages, client_n: int) -> None:
    """
    One of the clients creates a wrong template in the parsing
    """
    sender = Sender(do_anomaly=do_anomaly, msg=msg, client_n=client_n)

    logs.info(msg.prepared_to_send)
    for _ in range(4):
        wait_process = sender.wait_to_send()
        while next(wait_process): pass
        sender.send_package()
    

def is_admin(do_anomaly: bool, client_n: int) -> bool:
    return do_anomaly or client_n == 0


def collaborative_challenge_10(do_anomaly: bool, msg: Messages, client_n: int) -> None:
    """
    Infected clients access as admins and remove users.
    """
    logs.info(msg.starting_process)
    if is_admin(do_anomaly=do_anomaly, client_n=client_n):
        logs.info(msg.admin_remove_jeff)
        logs.info(msg.admin_remove_thomas)
        logs.info(msg.admin_remove_john)
    else:
        for _ in range(3):
            for _ in range(4):
                logs.info(msg.waiting)
                time.sleep(0.05)
            logs.info(msg.doing_process)