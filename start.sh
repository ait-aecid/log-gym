GREEN="\033[92m"
STOP="\033[0m"

# Config file use to generate challenges
CONFIG_FILE="config_files/collaborative.yaml"

echo "${GREEN}Running tests...${STOP}"
python -m unittest discover -s test/

if [ ! -d "results" ]; then
    echo "${GREEN}Creating result file...${STOP}"
    mkdir results/
fi

echo "${GREEN}Generating challenges...${STOP}"
python main.py --config_file $CONFIG_FILE


echo "${GREEN}Generated challenge${STOP}"
ls -lh results/

echo "${GREEN}Done${STOP}"