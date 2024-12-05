
from process.resources.simulation import start_simulation
from parser import Parser
from utils import purple, blue
import logs

import argparse

# %% Configure logs
logs.store_logs = True
logs.path_logs = "results/simulation_logs_anomaly.log"
logs.update_configuration()

# %% Configure argparser
parser = argparse.ArgumentParser(description="Run log simulation")
parser.add_argument(
    "--case", type=str, help="Case to use in the simulation", required=True
)
parser.add_argument(
    "--num_sim", 
    type=int, 
    help="Number of runs done in the simulation",
    default=100,
)
parser.add_argument(
    "--version", 
    type=int, 
    help="Versaion number use in the logs",
    default=1,
)
parser.add_argument(
    "--do_anomaly", 
    action="store_true", 
    help="Run simulation as anomalies"
)  

# %% Run simulation
if __name__ == "__main__":
    args = parser.parse_args()
    
    report, msg_path = start_simulation(
        do_anomaly=args.do_anomaly,
        case=args.case,
        num_sim=args.num_sim,
        version=args.version,
    )
    print(report)

    print(purple("Parsing"))
    parser = Parser.from_file(msg_path, version=args.version)
    results = parser.load_logs(logs.path_logs)

    results["Templates"].to_csv(
        path_t := "results/template.csv", index=False
    )
    print(f"{blue('Templates saved in')} {path_t}")

    results["Structured logs"].to_csv(
        path_s := "results/structured_logs.csv", index=False
    )
    print(f"{blue('Structured logs saved in')} {path_s}")