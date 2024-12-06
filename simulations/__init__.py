
from simulations.loading_dependencies.simulation import start_simulation as dep_simulation
from simulations.access_resource.simulation import start_simulation as res_simulation


challenges = {
    "Resource_challenge": res_simulation, 
    "Loading_dependencies": dep_simulation,
}