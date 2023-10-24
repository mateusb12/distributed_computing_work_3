import subprocess
import time

import requests

from nabor.automated_stress_test.global_variables import DOCKER_COMPOSE_LOCATION


def check_number_of_active_routes(nginx_endpoint: str = "http://localhost:80", num_requests: int = 10) -> int:
    active_routes = set()
    for _ in range(num_requests):
        response = requests.get(nginx_endpoint)
        if 'X-Upstream' in response.headers:
            active_routes.add(response.headers['X-Upstream'])
    return len(active_routes)


def is_nginx_running() -> bool:
    """Returns True if the NGINX container is running, else False."""
    try:
        result = subprocess.run(["docker", "ps", "-q", "--filter", "name=final_results-nginx-1"],
                                capture_output=True, text=True)
        return result.stdout.strip() != ''
    except subprocess.CalledProcessError:
        print("Error in processing docker command.")
        return False


def shutdown_nginx_container():
    """Stops the NGINX container if it's running."""
    try:
        result = subprocess.run(["docker", "ps", "-q", "--filter", "name=final_results-nginx-1"],
                                capture_output=True, text=True)
        if result.stdout.strip() == '':
            print("NGINX container is not running.")
            return
        subprocess.run(["docker", "stop", "final_results-nginx-1"], check=True)
        print("NGINX container stopped.")
    except subprocess.CalledProcessError:
        print("Error in processing docker command.")


def start_nginx_container():
    """Waits for a specified duration and then starts the NGINX container."""
    try:
        subprocess.run(["docker", "start", "final_results-nginx-1"], check=True)
        print("NGINX container restarted.")

    except subprocess.CalledProcessError:
        print("Error in processing docker command.")


def restart_nginx_container(wait_time: int = 5):
    shutdown_nginx_container()
    time.sleep(wait_time)
    start_nginx_container()
    print("NGINX container restarted.")


def shutdown_nginx_route(instance_index: int):
    try:
        # Step 1: Shutdown the NGINX container
        shutdown_nginx_container()

        # Step 2: Modify the nginx.conf file directly
        conf_path = f"{DOCKER_COMPOSE_LOCATION}/nginx.conf"
        with open(conf_path, "r") as f:
            content = f.read()

        server_line = f"server wordpress{instance_index};"
        modified_content = content.replace(server_line, f"# {server_line}")

        with open(conf_path, "w") as f:
            f.write(modified_content)

        # Step 3: Restart the NGINX container
        start_nginx_container()

        print(f"Successfully commented out the route to wordpress{instance_index}")

    except Exception as e:
        print(f"Error shutting down the route for wordpress{instance_index}. Error: {e}")


def __main():
    print(check_number_of_active_routes())
    # shutdown_nginx_route(2)
    # print(check_number_of_active_routes())


if __name__ == "__main__":
    __main()
