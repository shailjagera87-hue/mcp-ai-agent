
import os
import sys
import time
import socket
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SERVERS = [
    ("Weather MCP", "mcp_servers.weather_server.server", 8001),
    ("Finance MCP", "mcp_servers.finance_server.server", 8002),
    ("Database MCP", "mcp_servers.database_server.server", 8003),
]


def wait_for_port(name, port, process, timeout=60):
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"{name} exited unexpectedly.")

        try:
            with socket.create_connection(("127.0.0.1", port), timeout=2):
                print(f"{name} is ready on port {port}", flush=True)
                return
        except OSError:
            time.sleep(1)

    raise TimeoutError(f"{name} did not start on port {port}.")


def main():
    processes = []

    try:
        for name, module, port in SERVERS:
            print(f"Starting {name}...", flush=True)

            process = subprocess.Popen(
                [sys.executable, "-m", module],
                cwd=ROOT,
            )
            processes.append((name, process))

            wait_for_port(name, port, process)

        import uvicorn

        print("Starting FastAPI backend...", flush=True)

        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", "10000")),
            reload=False,
        )

    finally:
        for name, process in reversed(processes):
            if process.poll() is None:
                print(f"Stopping {name}...", flush=True)
                process.terminate()

        for name, process in reversed(processes):
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
