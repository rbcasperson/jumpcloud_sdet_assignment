import subprocess

import requests


class HashServeClient(requests.Session):
    def __init__(self, port, path_to_executable):
        super().__init__()
        self.port = port
        self.path_to_executable = path_to_executable
        self.base_url = f"http://127.0.0.1:{port}"

    def start(self):
        """Start a fresh instance of the API server."""
        subprocess.Popen([self.path_to_executable], env={"PORT": str(self.port)})

    def create_hash(self, password):
        return self.post(f"{self.base_url}/hash", json={"password": password})

    def get_hash(self, job_id):
        return self.get(f"{self.base_url}/hash/{job_id}")

    def get_stats(self):
        return self.get(f"{self.base_url}/stats")

    def shut_down(self):
        return self.post(f"{self.base_url}/hash", data="shutdown")
