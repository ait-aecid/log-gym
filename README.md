# Log Gym 

Framework for creating test challenges aimed at models that detect log anomalies. Official code base from: **Collaborative anomaly detection in log data: Comparative analysis and evaluation framework**.


## Sections 
1. [Requirements](#requirements)
2. [Generate Challenges](#generate-challenges)
3. [Docker support](#docker-support)
4. [Challenges](#challenges)
5. [Citation](#citation)

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

The challenges databases will be save in **results/**. To plot the distributions use **notebooks/data_analysis.ipynb**. Access the notebook with:
```bash
jupyter notebok
```

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

### Xray machine

Detect anomalies in an automaton system.

* **Challenge 7**:  The machine runs verification or measurement operations.
* **Challenge 8**: The machine must run verification before doing a measurement.

### Collaborative setup

Challenges for Collaborative Intrusion Detection Systems.

* **Challenge 9**: One of the clients creates a wrong template in the parsing.
* **Challenge 10**: Infected clients access as admins and remove users are part of the training process.

## Citation
```
@article{GARCIAGOMEZ2026108090,
  title = {Collaborative anomaly detection in log data: Comparative analysis and evaluation framework},
  journal = {Future Generation Computer Systems},
  volume = {175},
  pages = {108090},
  year = {2026},
  issn = {0167-739X},
  doi = {https://doi.org/10.1016/j.future.2025.108090},
  url = {https://www.sciencedirect.com/science/article/pii/S0167739X2500384X},
  author = {André {García Gómez} and Max Landauer and Markus Wurzenberger and Florian Skopik and Edgar Weippl},
  keywords = {Machine learning, CIDS, IDS, Anomaly detection, AI, Log analysis},
  abstract = {Log Anomaly Collaborative Intrusion Detection Systems (CIDS) are designed to detect suspicious activities and security breaches by analyzing log files using anomaly detection techniques while leveraging collaboration between multiple entities (e.g., different systems, organizations, or network nodes). Unlike traditional Intrusion Detection Systems (IDS) that require centralized algorithm updates and data aggregation, CIDS enable decentralized updates without extensive data exchange, improving efficacy, scalability, and compliance with regulatory constraints. Additionally, inter-detector communication helps to reduce the number of false positives. These systems are particularly useful in distributed environments, where individual system have limited visibility into potential threats. This paper reviews the current landscape of Log Anomaly CIDS and introduces an open-source framework designed to create benchmark datasets for evaluating system performance. We categorize log anomaly detectors into three categories: Sequential-wise, Embedding-wise, and Graph-wise. Furthermore, our open framework facilitates rigorous evaluation against different challenges identifying weaknesses in existing methods like Deeplog and enhancing model robustness.}
}

```

