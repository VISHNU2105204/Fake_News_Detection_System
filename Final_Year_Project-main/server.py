"""
Compatibility shim so tests that `from server import CORSRequestHandler`
work even though the real implementation lives in `working_server.py`.

This file re-exports the handler and start_server entrypoint.
"""
from working_server import CORSRequestHandler, start_server, init_db  # re-export

__all__ = ["CORSRequestHandler", "start_server", "init_db"]


if __name__ == "__main__":
    # Ensure DB initialized then start the server when run directly
    try:
        init_db()
    except Exception:
        # init_db may already have been called by the imported module
        pass
    start_server()
