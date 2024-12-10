from backbone.dataset_generator import process_all_tables
from backbone.parser import Parser
import backbone.logs as logs

from simulations import challenges
from utils import Color, Config , save_csv

import argparse
import os


def create_folder(path):
    folder = "/".join(path.split("/")[:-1])
    if not os.path.isdir(folder):
        os.mkdir(folder)

# %% Configure argparser
parser = argparse.ArgumentParser(description="Run log simulation")
parser.add_argument(
    "--config_file", type=str, help="Simulation config file", required=True
)

# %% Run simulation
if __name__ == "__main__":
    args = parser.parse_args()
    config = Config(args.config_file)
    simulation_type, case, db_path = config.get_parameters()

    print(Color.yellow(f"Doing {simulation_type}")) 
    structured_logs_paths, templates_paths = [], []
    for simulation in config.simulations():
        
        sim_config = config[simulation]
        print(Color.yellow(f"Initializing... {simulation}")) 
        create_folder(sim_config["Results"]["path_logs"])
        logs.store_logs = sim_config["store_logs"]
        logs.path_logs = sim_config["Results"]["path_logs"]
        logs.update_configuration()

        challenge = challenges[simulation_type]()
        report, msg_path = challenge.start_simulation(
            do_anomaly=sim_config["As_anomaly"],
            case=case,
            num_sim=sim_config["Number_simulations"],
            version=sim_config["Version"],
        )
        print(report)

        print(Color.purple("Parsing"))
        parser = Parser.from_file(msg_path, version=sim_config["Version"])
        results = parser.load_logs(logs.path_logs)

        save_csv(
            path_t := sim_config["Results"]["templates_path"], results["Templates"]
        )
        templates_paths.append(path_t)
        print(f"{Color.blue('Templates saved in')} {path_t}")

        save_csv( 
            path_s := sim_config["Results"]["structured_logs_path"], results["Structured logs"]
        )
        structured_logs_paths.append(path_s)
        print(f"{Color.blue('Structured logs saved in')} {path_s}")

    print(Color.purple("Generating db"))
    create_folder(db_path)
    process_all_tables(
        structured_logs_paths=structured_logs_paths,
        template_paths=templates_paths,
        save_path=db_path
    )