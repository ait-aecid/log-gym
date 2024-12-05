
from process.resources.simulation import start_simulation
from backbone.parser import Parser
from utils import Color 
import backbone.logs as logs

import argparse
import yaml


# %% Configure argparser
parser = argparse.ArgumentParser(description="Run log simulation")
parser.add_argument(
    "--config_file", type=str, help="Simulation config file", required=True
)

# %% Run simulation
if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.config_file) as file:
        config = yaml.safe_load(file)

    logs.store_logs = config["Logs"]["store_logs"]
    logs.path_logs = config["Logs"]["path_logs"]
    logs.update_configuration()
    
    report, msg_path = start_simulation(
        do_anomaly=config["Specific"]["As_anomaly"],
        case=config["General"]["Case"],
        num_sim=config["General"]["Number_simulations"],
        version=config["Specific"]["Version"],
    )
    print(report)

    print(Color.purple("Parsing"))
    parser = Parser.from_file(msg_path, version=config["Specific"]["Version"])
    results = parser.load_logs(logs.path_logs)

    results["Templates"].to_csv(
        path_t := config["Results"]["templates_path"], index=False
    )
    print(f"{Color.blue('Templates saved in')} {path_t}")

    results["Structured logs"].to_csv(
        path_s := config["Results"]["structured_logs_path"], index=False
    )
    print(f"{Color.blue('Structured logs saved in')} {path_s}")