import os
import re
import pandas as pd


def get_running_containers_dataframe():
    status_output = os.popen("docker-compose ps").read()
    lines = status_output.strip().splitlines()
    headers = lines[0].split()

    # Define a regex pattern for splitting the data into columns
    pattern = re.compile(r"(\S+)\s+(\S+)\s+(\"[^\"]+\")\s+(\S+)\s+([\d\s\w]+ ago)\s+([\w\s]+)\s+([\S\s]+)$")

    data = []
    for line in lines[1:]:
        match = pattern.match(line)
        if match:
            data.append(list(match.groups()))

    return pd.DataFrame(data, columns=headers)