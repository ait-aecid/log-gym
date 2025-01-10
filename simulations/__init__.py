
from simulations.loading_dependencies.simulation import LoadingDependencies 
from simulations.access_resource.simulation import AccessResources 
from simulations.xray_machine.simulation import XrayMachine


challenges = {
    "Resource_challenge": AccessResources, 
    "Loading_dependencies": LoadingDependencies,
    "XRay_machine": XrayMachine,
}