# Log Gym 

Framework to develop test challenges for log anomaly detectors models. Official code base from: **Sok: A Review on Log Anomaly Collaborative Intrusion Detection Systems (2025)**.


## Sections 
1. [Requirements](#requirements)
2. [Run Unittests](#run-unittests)
3. [Generate Challenges](#generate-challenges)
4. [Docker support](#docker-support)
5. [Challenges](#challenges)
6. [Citation](#citation)

## Requirements

The code was run with **Python version 3.12.3**. To install the requirements do:

```bash
pip install -r requirements.txt 
```
To run unittests do:

```bash
python -m unittest discover -s test/ 
```

## Generate challenges
First create a folder inside the project call **results**. In linux can be done as:

```bash
mkdir results
```

To generate the challenges run:

```bash
python main.py --config_file <CONFIG_FILE>
```

Example:

```bash
python main.py --config_file config_files/xray.yaml
```

The challenges databases will be save in **results/**. To plot the distributions use **notebooks/data_analysis.ipynb**.

## Docker support
To run the code inside a docker container use the file **Dockerfile** and change the challenge you want to generate in the variable **CONFIG_FILE** inside **start.sh**.

Build the image with the next command:
```bash
docker build -t log-gym .
```
And run the container with:
```bash
docker run --name log-gym log-gym
```
## Challenges

The configuration files of the implemented challenges can be found in **config_files/**. More information in the publication.

### Access resources

The simulation try to access a specific resource.

*   **Challenge 1**: In case of anomaly, the process is "stuck".
*   **Challenge 2**: In case of anomaly, the process try 10 times.
*   **Challenge 3**: In case of anomaly no event id distintion with nominaly.

### Loading dependencies

Anomalies are presented when certain dependencies change the time that it takes to load.

*   **Challenge 4**: Dependency d takes more time than the rest when abnormal.
*   **Challenge 5**: Dependency d and c exchanges times in abnormal behaviour.
*   **Challenge 6**: Same as challenge 4, but the time difference is much smaller.

### Medical machine

Detect anomalies in an automaton system.

* **Challenge 7**:  The machine runs verification or measurement operations.
* **Challenge 8**: The machine must run verification before doing a measurement.

### Collaborative setup

Challenges for Collaborative Intrusion Detection Systems.

* **Challenge 9**: One of the clients creates a wrong template in the parsing.
* **Challenge 10**: Infected clients access as admins and remove users are part of the training process.

## Citation
()