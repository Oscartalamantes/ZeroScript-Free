"""JunoMemoryBridge - the Juno-side hook from Oscar's Hy-Memory design.

Any local brain (VoidMind's server today, the 30B reader in the design)
wraps its answer path with this bridge:

    from juno_bridge_integration import JunoMemoryBridge
    juno_memory = JunoMemoryBridge(workspace_id="github.com/oscar/juno")

    mem = juno_memory.before_answer(user_query)   # scene auto-detected
    # mem["formatted_prompt"] -> inject into the reader's system prompt

Writes ride the same store the MCP server (memory_stack.py / OscarMCP)
serves to ZeroScript sessions, so a fact learned in a Meta AI tab and a
fact learned by VoidMind land in ONE memory - Oscar never re-teaches
either side. Source tags are preserved end to end: this bridge writes as
source "juno"; the tab writes as "zeroscript"; Oscar's own corrections
arrive through whichever side he is talking to and outrank both.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _memenv import make_client  # noqa: E402


class JunoMemoryBridge:
    def __init__(self, workspace_id: str = "github.com/oscar/juno"):
        self.workspace_id = workspace_id
        self._client, self._cfg = make_client()

    # ── read path ──────────────────────────────────────────────────────
    def before_answer(self, user_query: str) -> dict:
        """Recall what memory knows about this query, formatted for
        injection into the reader model's system prompt."""
        cfg = self._cfg
        results = self._client.search(
            user_query, user_ids=[cfg["user_id"]], limit=10
        )
        mems = results.get("memories", {}) if isinstance(results, dict) else {}

        def lines(items):
            out = []
            for m in items or []:
                out.append(f"- {m.get('content', m) if isinstance(m, dict) else m}")
            return out

        sections = []
        if lines(mems.get("profile")):
            sections.append("## Who Oscar is\n" + "\n".join(lines(mems.get("profile"))))
        if lines(mems.get("normal")):
            sections.append("## Remembered facts\n" + "\n".join(lines(mems.get("normal"))))
        if lines(mems.get("proactive")):
            sections.append("## Open intentions\n" + "\n".join(lines(mems.get("proactive"))))

        formatted = ""
        if sections:
            formatted = (
                "[PERSISTENT MEMORY - Oscar's store at "
                f"{cfg['dir']}; his live words outrank this]\n"
                + "\n\n".join(sections)
            )
        return {
            "formatted_prompt": formatted,
            "memories": mems,
            "workspace_id": self.workspace_id,
        }

    # ── write path ─────────────────────────────────────────────────────
    def remember(self, text: str, source: str = "juno") -> None:
        self._client.add(text, user_id=self._cfg["user_id"], source=source)

    def correct(self, memory_id: str, new_text: str) -> None:
        self._client.update(memory_id, new_text)

    def forget(self, memory_id: str) -> None:
        self._client.delete(memory_id)

    def health(self) -> str:
        resp = self._client.list_memories(user_id=self._cfg["user_id"])
        count = 0
        if isinstance(resp, dict):
            count = (resp.get("vdb") or {}).get("total", 0)
        return (
            f"store={self._cfg['dir']} writer={self._cfg['writer']} "
            f"embedder={self._cfg['embedder']} count={count}"
        )
