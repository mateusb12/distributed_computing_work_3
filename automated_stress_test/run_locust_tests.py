import os
import time
import requests

from nabor.automated_stress_test.docker_utils import get_running_containers_dataframe
from nabor.automated_stress_test.global_variables import DOCKER_COMPOSE_LOCATION

# Settings
NUM_OF_USERS = [10, 100, 1000]
INSTANCES = [3, 2, 1]
MINUTES_PER_TEST = 3


def start_all_containers():
    os.chdir(DOCKER_COMPOSE_LOCATION)
    container_df = get_running_containers_dataframe()
    running_containers = container_df[container_df['STATUS'].str.startswith('Up')]
    if running_containers.empty:
        print("No containers are running. Starting them now.")
        os.system("docker-compose up -d")
        return
    print("Containers are already running. No need to start them.")


def test_nginx_connectivity():
    url = "http://localhost/?p=8"
    try:
        response = requests.get(url, timeout=5)  # Wait for up to 5 seconds
        if response.status_code == 200:
            print(f"Successfully connected to {url}")
        else:
            print(f"Received {response.status_code} when trying to connect to {url}")
    except requests.ConnectionError:
        print(f"Failed to connect to {url}")
    except requests.Timeout:
        print(f"Connection to {url} timed out")


def run_single_locust_test(user_amount: int, instance_amount: int):
    os.chdir(DOCKER_COMPOSE_LOCATION)
    os.system("docker-compose up -d")
    time.sleep(15)
    csv_dir = os.path.join(DOCKER_COMPOSE_LOCATION, 'csvs')
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    filename = f"csvs\\result_{user_amount}_users_{instance_amount}_instances"
    desired_host = "http://localhost:80"
    print(f"Running test with {user_amount} users and {instance_amount} instances")
    os.system(f"locust -f locustfile.py -u {user_amount} -r 10 --host={desired_host}"
              f" --headless --run-time {MINUTES_PER_TEST}m --csv={filename}")

    # A delay to ensure everything is cleaned up before the next run
    time.sleep(1)
    os.system("docker-compose down")
    time.sleep(15)


def run_all_locust_tests():
    # load_tests = [10, 100, 1000]
    load_tests = [1000]

    for load in load_tests:
        run_single_locust_test(load, 2)


def __main():
    run_all_locust_tests()


if __name__ == "__main__":
    __main()
