"""Shared environment bootstrap for Oscar's persistent-memory stack.

Both entry points (the MCP server ``memory_stack.py`` and the Juno-side
hook ``juno_bridge_integration.py``) import this FIRST, before importing
``hy_memory``, so the SDK always sees the same endpoints and store path.

Design (Oscar's, from his "Hy-Memory-30B-A3B Persistent Memory Stack -
Single Owner 30B" README):
  - Writer  = a local memory-writer LLM behind Ollama's OpenAI-compatible
    endpoint. Ships pointing at a model that exists on the OMEN today;
    swap MEMORY_LLM_MODEL to the Hy-Memory-30B-A3B GGUF once it is pulled
    (that is a config change, not a rebuild).
  - Reader  = whatever brain asks (the ZeroScript agent in the tab, or
    VoidMind through JunoMemoryBridge.before_answer).
  - Store   = disk-backed Chroma (+ Kuzu graph in ultra mode) under
    ~/juno/memory - survives reboots; updates link through supersedes
    chains, never overwrite.

No secrets live here: Ollama is local and keyless; the API key fields are
placeholders the OpenAI client requires.
"""

import os
from pathlib import Path


def memory_dir() -> Path:
    """The on-disk memory store root (created on demand)."""
    raw = os.environ.get("JUNO_MEMORY_DIR", "").strip()
    base = Path(raw).expanduser() if raw else Path.home() / "juno" / "memory"
    return base


def bootstrap_env() -> dict:
    """Set hy-memory's env vars (only where unset) and return the config."""
    # This stack talks ONLY to loopback endpoints (local Ollama). Proxy
    # env vars must never apply - and a malformed proxy value (e.g. a
    # bracketed IPv6 entry in NO_PROXY) makes httpx raise InvalidURL the
    # moment the SDK builds its HTTP client, killing every embed call.
    # Sanitize this process's proxy env before anything imports httpx.
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(var, None)
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"
    os.environ["no_proxy"] = "localhost,127.0.0.1"

    # Optional .env beside this stack (the laptop deploy writes one);
    # real environment variables always win.
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
    except Exception:
        pass

    base = memory_dir()
    base.mkdir(parents=True, exist_ok=True)

    ollama = os.environ.get("JUNO_OLLAMA_URL", "http://127.0.0.1:11434/v1")
    writer = os.environ.get("JUNO_MEMORY_WRITER", "llama3.1:8b")
    embedder = os.environ.get("JUNO_MEMORY_EMBEDDER", "nomic-embed-text")
    # nomic-embed-text is 768-dim; the SDK defaults to 1536 and would
    # reject every vector. Must match the embedder model.
    dims = os.environ.get("JUNO_MEMORY_EMBEDDING_DIMS", "768")

    defaults = {
        # Writer LLM (extraction / reconcile) - local Ollama.
        "MEMORY_LLM_BASE_URL": ollama,
        "MEMORY_LLM_API_KEY": "ollama",
        "MEMORY_LLM_MODEL": writer,
        # Embedder - local Ollama.
        "MEMORY_EMBEDDER_BASE_URL": ollama,
        "MEMORY_EMBEDDER_API_KEY": "ollama",
        "MEMORY_EMBEDDER_MODEL": embedder,
        "MEMORY_EMBEDDING_DIMS": dims,
        # Oscar's design is Chroma + Kuzu: in pro mode the SDK opens the
        # Kuzu graph store at startup when this is on.
        "MEMORY_ENABLE_GRAPH": "1",
        # Store location (hy-memory reads MEMORY_DATA_DIR; see SDK env ref).
        "MEMORY_DATA_DIR": str(base),
        "HY_MEMORY_DATA_DIR": str(base),
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)

    return {
        "dir": str(base),
        "ollama": ollama,
        "writer": writer,
        "embedder": embedder,
        "user_id": os.environ.get("JUNO_MEMORY_USER", "oscar"),
        "mode": os.environ.get("JUNO_MEMORY_MODE", "pro"),
    }


def make_client(mode: str = None, data_dir: str = None):
    """Construct the HyMemoryClient with the shared config.

    ``data_dir`` force-points the store elsewhere (the healthcheck's
    throwaway plumbing probe); ``mode`` overrides JUNO_MEMORY_MODE.
    """
    cfg = bootstrap_env()
    if data_dir is not None:
        os.environ["MEMORY_DATA_DIR"] = data_dir
        os.environ["HY_MEMORY_DATA_DIR"] = data_dir
        cfg = dict(cfg, dir=data_dir)
    from hy_memory import HyMemoryClient  # imported after env bootstrap

    return HyMemoryClient(mode=mode or cfg["mode"]), cfg
