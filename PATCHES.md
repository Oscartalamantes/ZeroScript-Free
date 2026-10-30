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

## Patch #1 — COMPLETE (Juno, 2026-10-22)
- bridge.py: ZS_BRIDGE_HOST (bind) + ZS_BRIDGE_TOKEN gate — sockets without ?t=<token> are closed (4401) before joining the client set when a token is set. Unset token = stock behavior.
- Extension: background.js reads zsHost/zsPort/zsToken from chrome.storage on every connect (defaults = stock localhost); popup gained Bridge address fields (host/port/token) with save + reconnect; manifest host_permissions adds ws://100.*/* for the Tailscale range.
- Purpose: let Juno reach this bridge over Tailscale with a token, so the laptop leg works without anyone relaying. Activation: pipeline job 010.

## Patch #2 — list_commands never dumps the catalogue into chat (Juno, 2026-10-27, Oscar's order)
Why: every agent attach made the model call list_commands and the extension pasted the full command prose back into the visible chat (stock ~30k chars; even the 2026-10-24 compact format ~11.5k / 69 lines). Oscar's Meta AI history filled with junk "Checking commands" chats he had to open one by one.
Change (core/main.js list_commands handler): the result is now ONE signature line per command — exact name + parameter keys, `*` = required — plus a two-line header/footer. No descriptions, no shared-params block, no TOOL_NOTES. Param mistakes still surface via each command's own ERROR text; the periodic toolsReminder already re-anchors exact names.
Change (core/config.js): system-prompt wording now calls list_commands the compact reference and states it is the ONLY version (never ask for a fuller one); toolsReminder's list_commands line updated to match; the execute_luau parenthetical no longer points at tips in the list_commands output.
Backups: core/main.js.bak-20261027-listcmd, core/config.js.bak-20261027-listcmd beside the files.
Live build note: the laptop's registered copies run the VAULT build (stock + 2026-10-24 size patch, ~/workspace/zeroscript-fix-vault) with this same Patch #2 applied on top — staged at ~/workspace/zeroscript-listcmd-fix/ and deployed via the juno-memory repo bundle zs-fix-20261027/. This fork's core/main.js is still the stock base + Patch #2 only (the 2026-10-24 size patch has not been transplanted into the fork yet).

## Patch #3 — purge + proper build: size patch transplanted, repo is source of truth (Juno, 2026-10-27, Oscar's order)
Why: the laptop's registered extension copies ran the vault build (stock + 2026-10-24 size patch) with Patch #2 bolted on, while this fork carried Patch #2 without the size patch — two divergent lines, three drifting copies on the laptop, and the size fix living only in a VM-side vault folder.
Change (core/main.js): the 2026-10-24 hard size guard transplanted verbatim into submitAndGetBase — ZS_SEND_CAP 12500, oversized injections split at paragraph boundaries and submitted as framed back-to-back parts. Patch #2's signature-format list_commands is unchanged.
Change (providers/meta.js): now byte-identical to the vault build — progressive write for texts >3000 chars (1800-char slices with an input event per slice) and sendCharBudget: 12500.
Cleanup: committed .bak-20261027-listcmd backups removed from the repo (backups belong on the laptop beside live files, not in source).
Deployment: all laptop extension copies purged to C:\Users\Etern\zeroscript-purge-archive-20261027\ except the Edge-registered copy, which is deployed byte-identical to this commit. The vault (~/workspace/zeroscript-fix-vault) is retired as an input — this repo is the single source of truth.

## Patch #4 - 2026-10-27 (Juno, Oscar's design): ONE canonical catalogue file, pulled once

Oscar's design, replacing the dump model entirely (the compact catalogue was
NOT the fix - it still fragmented across history chats):

- `catalogue/COMMANDS.md` (NEW, repo root): the full command catalogue in ONE
  canonical file - all 37 commands (28 roblox + 9 blender) with full
  descriptions, complete parameter specs (types, REQUIRED, enums, array item
  shapes) and the tested TOOL_NOTES. Generated 2026-10-27 from the live
  bridge's tools list, merged with core/config.js TOOL_NOTES.
- `core/config.js` (buildSystemPrompt): the first-loaded directive now
  carries the pointer - the catalogue lives in that one repo file; the first
  `list_commands` result IS the pull; it is never sent again.
- `core/main.js`: `pullCatalogue()` fetches the file once per session via the
  background worker (prefetch fired at session start). The first
  `list_commands` returns the pulled file as a single result; every later
  call returns only a confirmation stub. A failed pull returns an explicit
  ERROR - no silent fallback to any locally formatted dump.
- `background.js`: new `fetch_catalogue` message (20s timeout, no-store).
- `manifest.json`: host_permissions += https://raw.githubusercontent.com/*
