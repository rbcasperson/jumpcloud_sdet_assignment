import subprocess
import time

import requests


class HashServeClient(requests.Session):
    def __init__(self, port, path_to_executable):
        super().__init__()
        self.port = port
        self.path_to_executable = path_to_executable
        self.base_url = f"http://127.0.0.1:{port}"
        self.server_process = None

    def start(self):
        """Start a fresh instance of the API server."""
        self.server_process = subprocess.Popen(
            [self.path_to_executable], env={"PORT": str(self.port)}
        )
        # A short sleep here ensures the server is running before anything tries to access it.
        # Ideally, we'd implement logic to wait until the server is responding,
        # but this is a temporary working solution.
        time.sleep(0.5)

    def stop(self):
        self.server_process.terminate()
        self.server_process = None

    def restart(self):
        if self.server_process:
            self.stop()

        self.start()

    def create_hash(self, password=None, payload=None):
        return self.post(
            f"{self.base_url}/hash",
            json={"password": password} if payload is None else payload,
        )

    def get_hash(self, job_id):
        return self.get(f"{self.base_url}/hash/{job_id}")

    def get_stats(self):
        return self.get(f"{self.base_url}/stats")

    def shut_down(self):
        return self.post(f"{self.base_url}/hash", data="shutdown")
