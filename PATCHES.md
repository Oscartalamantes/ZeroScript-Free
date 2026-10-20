# Oscar's fork — patch log

Fork of sebattfg/ZeroScript-Free (GPL-3.0). Upstream remote = upstream; pull upstream fixes, then re-apply the patches below.
Baseline: v1.5.5, commit 32dd846.

## Step 0 — baseline (before ANY patch)
- [ ] Load THIS fork's `zeroscript-extension` folder in Edge (Load unpacked), replacing the stock one
- [ ] Run THIS fork's bridge via start.bat
- [ ] Start a session, one small Zero command → must work exactly like stock
- Rule: never patch on top of an unverified baseline.

## Setup prep (Juno, 2026-10-20, local + uncommitted)
- `config.json` now carries BOTH MCP servers: `roblox` (launch_studio_mcp.py) and `blender` (`uvx` + `mcp-for-blender`) — stock fork config only had roblox, so the fork could not drive Blender at all. On the laptop, uvx is installed (winget) and Blender's addon listens on 9876, so the blender row should come alive at bridge start.
- Bridge smoke-tested in a scratch copy on Juno's VM (Linux): binds ws://127.0.0.1:17613, answers the extension protocol (connected/pong/status), parses the 2-server config, launches both children, and survives their failure here (no uvx / no Studio on Linux) with "(other servers continue)" + auto-restart. Bridge core = verified. Still unverified until the laptop run: fork extension in Edge + both servers alive with real Studio/Blender.

## Patch #1 — configurable bridge address + pairing token (IN PROGRESS — bridge HOST half done locally 2026-10-19 by Juno, uncommitted; token check + extension half still pending baseline)
Why: stock extension hardcodes ws://127.0.0.1:17613 (background.js + manifest host_permissions).
Direct LAN connection without it requires the tunnel; with it, the phone browser can point at the laptop's LAN IP.
Status note: `bridge.py` now reads HOST from env ZS_BRIDGE_HOST (default 127.0.0.1, py_compile verified). Motivated by JunoClient: on 2026-10-19 the laptop ('eternal') joined Oscar's tailnet and Juno reached its TCP services, but bridge 17613 refused on the tailnet interface because stock binds localhost only. Running the fork bridge with ZS_BRIDGE_HOST=0.0.0.0 (plus the token check, once implemented) is the unlock. Do NOT run 0.0.0.0 without the token check on shared networks.

Changes:
- `zeroscript-extension/background.js`: read host/port from chrome.storage.local (keys zsBridgeHost/zsBridgePort), default 127.0.0.1:17613. Send token on connect (first WS message / query param).
- `zeroscript-extension/popup.html` + `popup.js`: Host, Port, Token fields + Save (storage permission already granted in manifest).
- `zeroscript-extension/manifest.json`: widen host_permissions for ws/http to `*://*/*` (personal fork; needed to reach a LAN IP).
- `bridge.py`: HOST from env ZS_BRIDGE_HOST (default 127.0.0.1 — unchanged behavior). Optional token check: env ZS_BRIDGE_TOKEN; when set, reject WS connections without it.

SECURITY (why the token is not optional): if the bridge listens on 0.0.0.0, anyone on the same Wi-Fi who finds port 17613 can run Luau in Oscar's Studio = remote code execution on the laptop. Token + home-network-only keeps it sane. The SSH tunnel route stays the zero-patch fallback.

## Test order for Patch #1
1. Laptop, extension pointed at 127.0.0.1 (regression — must behave like stock)
2. Laptop, bridge on ZS_BRIDGE_HOST=0.0.0.0 + token, extension pointed at laptop LAN IP
3. Phone (Quetta): load fork extension, set host = laptop LAN IP + token, start session
