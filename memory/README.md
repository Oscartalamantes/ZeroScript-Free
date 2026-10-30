# Hy-Memory-30B-A3B Persistent Memory Stack — Single Owner 30B

Oscar's design, built 2026-10-30 (Juno, Patch #5). The design was drafted
inside a Meta AI chat and lived only there; this folder is the design on
disk, in the repo, where it belongs.

- **Writer** = a memory-writer LLM behind Ollama's OpenAI-compatible
  endpoint. Ships as `llama3.1:8b` (already on the OMEN). Swap
  `JUNO_MEMORY_WRITER` to `hf.co/rapatsky/Hy-Memory-30B-A3B-GGUF:Q4_K_M`
  after `ollama pull hf.co/rapatsky/Hy-Memory-30B-A3B-GGUF:Q4_K_M`
  completes — the dedicated Hy-Memory writer (Tencent Hunyuan, Apache
  2.0, 30B total / ~3B active). Config change only; nothing else moves.
  Note: the Q4_K_M GGUF is ~18 GB and the design targets a 24 GB card;
  the OMEN's RTX 5060 has 8 GB VRAM, so the writer runs RAM-offloaded as
  a background write path. Recall (embeddings + vector search) is fast
  and unaffected.
- **Reader** = any brain that asks: the ZeroScript agent in the tab via
  the `memory_recall` tool, or VoidMind via `JunoMemoryBridge`.
- **Store** survives reboots: disk-backed Chroma + Kuzu + supersedes
  chain at `~/juno/memory/` (on the laptop: `C:\Users\Etern\juno\memory`).
- **Framework** = Tencent's `hy-memory` SDK (`pip install hy-memory[all]`),
  three scenes (chat / working / coding), updates linked by supersedes —
  never overwritten.

## Pieces

| File | Job |
|---|---|
| `memory_stack.py` | MCP server "OscarMCP" (stdio child of bridge.py): `memory_recall`, `memory_remember`, `memory_correct`, `memory_forget`, `memory_list`, `memory_health`. `--healthcheck` self-test. |
| `juno_bridge_integration.py` | `JunoMemoryBridge(workspace_id="github.com/oscar/juno")`; `before_answer(user_query)` returns `formatted_prompt` for the reader's system prompt. |
| `_memenv.py` | Shared env bootstrap (endpoints, store path, writer/embedder). |
| `seed.jsonl` / `seed_memories.py` | Juno's verified standing facts, written once at deploy. |
| `.env.template` | Laptop config; copy to `.env` beside the stack. |

## How it loads automatically

1. The bridge autostarts at logon (pythonw, no window) and spawns this
   server from `config.json` next to roblox + blender.
2. The extension's startup directive (Patch #5) makes every new agent
   session call `list_commands` (the catalogue pull) and then
   `memory_recall` — both loads happen before the agent's first reply.
3. Oscar opens a fresh chat and it is already loaded. No history tabs,
   no pasting, no re-teaching. `/remember`, `/correct`, `/forget` in
   chat write back to the same store.

## Quick start (laptop)

```
pip install -r requirements.txt        # into the bridge's Python
copy .env.template .env                # adjust if needed
python memory_stack.py --healthcheck   # write / recall / forget proof
python seed_memories.py                # first boot only
```
