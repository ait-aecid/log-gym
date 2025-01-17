
from backbone.msg_reader import Messages
import backbone.logs as logs


def case_1_wrong_template(
    do_anomaly: bool, msg: Messages, client_n: int, is_test: bool = False, 
) -> None:
    """
    One of the clients creates a wrong template in the parsing
    """
    logs.info(msg.test_simulation)