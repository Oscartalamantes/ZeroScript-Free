# ZeroScript — canonical command catalogue

This file is the ONE source of command knowledge for the ZeroScript agent.
It lives in the GitHub repo Oscartalamantes/ZeroScript-Free (catalogue/COMMANDS.md).
At agent start, the extension pulls this file ONCE and hands it to the agent as the
single first list_commands result. The agent answers every command question from this
pulled copy. list_commands never prints the catalogue again after that one pull.

Generated 2026-10-27 from the live bridge: 37 commands across roblox, blender.
Parameter keys marked REQUIRED must always be sent. If a call fails, its ERROR text
names the parameter to fix — trust the ERROR over your memory of this file.

Call format (all commands except execute_luau): one fenced JSON block per reply,
`{"command": "name", "params": { ... }}`. execute_luau uses the ###LUA### block instead.

## Server: roblox (28 commands)

### upload_image

Upload a batch of images from http server to Roblox Asset Server, returning imagePath to assetId map, such as {"http://localhost/image.png" : "rbxassetid://12345678", "https://www.figma.com/api/mcp/asset/6dcff81e-b394-4640-b3b1-123456789" : "rbxassetid://12345679"}.

Parameters:
- `imagePaths` (array, REQUIRED) — An array of image paths to be uploaded.
  Array items: string
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### search_game_tree

Explore the Roblox game hierarchy tree with flat JSON output.
Returns an array of JSON objects representing instances in the Data Model, showing names, paths, and relationships.
Use optional filters to narrow down results by path, instance type, or keywords.
For detailed inspection of a specific instance's properties and attributes, use the Inspect Instance tool.

OUTPUT FORMAT:
Array of objects with:
{
  "name": "InstanceName",
  "className": "Part", 
  "fullPath": "Workspace.Folder.InstanceName",
  "parentName": "Folder",
  "childSummary": "5 children (3 Part, 2 Script)",  // Present if depth limit reached and children exist
  "unexploredChildCount": 5  // Present if depth limit reached with matching children
}

DEPTH LIMITING:
- Default max_depth: 3 levels from start point (absolute traversal depth)
- Absolute max: 10 levels
- max_depth limits how deep into the hierarchy we traverse, regardless of filters
- Beyond max_depth, children are summarized with counts by class type
- Nodes at depth limit show: "unexploredChildCount" and "childSummary"

EXAMPLES (every call must pass datamodel_type: use "Edit" in edit mode, or "Client"/"Server" during a playtest -- "Edit" is rejected while playing):
- Full tree (3 levels): search_game_tree(datamodel_type: "Edit")
- Workspace only: search_game_tree(datamodel_type: "Edit", path: "Workspace")
- ServerScriptService: search_game_tree(datamodel_type: "Edit", path: "ServerScriptService")
- All base scripts: search_game_tree(datamodel_type: "Edit", instance_type: "BaseScript")
- All parts: search_game_tree(datamodel_type: "Edit", instance_type: "Part")
- By keywords: search_game_tree(datamodel_type: "Edit", keywords: "player, character")
- Deep exploration: search_game_tree(datamodel_type: "Edit", max_depth: 6)
- Combined filters: search_game_tree(datamodel_type: "Edit", path: "Workspace", instance_type: "Part", keywords: "red")
- Client tree during a playtest: search_game_tree(datamodel_type: "Client", path: "Players")
- Server tree during a playtest: search_game_tree(datamodel_type: "Server", path: "Workspace")

Parameters:
- `datamodel_type` (enum: Edit | Client | Server, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `head_limit` (number, optional) — Maximum number of results to return. Default: 200. Prevents overwhelming output for large trees.
- `instance_type` (string, optional) — Filter by ClassName using IsA() check. Examples: 'BasePart', 'BaseScript', 'GuiObject', 'Model', 'Folder'. Case sensitive.
- `keywords` (string, optional) — Filter by instance name keywords (case-insensitive). Separate multiple keywords with commas or spaces. Instance name must contain at least one keyword. Examples: 'player', 'red, blue', 'button door'
- `max_depth` (number, optional) — Maximum absolute depth to traverse from start point. Default: 3, Absolute max: 10. Limits how deep we explore in the hierarchy regardless of filters. Beyond this depth, children are summarized instead of expanded.
- `path` (string, optional) — Start exploration from this path. Examples: 'Workspace', 'ServerScriptService', 'Workspace.Models'. Path is case-sensitive.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### script_search

Fast script search based on fuzzy matching against script names.
Use if you know part of the script name but don't know where it's located exactly.
Response will be capped to 10 results.
Make your query more specific if need to filter results further.
Note: Pattern matching is not supported such as asterisk (*) or question mark (?) wildcards.

Parameters:
- `keywords` (string, REQUIRED) — The comma-separated keywords string to search for in the game's scripts. Each keyword is case-insensitive.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### skill

Retrieve detailed knowledge, best practices, or reference material for a specific skill.
Skills provide domain-specific expertise that helps you produce better, more accurate results.

<available_skills>
  <skill>
    <name>rbx-configs-experimentation</name>
    <source>Roblox</source>
    <description>"IMPORTANT: Before writing hard-coded constants, using DataStores for simple tunable values, or suggesting a manual server restart to change a value — call this skill. Roblox's built-in ConfigService updates in-game values live without restarting servers and runs A/B experiments to measure impact on retention, engagement, and monetization. Use it to set up, integrate, debug, and optimize Experience Configs and experiments. Trigger when the creator wants to change game values without a restart (boss health, prices, drop rates, event timing, difficulty), add feature flags or toggles, run A/B tests or experiments, build live-ops or seasonal/timed content, tune balance across the player base, or mentions ConfigService, GetConfigAsync, or GetConfigForPlayerAsync."</description>
  </skill>
  <skill>
    <name>rbx-create-skill</name>
    <source>Roblox</source>
    <description>Guide the user through authoring or modifying a custom skill. Use when the user wants to create, edit, update, or rename a skill.</description>
  </skill>
  <skill>
    <name>rbx-debug</name>
    <source>Roblox</source>
    <description>Programmatically add breakpoints and inspect thread information to debug Roblox Studio games via MCP, plugins, or command scripts. Use as a more robust tool to investigate scripting bugs or verify script behavior beyond static analysis.</description>
  </skill>
  <skill>
    <name>rbx-device-simulator-lua</name>
    <source>Roblox</source>
    <description>Control the Studio Device Simulator to test UI across device form factors. Use when switching devices, testing orientations, running multi-device comparisons, or verifying UI layout via MCP tools (execute_luau + screen_capture).</description>
  </skill>
  <skill>
    <name>rbx-docs-search</name>
    <source>Roblox</source>
    <description>Look up Roblox documentation using the http_get tool — Engine API reference, creator guides (avatar, characters, Studio workflows), cloud API, and docs indexes. Use when you need accurate API details or how-to guidance.</description>
  </skill>
  <skill>
    <name>rbx-perf-profiling</name>
    <source>Roblox</source>
    <description>Analyze fine-grained performance data provided by the MicroProfiler through the LibMP Luau module. Use it to investigate CPU and GPU bottlenecks, identify the causes of frame-time spikes, and analyze memory allocations by subsystem.</description>
  </skill>
  <skill>
    <name>rbx-scene-analysis</name>
    <source>Roblox</source>
    <description>Analyze and optimize Roblox scenes using SceneAnalysisService — rendering, memory, instance composition, unparented instances, and animation/audio assets. Use when investigating performance, memory, or leaks in a place.</description>
  </skill>
  <skill>
    <name>rbx-unit-test</name>
    <source>Roblox</source>
    <description>Write, run, and debug Luau unit tests for ModuleScripts in Roblox Studio. Use this skill only when the user asks to add unit tests, improve test coverage, run existing tests, or debug failing tests. Do not use it for playtesting, gameplay QA, or validating visuals and UI feel.</description>
  </skill>
</available_skills>

When to use skills:
1. When the task involves a domain covered by an available skill
2. When you need best practices or conventions before writing or reviewing code
3. When you are unsure about the correct patterns or APIs for a specific area

Important:
1. Invoke the skill BEFORE writing code or taking action, not after
2. Follow the returned guidance closely in your response
3. Do not mention a skill without actually invoking it first

Parameters:
- `skill_name` (string, REQUIRED) — The name of the skill to retrieve. Options: rbx-configs-experimentation, rbx-create-skill, rbx-debug, rbx-device-simulator-lua, rbx-docs-search, rbx-perf-profiling, rbx-scene-analysis, rbx-unit-test
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### multi_edit

Makes multiple edits to a single script in one operation. More efficient than multiple single edits.
Can also create new scripts if the path doesn't exist (will need to specify className).

Example Call (correct):
- Args: {"file_path":"ReplicatedStorage.Platformer.Constants","edits":[{"old_string":"JUMP_COOLDOWN = 0.15","new_string":"JUMP_COOLDOWN = 0.3"}]}

Path Format:
- Use dot notation like "game.ServerScriptService.MyScript"

Creating New Scripts:
- If the script doesn't exist, it will be created using the provided className
- className is required when creating new scripts
- First edit with empty old_string ("") sets the initial content
- Subsequent edits work normally on the created content

Before Using:
- Read or search file to understand existing script contents
- For new scripts, provide className and start with empty old_string to set initial content

Important Notes:
- All edits are applied in sequence, in the order provided
- Each edit operates on the result of the previous edit
- All edits must be valid for the operation to succeed - atomic operation
- Plan edits carefully to avoid conflicts between sequential operations

Critical Requirements:
- old_string must match script contents exactly (including whitespace)
- old_string and new_string must be different
- className required only when creating new scripts
- For new files: first edit can have empty old_string to set initial content

When Making Edits:
- Ensure all edits result in correct, runnable code
- Don't leave code in a broken state
- Use replace_all for renaming variables across the entire script

Parameters:
- `className` (string, optional) — The class name of the script to create (e.g., 'Script', 'LocalScript', 'ModuleScript'). Required only when creating new scripts, leave empty if script already exists.
- `datamodel_type` (enum: Edit, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `edits` (array, REQUIRED) — An array of edit operations. For new scripts, first edit can have empty old_string to set initial content.
  Array item shape: { `new_string` (string, REQUIRED) — The text to replace it with (must be different from old_string); `old_string` (string, REQUIRED) — The text to replace (must match exactly). Use empty string for new script initial content.; `replace_all` (boolean, optional) — Replace all occurrences of old_string (optional, defaults to false) }
- `file_path` (string, REQUIRED) — The dot-notation path of the script (e.g., 'game.ServerScriptService.MyScript'). Will be created if it doesn't exist.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: old_string must match the script's current text EXACTLY, byte-for-byte, including tabs and spaces - otherwise you get 'old_string ... not found in current content'. ALWAYS script_read the file FIRST and copy the exact text. It replaces the FIRST match and does NOT warn on multiple matches, so a short old_string can silently edit the WRONG line and break the code - include enough surrounding context (whole lines) to be unique, or set replace_all:true for renames. old_string and new_string must differ ('identical old_string and new_string' otherwise). WATCH FOR BAD UNICODE in old_string: do NOT retype code that contains quotes or dashes - this chat can silently turn straight quotes " into curly ones and -- into a long unicode dash, which then do NOT byte-match the script and the edit fails. Paste old_string verbatim from script_read. (new_string may contain unicode safely - it is written as-is.) Edits apply in order, each on the result of the previous, and are atomic (all succeed or none). To CREATE a script: set className (Script/LocalScript/ModuleScript) and make the first edit old_string:"" with the full initial source. datamodel_type must be "Edit".

### start_stop_play

Start play the game or stop the play.

Parameters:
- `is_start` (boolean, REQUIRED) — true to start the game, false to stop the game and return to edit mode.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### get_console_output

Get the console output from the Studio output log.

Parameters:
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### user_mouse_input

Send one or more mouse actions in order: moveTo, mouseButtonDown, mouseButtonUp, mouseButtonClick, scrollUp, scrollDown, or wait. For mouseButtonDown, mouseButtonUp, and mouseButtonClick, set mouse_button to "left" or "right". After the first step that sets position (x/y or instance_path), later steps may omit coordinates and reuse that position.

Parameters:
- `actions` (array, REQUIRED) — Ordered list of mouse actions to perform.
  Array item shape: { `action` (enum: moveTo | mouseButtonDown | mouseButtonUp | mouseButtonClick | scrollUp | scrollDown | wait, REQUIRED) — The mouse action for this step.; `instance_path` (string, optional) — The instance path that the mouse should be moved to. for example: "LocalPlayer.PlayerGui.Frame", "game.Workspace.Folder.Frame". The path should start with game, LocalPlayer, or Workspace. If instance_path is provided, x and y will be ignored, vice versa.; `mouse_button` (enum: left | right, optional) — Required when action is mouseButtonDown, mouseButtonUp, or mouseButtonClick.; `wait_time_ms` (number, optional) — Delay in milliseconds before the next step. Required for wait; range 0 to 10000.; `x` (number, optional) — Screen X coordinate. Omit if instance_path is set or a prior step already established position (reused for scroll, mouse button actions, etc.).; `y` (number, optional) — Screen Y coordinate. Omit if instance_path is set or a prior step already established position (reused for scroll, mouse button actions, etc.). }
- `datamodel_type` (enum: Client, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: Simulates real player mouse actions during PLAY. Same requirement as user_keyboard_input: "datamodel_type":"Client" (auto-filled if omitted) AND the game RUNNING (start_stop_play {"is_start": true} first; fails in Edit mode). "actions" is an ORDERED array of OBJECTS - each step MUST be {"action": ...}, NOT a bare string (a missing/misnamed action gives 'Unknown mouse action: nil'). action is one of: moveTo | mouseButtonDown | mouseButtonUp | mouseButtonClick | scrollUp | scrollDown | wait. You MUST establish a position BEFORE any click/scroll: the FIRST step needs "x"/"y" (screen pixels) OR "instance_path" (starts with game/LocalPlayer/Workspace; if set, x/y are ignored) - else 'Either x and y, instance_path, or a prior action ... is required'. Later steps may omit x/y and reuse the last position (click then scroll at the same spot). mouseButtonDown/Up/Click need "mouse_button":"left" or "right". A "wait" step needs "wait_time_ms" (0-10000). Example: {"datamodel_type":"Client","actions":[{"action":"mouseButtonClick","mouse_button":"left","instance_path":"LocalPlayer.PlayerGui.Menu.PlayBtn"}]}.

### store_image

Load an image from a local file path and return an IMAGEID_<id> URI that can be passed to other tools (e.g. as attachedImageUri for generate_procedural_model).
Use this tool when you need to convert a local image file into an image URI that other tools accept.
Supported formats: png, jpg, jpeg. Max file size: 5MB.

Parameters:
- `filePath` (string, REQUIRED) — Absolute path to a local image file (png, jpg, or jpeg).
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### http_get

Fetches the content of a URL via HTTP GET request. Returns the response body as text.

Optionally searches the fetched content for a keyword (query parameter). When a query is provided:
- Returns only the matching sections with surrounding context lines, saving context window space.
- Returns a short "no match" message if the keyword isn't found.
- Use context_lines to control how many lines of context around each match (default: 3).
- Use return_full: true to get the entire document when the keyword matches.

Without a query, the full response body is returned.

Only the following URL patterns are allowed:
- https://create.roblox.com/docs/reference/engine (Roblox Engine API docs — URLs must end with .md or be llms.txt)
- https://create.roblox.com/docs/cloud (Roblox Cloud API docs — URLs must end with .md or be llms.txt)
- https://create.roblox.com/docs/performance-optimization (Roblox Performance Optimization docs — URLs must end with .md or be llms.txt)
- https://github.com/Roblox/libmp (Roblox LibMP repository — URLs must end with .md or be llms.txt)
- https://create.roblox.com/docs (Roblox Creator docs (guides, tutorials, etc.) — URLs must end with .md or be llms.txt)

Any URL that does not match one of the above rules will be rejected.
Only GET requests are supported. The full URL must be provided.

Examples:
- http_get(url: "https://create.roblox.com/docs/reference/engine/classes/Part.md")
- http_get(url: "https://create.roblox.com/docs/reference/engine/classes/Part.md", query: "Anchored")
- http_get(url: "https://create.roblox.com/docs/reference/engine/classes/BasePart.md", query: "Position", context_lines: 10)
- http_get(url: "https://create.roblox.com/docs/reference/engine/classes/Part.md", query: "Anchored", return_full: true)

Parameters:
- `context_lines` (number, optional) — Lines of surrounding context per match. Only meaningful when query is provided. Default: 3.
- `query` (string, optional) — Optional keyword to search for in the fetched content (case-insensitive literal match). When provided, only matching sections are returned.
- `return_full` (boolean, optional) — If true and query matches, return the entire document instead of just matched sections. Only meaningful when query is provided. Default: false.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `url` (string, REQUIRED) — The full URL to fetch. Must match one of the allowed URL patterns.

### character_navigation

Navigate the character to the given position, or instance.

Parameters:
- `datamodel_type` (enum: Client, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `instance_path` (string, optional) — The instance path that the character should be moved to. for example: "game.Workspace.Part","game.Workspace.Model". The path should start with game, LocalPlayer, or Workspace.
- `speed_multiplier` (number, optional) — speed multiplier, default is 1.0, 0.5 is half speed, 2.0 is double speed. minimum is 0.1, maximum is 10.0.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `x` (number, optional) — The x coordinate to move the character to. Required if instance_path is not provided.
- `y` (number, optional) — The y coordinate to move the character to. Required if instance_path is not provided.
- `z` (number, optional) — The z coordinate to move the character to. Required if instance_path is not provided.

### script_read

Reads a script from the Roblox workspace. The output will be returned with line numbers in format: LINE_NUMBER→LINE_CONTENT.
When using this tool to gather information, ensure you gather the COMPLETE context to fulfill the user's request.

Usage:
- This tool reads the entire script by default to provide complete context
- You can read multiple scripts in parallel for efficiency
- If you need to find specific symbols across multiple scripts, use the grep search tool
- Avoid re-reading the same script unless the script may have changed since the last read
- For very large scripts (thousands of lines), consider using grep_search to locate specific functions or patterns first

Path Format:
- The path needs to be a full path, with no wildcard matching
- Use dot notation like "game.ServerScriptService.MyScript"
- Script must already exist (use `file_search` or `grep_search` to find the script path first)
- Will only read existing scripts, never creates new ones

Parameters:
- `end_line_one_indexed_inclusive` (integer, optional) — The one-indexed line number to end reading at (inclusive). Required if should_read_entire_file is false.
- `should_read_entire_file` (boolean, optional) — Whether to read the entire script. Defaults to true.
- `start_line_one_indexed` (integer, optional) — The one-indexed line number to start reading from (inclusive). Required if should_read_entire_file is false.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `target_file` (string, REQUIRED) — The dot-notation path of the script to read (e.g., 'game.ServerScriptService.MyScript')

Tested usage note: Reads the WHOLE script by default with line numbers (LINE→CONTENT). Use it before multi_edit so your old_string matches exactly. target_file is a full dot-path; it never creates a script (use search/grep first to find the path).

### get_studio_state

Get the state of the studio, including current play state and available datamodel types. If the studio state is not expected, please call start_stop_play tool to start or stop the play.

Parameters:
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### screen_capture

Capture current edit-time screen, return the image data. If camera_position and look_at_position are provided, the camera will be temporarily set to the camera_position and look at the look_at_position.

Parameters:
- `camera_position` (array, optional) — The position of the camera to capture the screen from.
  Array items: number
- `capture_id` (string, REQUIRED) — Capture identifier such as 'ScreenCapture_1', 'ScreenCapture_2', etc.
- `look_at_position` (array, optional) — The position to look at.
  Array items: number
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### script_grep

Runs a search for a string pattern over all script contents in the game. To avoid overwhelming output, the results are capped at 50 matches.

Parameters:
- `query` (string, REQUIRED) — The string or Luau pattern to search for.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### wait_job_finished

Wait for a background job to finish. Returns the final status and details when the job reaches a terminal state (Completed, Failed, or Cancelled).

Pass the jobId returned when a tool was called with its 'async' argument set to true.

Only call this tool when:
- The user EXPLICITLY asks to wait for a backgrounded job to finish (e.g. "wait for it to complete", "let me know when it's done")
- You need to confirm a job's result before performing a follow-up action that depends on it

Parameters:
- `jobId` (string, REQUIRED) — The jobId returned when a tool was called with its 'async' argument set to true.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `timeout` (number, optional) — Maximum time in seconds to wait for the job to finish. Defaults to 600 seconds.

### generate_procedural_model

Creates 3D objects built from primitive parts (blocks, spheres, cylinders, wedges) as a ProceduralModel with configurable attributes.
Use this tool when the user wants to:
- Create or build a 3D object, model, character, creature, vehicle, building, scenery, or any physical thing in the workspace
- Generate something from a reference image
- Create an object with tunable parameters (e.g. "add attributes to control head size, arm length, color")
- Build anything described as "procedural", "parametric", "configurable", or "with attributes"

The output is a ProceduralModel: a scripted model whose appearance is controlled by user-editable attributes (like size, color, proportions). The user can tweak these attributes after generation without regenerating.

The tool automatically inserts the generated model into the workspace. You do not need to run any code afterward.

CRITICAL: This is a long-running generative tool. Default to calling it with the 'async' argument set to true, which runs the generation in the background and returns immediately with a jobId. Handle other tasks while the generation is in-progress, and only call the 'wait_job_finished' tool when you absolutely need the result.

Parameters:
- `async` (boolean, optional) — Run this tool asynchronously and return immediately with a jobId, without blocking on completion. Use this when you want to kick off the work (e.g. several generations at once, or when the user does not need to wait for the result) and continue with other tasks. The tool runs in the background and updates its own UI. Poll the returned jobId with the wait_job_finished tool only when you actually need the final result. If you DO need the result before proceeding, omit this argument (or set it false) and call the tool normally.
- `attachedImageUri` (string, optional) — The image URI (IMAGEID_<id>) from the user's attached image. Always pass this when the user provides a reference image.
- `partNames` (string, optional) — List of part names that define the structure of the generated model. Accepts a comma-separated string (e.g. 'body, left wheel, right wheel, door') or a JSON array of strings (e.g. ['body', 'left wheel', 'right wheel', 'door']). Required when segmentation='explicit'. Maximum 8 parts (excess will be truncated).
- `prompt` (string, REQUIRED) — A text description of what to create and what attributes to expose.
Pass the user's own words. If they mention specific configurable properties (e.g. "head size", "arm length", "wheel count"), include those in the prompt so the generated model exposes them as editable attributes.
If an image is attached and the user gave no text description, pass an empty string.
Do NOT describe or interpret the attached image — only pass the user's own words.

- `segmentation` (enum: auto | none | explicit, optional) — Controls how the model is broken into parts. Pick based on the user's wording:
- Omit (or "auto"): user did NOT mention parts/segmentation (e.g. "generate a car"). The tool will derive parts automatically via an internal LLM call.
- "none": user explicitly asked for no parts / a single piece (e.g. "generate a car with no parts", "as one mesh", "single piece").
- "explicit": user named specific parts (e.g. "a car with body and wheels"). You MUST also pass partNames with the user's listed parts (max 8).

- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: Unlike generate_mesh, this call does NOT yield: it returns immediately with a generationId while the model builds in the background and auto-inserts into the workspace once done - do NOT run other commands assuming the model already exists yet. Do NOT call wait_job_finished as a reflex right after this - but DO call it (pass the generationId) whenever you actually need the finished result before continuing: either the user explicitly asked to wait, or your next step depends on the model being done (e.g. editing/coloring it, checking its geometry).

### generate_texture

Re-textures an existing mesh using AI, given a text prompt describing the desired look. Requires a source MeshPart or Model. Replaces the source in place.

Parameters:
- `hintImage` (object, optional) — Optional reference image guiding the texture style. When provided, textPrompt may be an empty string.
- `instance_path` (string, optional) — Full Studio path to the source MeshPart or Model, e.g. "Workspace.Model1.Part2". Resolved directly — no live Studio selection required. If omitted, falls back to the current Studio selection (which must be exactly one MeshPart or Model).
- `model` (enum: Fast | Quality, optional) — Generation mode. "Fast" trades quality for speed. "Quality" (default) is a research preview that only supports a single-MeshPart source and can vary in results.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `textPrompt` (string, REQUIRED) — Text description of the desired texture/appearance, e.g. "rusty metal".

### segment_mesh

Segments an existing mesh into named sub-parts using AI. Requires a source MeshPart or Model and up to 5 part names (e.g. ["head", "body", "tail"]). Returns a new Model containing the segmented parts, inserted as a sibling of the source.

Parameters:
- `instance_path` (string, optional) — Full Studio path to the source MeshPart or Model, e.g. "Workspace.Model1.Part2". Resolved directly — no live Studio selection required. If omitted, falls back to the current Studio selection (which must be exactly one MeshPart or Model).
- `parts` (array, REQUIRED) — List of part names to segment the mesh into (max 5). Example: ["head", "body", "tail"].
  Array items: string
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### user_keyboard_input

Send one or more keyboard inputs to the game in order. Each step is keyDown, keyUp, keyPress (keyDown then keyUp), textInput, or wait.

Parameters:
- `actions` (array, REQUIRED) — Ordered list of keyboard actions to perform.
  Array item shape: { `action` (enum: keyDown | keyUp | keyPress | textInput | wait, REQUIRED) — The keyboard action for this step.; `instance_path` (string, optional) — The instance path that the keyboard input should be sent to. for example: "LocalPlayer.PlayerGui.Frame", "game.Workspace.Folder.Frame". The path should start with game, LocalPlayer, or Workspace.; `key_code` (enum: None | Backspace | Tab | Clear | Return | Pause | Escape | Space | QuotedDouble | Hash | Dollar | Percent | Ampersand | Quote | LeftParenthesis | RightParenthesis | Asterisk | Plus | Comma | Minus | Period | Slash | Zero | One | Two | Three | Four | Five | Six | Seven | Eight | Nine | Colon | Semicolon | LessThan | Equals | GreaterThan | Question | At | LeftBracket | BackSlash | RightBracket | Caret | Underscore | Backquote | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z | LeftCurly | Pipe | RightCurly | Tilde | Delete | World0 | World1 | World2 | World3 | World4 | World5 | World6 | World7 | World8 | World9 | World10 | World11 | World12 | World13 | World14 | World15 | World16 | World17 | World18 | World19 | World20 | World21 | World22 | World23 | World24 | World25 | World26 | World27 | World28 | World29 | World30 | World31 | World32 | World33 | World34 | World35 | World36 | World37 | World38 | World39 | World40 | World41 | World42 | World43 | World44 | World45 | World46 | World47 | World48 | World49 | World50 | World51 | World52 | World53 | World54 | World55 | World56 | World57 | World58 | World59 | World60 | World61 | World62 | World63 | World64 | World65 | World66 | World67 | World68 | World69 | World70 | World71 | World72 | World73 | World74 | World75 | World76 | World77 | World78 | World79 | World80 | World81 | World82 | World83 | World84 | World85 | World86 | World87 | World88 | World89 | World90 | World91 | World92 | World93 | World94 | World95 | KeypadZero | KeypadOne | KeypadTwo | KeypadThree | KeypadFour | KeypadFive | KeypadSix | KeypadSeven | KeypadEight | KeypadNine | KeypadPeriod | KeypadDivide | KeypadMultiply | KeypadMinus | KeypadPlus | KeypadEnter | KeypadEquals | Up | Down | Right | Left | Insert | Home | End | PageUp | PageDown | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 | F13 | F14 | F15 | NumLock | CapsLock | ScrollLock | RightShift | LeftShift | RightControl | LeftControl | RightAlt | LeftAlt | RightMeta | LeftMeta | LeftSuper | RightSuper | Mode | Compose | Help | Print | SysReq | Break | Menu | Power | Euro | Undo | ButtonX | ButtonY | ButtonA | ButtonB | ButtonR1 | ButtonL1 | ButtonR2 | ButtonL2 | ButtonR3 | ButtonL3 | ButtonStart | ButtonSelect | DPadLeft | DPadRight | DPadUp | DPadDown | Thumbstick1 | Thumbstick2 | Thumbstick1Up | Thumbstick1Down | Thumbstick1Left | Thumbstick1Right | Thumbstick2Up | Thumbstick2Down | Thumbstick2Left | Thumbstick2Right | MouseLeftButton | MouseRightButton | MouseMiddleButton | MouseBackButton | MouseNoButton | MouseX | MouseY | MousePosition | TouchPosition | MouseWheel | TrackpadPan | TrackpadPinch | MouseDelta | TouchDelta | TouchPinch | ButtonCenter | ButtonBack | ButtonUp | ButtonDown | ButtonLeft | ButtonRight, optional) — The key code to send to the game. Required when action is keyDown, keyUp, or keyPress.; `text_inputs` (string, optional) — The text to send to the game. Required when action is textInput.; `wait_time_ms` (number, optional) — The time to wait in milliseconds before the next action, required for wait action, range from 0 to 10000. }
- `datamodel_type` (enum: Client, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: Simulates a real player typing during PLAY. REQUIRES "datamodel_type":"Client" AND the game RUNNING - the Client datamodel only exists in play mode, so first call start_stop_play {"is_start": true}; in Edit mode this fails. (ZeroScript auto-fills datamodel_type:"Client" if you omit it, but the game must still be running.) "actions" is an ORDERED array of OBJECTS - each step MUST be {"action": ...}, NOT a bare string (a missing/misnamed action gives 'Unknown ... action: nil'). action is one of: keyDown | keyUp | keyPress (down+up) | textInput | wait. key_code uses Roblox KeyCode NAMES, not raw characters: Enter="Return", digits="Zero".."Nine", letters=single uppercase "A".."Z", plus "Space", "Backspace", "Tab", arrows "Up"/"Down"/"Left"/"Right", modifiers "LeftShift"/"LeftControl"/"LeftAlt" - REQUIRED on keyDown/keyUp/keyPress ('key_code is required' otherwise). To type a whole string use ONE textInput step with "text_inputs":"hello" instead of many keyPress. A "wait" step MUST carry "wait_time_ms" (0-10000) ('wait_time_ms is required for wait action' otherwise). Optional "instance_path" routes input to a focused GUI element and must start with game, LocalPlayer or Workspace (e.g. "LocalPlayer.PlayerGui.Menu.NameBox"); omit it to send to whatever currently has focus. Example: {"datamodel_type":"Client","actions":[{"action":"textInput","text_inputs":"hi"},{"action":"keyPress","key_code":"Return"}]}.

### generate_mesh

Generates a textured mesh from a prompt using AI.

Parameters:
- `async` (boolean, optional) — Run this tool asynchronously and return immediately with a jobId, without blocking on completion. Use this when you want to kick off the work (e.g. several generations at once, or when the user does not need to wait for the result) and continue with other tasks. The tool runs in the background and updates its own UI. Poll the returned jobId with the wait_job_finished tool only when you actually need the final result. If you DO need the result before proceeding, omit this argument (or set it false) and call the tool normally.
- `maxTriangles` (number, optional) — The maximum number of triangles for the generated mesh. If provided, this must be between 12 and 20000 (inclusive).
- `partNames` (string, optional) — List of part names defining the schema for the generated mesh. Accepts a comma-separated string (e.g. 'body, left wheel, right wheel') or a JSON array of strings (e.g. ['body', 'left wheel', 'right wheel']). Required when segmentation='explicit'. Maximum 8 parts (excess will be truncated).
- `segmentation` (enum: auto | none | explicit, optional) — Controls how the mesh is broken into parts. Pick based on the user's wording:
- Omit (or "auto"): user did NOT mention parts/segmentation (e.g. "generate a car"). The tool will derive parts automatically via an internal LLM call.
- "none": user explicitly asked for no parts / a single piece (e.g. "generate a car with no parts", "as one mesh", "single piece").
- "explicit": user named specific parts (e.g. "a car with body and wheels"). You MUST also pass partNames with the user's listed parts (max 8).

- `size` (object, optional) — The generation's bounding box size. The generation will try to fit within this volume. Try to approximate a good size based on textPrompt.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `textPrompt` (string, REQUIRED) — The text prompt describing the mesh to generate.

Tested usage note: Unlike generate_procedural_model, this call YIELDS: it blocks until the AI mesh generation finishes and only then returns the result (the finished mesh) - there is no separate poll/wait step needed, just wait for the response.

### subagent

Launch a specialized subagent to handle complex, multi-step tasks autonomously.
Subagents are independent AI assistants with restricted tool access and specialized instructions.

<available_subagents>
  <subagent>
    <name>explore</name>
    <description>Fast agent specialized for exploring codebases and searching for information. Use this when you need to:
- Find files by patterns (e.g., "scripts with 'player' in the name")
- Search code for keywords or patterns (e.g., "how are touch events handled?")
- Answer questions about the codebase structure
- Query the current game state via Luau execution
- Understand existing game architecture before making changes
- Gather context from multiple files before deciding on an approach</description>
  </subagent>
</available_subagents>

When to use subagents:
1. When you need to explore the codebase before making decisions
2. When a task requires multiple search/read steps across many files
3. When you're uncertain about the right approach and need autonomous investigation
4. To separate concerns (e.g., explore first, then modify)

Important:
1. Subagents return a final text result summarizing their work
2. You cannot have a back-and-forth conversation with a subagent
3. Subagents cannot spawn other subagents (no nesting)
4. Choose the most specific subagent for your task

Parameters:
- `description` (string, REQUIRED) — A short 3-5 word description of the task in present continuous tense (e.g., 'Exploring player spawn logic', 'Finding lighting scripts'). Used for display.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `subagent_type` (string, REQUIRED) — The type of subagent to invoke. Options: explore, screen_capture, unit_test
- `task` (string, REQUIRED) — Detailed task description and instructions for the subagent. Be specific about what you need the subagent to do and what information to return.

### execute_luau

Executes Luau code in Roblox Studio. Returns the result of the executed code or an error message if the code fails to execute.

Code runs on Studio's main thread; until it yields, Studio is frozen, the script can't be stopped, and the MCP connection may drop. For heavy work (bulk instance creation or edits, procedural or terrain generation, large loops), split it into logical chunks (e.g. per region, or batches of ~1000 items) and call `task.wait()` once per chunk, not per item. When creating many instances, build each chunk in a container outside the DataModel and parent it before that chunk's `task.wait()`. The cost of a .Parent write into the DataModel scales with the total size of the subtree being inserted (all descendants), so parenting one large container is itself a single unyielding operation that can freeze Studio or drop the connection, no matter how incrementally the container was built. Keeping each flushed subtree small (one chunk's worth) bounds the cost of every .Parent write. A loop that waits for state to change (e.g. `while not ready do`) must call `task.wait()` inside it.

Parameters:
- `code` (string, REQUIRED) — The Luau code to execute.
- `datamodel_type` (enum: Edit | Client | Server, REQUIRED) — The target datamodel to operate on, the tool can only be performed in those datamodel types. call get_studio_state to get current available datamodel types. if the target datamodel is not available in current mode, consider using start_stop_play to switch to the desired mode and then use the tools. This is a required argument.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: Use `return` to produce output - `print()` is NOT captured (a script with only print() returns nil). Only the FIRST returned value is shown: `return a, b` shows just `a`; to return several values return ONE table, e.g. `return {ok=true, n=3}` (tables come back as JSON). Runs synchronously with a ~20s budget: a brief `task.wait(1)` is fine, but anything that can block or never resolve will TIME OUT. ALWAYS pass a timeout to WaitForChild - write `obj:WaitForChild("X", 5)`, NEVER `obj:WaitForChild("X")`: without the timeout it blocks until the budget kills the whole call. Same for `:Wait()` on events, infinite loops, HttpService/DataStore - set those up inside a real Script/LocalScript instance instead, never directly in execute_luau. Property types must match exactly (e.g. Position needs Vector3.new(...), not a string). On error you get a long internal stack prefix - the REAL message is the LAST segment after the final ':' (e.g. '... : Vector3 expected, got string', or 'Failed to parse command code' for a syntax error). Create objects with Instance.new and set .Parent; reach services via game:GetService("Name").

### generate_material

Returns the BaseMaterial and Name of the generated MaterialVariant. To use, these must both be set to the Material and MaterialVariant properties of BaseParts, respectively.

Parameters:
- `async` (boolean, optional) — Run this tool asynchronously and return immediately with a jobId, without blocking on completion. Use this when you want to kick off the work (e.g. several generations at once, or when the user does not need to wait for the result) and continue with other tasks. The tool runs in the background and updates its own UI. Poll the returned jobId with the wait_job_finished tool only when you actually need the final result. If you DO need the result before proceeding, omit this argument (or set it false) and call the tool normally.
- `baseMaterial` (enum: Plastic | SmoothPlastic | Wood | WoodPlanks | Marble | Basalt | Slate | CrackedLava | Concrete | Limestone | Granite | Pavement | Brick | Pebble | Cobblestone | Rock | Sandstone | CorrodedMetal | DiamondPlate | Foil | Metal | Grass | LeafyGrass | Sand | Fabric | Snow | Mud | Ground | Asphalt | Salt | Ice | Glacier | Cardboard | Carpet | CeramicTiles | ClayRoofTiles | RoofShingles | Leather | Plaster | Rubber, REQUIRED)
- `materialDescription` (string, REQUIRED)
- `materialId` (string, REQUIRED)
- `materialPattern` (enum: Regular | Organic, REQUIRED)
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### inspect_instance

Inspect a specific Roblox instance to get all its properties, attributes, and children summary.
Returns detailed information about instances including all readable properties, custom attributes, 
and a comprehensive summary of immediate children and recursive child counts.
If multiple instances match the same path, all matches will be returned.
Use this tool after using GameTree to explore specific instances in detail.

SINGLE MATCH OUTPUT FORMAT:
{
  "name": "MyPart",
  "className": "Part",
  "path": "Workspace.MyPart",
  "uniqueId": "1234567890ABCDEF",
  "properties": {
    "Anchored": true,
    "CanCollide": true,
    "CFrame.Position": "0, 10, 0",
    "CFrame.Rotation": "1, 0, 0, 0, 1, 0, 0, 0, 1",
    // ... all other readable properties
  },
  "attributes": {
    "CustomTag": "PlayerSpawn",
    "SpawnDelay": 5,
    "IsActive": true
  },
  "children": {
    "immediateChildren": [
      {
        "className": "Part",
        "path": "Workspace.MyPart.ChildPart"
      },
      {
        "className": "Model",
        "path": "Workspace.MyPart.ChildModel"
      }
    ],
    "childrenCount": 2,
    "totalDescendants": 8
  }
}

CHILDREN SUMMARY FIELDS:
- immediateChildren: Array of direct children with className and path only (no name, childCount, or uniqueId)
- childrenCount: Number of direct children
- totalDescendants: Total count of all descendants (children, children's children, etc.)

uniqueId is included for the main inspected instance when available. This is a unique identifier for each instance in the DataModel.

MULTIPLE MATCHES OUTPUT FORMAT:
{
  "matches": [
    { 
      "name": "MyPart", 
      "className": "Part", 
      "path": "Workspace.MyPart",
      "uniqueId": "RBX1234567890ABCDEF",
      "properties": {...}, 
      "attributes": {...},
      "children": {...}
    },
    { 
      "name": "MyPart", 
      "className": "MeshPart", 
      "path": "Workspace.MyPart",
      "uniqueId": "RBX9876543210FEDCBA",
      "properties": {...}, 
      "attributes": {...},
      "children": {...}
    }
  ],
  "count": 2,
  "totalFound": 2,
  "note": "Multiple instances found with path 'Workspace.MyPart'. All 2 matches are included below."
}

WHEN TOO MANY MATCHES (>20):
{
  "matches": [ /* first 20 matches with full details */ ],
  "count": 20,
  "totalFound": 45,
  "note": "Multiple instances found with path 'Workspace.Part'.",
  "warning": "Found 45 total matches, but only showing first 20 due to output limits. Consider using a more specific path to narrow down results."
}

PATH SPECIFICATION:
- Use dot notation: "Workspace.Model.Part"
- Can include or omit "game." prefix
- Path must match instance hierarchy
- If multiple instances have the same name at the same level, all will be returned
- Maximum of 20 matches will be returned (with warning if more exist)

EXAMPLES:
- Inspect with children: InspectInstance(path: "Workspace.Baseplate")
- Multiple matches: InspectInstance(path: "Workspace.Part") → Returns up to 20 Parts with children summary
- Case-insensitive: InspectInstance(path: "workspace.baseplate")
- Inspect script: InspectInstance(path: "ServerScriptService.MainScript")
- Inspect GUI: InspectInstance(path: "StarterGui.ScreenGui.Frame")
- With game prefix: InspectInstance(path: "game.Workspace.Model")

CHILDREN SUMMARY USE CASES:
- Understand instance hierarchy structure
- Count total descendants for performance considerations
- See immediate children for navigation purposes
- Identify complex models with many nested children
- Plan traversal strategies for large hierarchies

Parameters:
- `path` (string, REQUIRED) — Path to the instance(s) to inspect using dot notation (case-insensitive). Returns detailed properties, attributes, and children summary. If multiple instances match, up to 20 will be returned with a warning if more exist. Example: 'Workspace.Model.Part' or 'workspace.model.part'
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

Tested usage note: Path is dot-notation and case-insensitive, e.g. 'Workspace.Model.Part'. Returns all readable properties, attributes, and a children summary (not the children's properties - inspect them separately). If several instances share the path, up to 20 matches are returned. Use this to read exact property names/values before editing them with execute_luau.

### search_asset

Searches for assets across Creator Store (public marketplace) and Creator Inventory (user/group/universe).
Use this tool to find assets by keyword before inserting them with insert_asset.
Returns a list of matching assets with metadata (name, type, source, price).

Scope controls where to search:
- 'auto' (default): waterfalls through universe inventory → universe's owning group → user inventory → Creator Store. Best for general "find me an X" requests.
- 'creator_store': searches only the marketplace. Use this when the user wants marketplace assets, paid assets, or when using price/creator filters.
- 'user': searches the user's personal inventory only.
- 'group': searches the universe's owning group by default. Pass groupId or groupName to search a different group instead. If the universe has no owning group and you don't pass a groupId, the response lists the user's groups so you can retry.
- 'universe': searches the current universe's inventory only.

Targeting a specific group: when the user names a particular group ("in my group X" / "in group 12345"), set scope='group' AND pass groupId or groupName to constrain to that one group. groupId/groupName are only valid with scope='group'; combining with any other scope (including 'auto') is rejected.

Result attribution: each inventory result includes `creatorId` (string, the group or user ID that owns the asset) and `creatorName` (the group/user name when known). `creatorId` semantics depend on `source`: for source='inventory' coming from a group, it's the group ID.

Every scope='group' or scope='auto' response includes a `groups` field listing { id, name } for each of the user's groups (when the user has any). Use these to make a follow-up scope='group' + groupId call when the default (the universe's owning group, or the first relevant group) doesn't match what the user wants.

Every response also includes a `context` field describing the current Studio session: { userId, universeId, isPublished, creatorType ('User'/'Group' when published), creatorId, creatorName }. Use this to ground answers about which place is being edited and to disambiguate "in my group" requests.

Cross-owner inserts caution: when an inventory result's creatorId differs from context.creatorId (the place's owner), inserting it brings another owner's asset into this place. The user may have access to view the asset but might not intend or have the authority to share it across owners. Before calling insert_asset on a cross-owner result, name the source (the asset's creatorName) and the destination (context.creatorName or universe), and ask the user for explicit consent.

When to use price filters: If the user asks for paid/premium assets or specifies a price range, set scope='creator_store' and use priceFilter, minPriceCents, and/or maxPriceCents. These filters only apply to Creator Store searches.
When to use asset type: If the user asks for a specific asset type (audio, decals, meshes, packages, etc.), set assetType to filter results. The inventory API requires exactly one assetType per call and defaults to 'Model' when omitted, so cross-type discovery requires explicit assetType=Image / Audio / etc. Packages are stored as Models with a Package subtype — set assetType='Package' to find them (do not search for the word "package" as a query).
Inventory results (source='inventory') are always insertable. Creator Store results may occasionally be restricted — if insert fails, try the next result.
Each result includes a thumbnailUrl (Roblox Thumbnails API). Fetch it to get JSON with data[0].imageUrl pointing to a CDN image of the asset — useful for visually comparing assets before inserting.

Parameters:
- `assetType` (enum: Model | Audio | Mesh | MeshPart | Image | Decal | Video | Package, optional) — Filter by asset type. Use 'Image' for user-uploaded images (most decals/textures uploaded today are stored as Image, not Decal). Use 'Package' when the user asks about packages — packages are Models with a Package subtype, so a keyword search for 'package' won't find them.
- `audioMaxDuration` (number, optional) — Maximum audio duration in seconds (only when assetType='Audio').
- `audioMinDuration` (number, optional) — Minimum audio duration in seconds (only when assetType='Audio').
- `excludeSources` (array, optional) — With scope='auto': skip these sources from the waterfall.
  Array items: string (user | group | universe | creator_store)
- `facets` (array, optional) — Additional keywords to refine the search (Creator Store only, ignored for inventory scopes). Facets narrow results by related concepts — e.g. for a 'lion' search: 'mane', 'safari', 'realistic', 'animated'. Available facets depend on the query.
  Array items: string
- `groupId` (string, optional) — Numeric group ID to constrain group inventory searches to a single group. Only valid with scope='group'. Mutually exclusive with groupName.
- `groupName` (string, optional) — Group name to constrain group inventory searches to a single group. Matched case-insensitively against the user's groups. Only valid with scope='group'. If the name doesn't match any of the user's groups, the response includes a `groups` field listing valid options. Mutually exclusive with groupId.
- `includeSources` (array, optional) — With scope='auto': only search these sources (e.g. ['user', 'creator_store']).
  Array items: string (user | group | universe | creator_store)
- `maxPriceCents` (number, optional) — Maximum price in cents. Requires scope='creator_store'. Use with minPriceCents for a price range.
- `maxResults` (number, optional) — Number of results to return (1-20, default 5).
- `minPriceCents` (number, optional) — Minimum price in cents. Requires scope='creator_store'. Use with maxPriceCents for a price range (e.g. minPriceCents=100, maxPriceCents=5000).
- `priceFilter` (enum: free | paid | all, optional) — Price filter. Requires scope='creator_store'. 'free' returns only free assets, 'paid' returns only paid assets, 'all' (default) returns both.
- `query` (string, optional) — Search term. Can be empty when filtering by assetType alone (e.g. to list all packages). Supports multi-term search with '+' (e.g. 'red+car') and exact phrase with quotes (e.g. '"red+car"').
- `scope` (enum: auto | creator_store | user | group | universe, optional) — Where to search. 'auto' (default) waterfalls through all available sources. Use explicit scope to target a single source.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances
- `tags` (array, optional) — Tags to filter by (Creator Store only, ignored for inventory scopes). Tags are category labels like 'Vehicle', 'Airplane', 'Fantasy'.
  Array items: string
- `verifiedCreatorsOnly` (boolean, optional) — Only return results from verified creators (Creator Store only).

### insert_asset

Inserts an asset into the game by its numeric Roblox asset ID.
Use this tool when you have a specific asset ID to insert directly, rather than searching the Creator Store.
The asset will be loaded, validated, and placed in the scene.
Always provide assetName when you know the name of the asset (e.g. from search results or user request). The inserted instance will be named using assetName — if omitted, it defaults to a generic name.
Supports models, meshes, images/decals, audio, video, animations, and packages.

Parameters:
- `assetId` (string, REQUIRED) — Numeric Roblox asset ID to insert.
- `assetName` (string, optional) — Name for the inserted instance in the game tree. Always provide this when you know the asset name (e.g. from search_asset results). If omitted, defaults to a generic name.
- `assetType` (enum: Model | Package | Mesh | MeshPart | Image | Decal | Audio | Video | Animation, optional) — Asset type hint. If provided, skips the metadata API lookup and uses this type directly. Use when the caller already knows the asset type (e.g. from inventory search results). 'Image' and 'Decal' both insert as a Decal instance.
- `parentPath` (string, optional) — DataModel path to parent the asset under (e.g. game.Workspace.Folder1). Defaults to workspace.
- `studio_id` (string, REQUIRED) — Selects Roblox Studio instance, use the list_roblox_studios tool to get available instances

### list_roblox_studios

Lists the connected Roblox Studio instances so a call can be directed at one. Several instances are commonly open at once, so every tool call must include a `studio_id` identifying the target instance — call this tool first to obtain the ids. Each result has an `id` and a human-readable `name` (including its place id or file name); use the `name` to choose the intended instance, confirming with the user before modifying their game.

Parameters: none.

## Server: blender (9 commands)

### get_addon_status

Check the connected Blender: its version, whether the addon matches this server, and which
asset libraries and 3D generators are switched on. Call it once at the start.

`libraries` are the search_assets sources and `generators` the generate_3d providers, each
on or off for this user. "(Premium)" ones come with MCP for Blender Premium and don't use the
user's own API keys. When pointing the user to Premium, link
https://mcp-for-blender.com/premium?ref=mcp-status

If outdated, tells the user how to update via `uvx mcp-for-blender install-addon`
(then restart or re-enable the addon in Blender).

`telemetry_consent` reports whether data collection is on, off, or null if
Blender could not be reached. Use it to answer telemetry status questions.

Parameters:
- `user_prompt` (string, optional) [default: ""]

### disable_telemetry

Turn OFF collection of prompts, code, screenshots and scene data.

Use this whenever the user asks to stop data collection, opt out of
telemetry, or stop sharing their data. Takes effect immediately.

This tool can only turn collection OFF. Turning it back on is done by the
user in Blender under Preferences > Add-ons > Blender MCP.

Parameters:
- `user_prompt` (string, optional) [default: ""]

### get_scene_info

Facts about the scene as text: what's there, where, how big, and how healthy meshes and rigs
are. No image; to see the scene, use look.

One header line (object counts, active, selection, mode), then one line per object with the
fields you ask for. Top-level objects by default; root="Name" lists that object's hierarchy,
query="chair" lists every object whose name contains the text. For anything else about an
object, read it with execute_blender_code.

Parameters:
- fields: What to show per object (default: location, size, children, hidden).
  placement: location (world), size (world bounding box), ground (on ground, floating or
    below by), rotation (degrees), scale, parent
  contents: children (count), hidden, details (faces, bones or light power), materials,
    modifiers, animation
  health: topology (quads, tris, ngons, non-manifold and boundary edges, loose verts,
    poles), weights (vertices no deform bone moves, deform bones with no vertex group)
  settings: adds a line with the file, engine, frame range, resolution, camera, HDRI and
    unit scale
- query: Name filter across all objects.
- root: Object whose hierarchy to list.
- limit: Maximum object lines (default 20).
- user_prompt: The user's own words describing what they want, quoted verbatim.

Parameters:
- `user_prompt` (string, optional) [default: ""]
- `query` (any, optional) [default: null]
- `root` (any, optional) [default: null]
- `fields` (any, optional) [default: null]
- `limit` (integer, optional) [default: 20]

### execute_blender_code

Run Python in the user's live Blender (bpy, bmesh, mathutils). Whatever it prints is returned.

Work in small steps and print what you need to know.

Parameters:
- code: The Python code to execute
- user_prompt: The user's own words describing what they want, quoted verbatim (do not paraphrase or summarise). Pass the same goal on every call in a multi-step task so each action is linked to the intent behind it. Never substitute your own sub-goal, plan step, or status text; if the user has given no new instruction, repeat their previous words unchanged.

Parameters:
- `code` (string, REQUIRED)
- `user_prompt` (string, optional) [default: ""]

### record_trajectory_feedback

Record evaluation feedback for a captured trajectory step.

Call it when the user reacts to a result: "accept" when they keep it ("looks good"),
"reject" or "undo" when they reject it or ask to undo, and "correction" with their words
as correction_text when they correct you ("too dark", "make it taller").

Parameters:
- feedback: One of accept | reject | undo | correction
- correction_text: Optional free-text correction or follow-up (especially for correction)
- step_index: Optional 0-based step index; defaults to the last recorded step
- user_prompt: Optional goal/prompt context for the feedback row

Parameters:
- `feedback` (string, REQUIRED)
- `correction_text` (any, optional) [default: null]
- `step_index` (any, optional) [default: null]
- `user_prompt` (string, optional) [default: ""]

### look

See the scene as one image. For counts, sizes and positions, use get_scene_info.

Choose where from (mode) and how it's drawn (shading):
- mode: viewport (what the user sees; default), camera (through the scene camera, at the
  render aspect), angles (the target from several sides, auto-framed; default front, right,
  top, three_quarter), frames (a strip over the animation).
- shading: solid, material, rendered (EEVEE and Workbench only), wireframe (edges over a
  plain surface), xray (see-through, bones in front). Default: the viewport's.
- image: Instead of the scene, show this image: "Render Result" after a render, another
  image in the file, or a file path.

Parameters:
- target: Object names to frame (children included). Default: every visible object.
- views: For angles: up to 6 of front, back, left, right, top, three_quarter, or [x, y, z]
  directions from the target towards the eye ([0, -1, 0.2] is front, slightly above).
- distance: Metres from the target's centre to the eye, for angles and frames views. Default:
  far enough to fit it; closer for detail or to stand inside a room.
- frames / frame_count: For frames: explicit frame numbers, or how many to sample (2-12).
- view: For frames: "camera", an angle name or an [x, y, z] direction; default the viewport.
- max_size: Longest side in pixels (default 768). Images stay in the conversation, so go
  smaller for quick checks and larger only to read fine detail.
- user_prompt: The user's own words describing what they want, quoted verbatim.

Every setting changed to take the picture is restored afterwards.

Parameters:
- `mode` (any, optional) [default: null]
- `target` (any, optional) [default: null]
- `views` (any, optional) [default: null]
- `distance` (any, optional) [default: null]
- `shading` (any, optional) [default: null]
- `frames` (any, optional) [default: null]
- `frame_count` (integer, optional) [default: 6]
- `view` (any, optional) [default: null]
- `image` (any, optional) [default: null]
- `max_size` (integer, optional) [default: 768]
- `user_prompt` (string, optional) [default: ""]

### generate_3d

Make one new textured 3D model from a text prompt or an image, and import it.

One object per call: not a whole scene, the ground, or parts to assemble. It arrives at
arbitrary scale and facing (meshy: real-world size, origin at the bottom). Each call can cost
the user money or a monthly generation, so duplicate a generated object for repeats.

Waits up to wait_seconds (at most 45), then imports. Generation usually takes 1-3 minutes: if
it isn't done in time you get a job handle; call generate_3d(job=..., name=...) again to keep
waiting. Repeating a request whose generation is still unfinished resumes it instead of paying
again.

Parameters:
- prompt: Short English description of one object ("weathered wooden treasure chest").
- image: Instead of a prompt: an absolute image file path or an http(s) URL. Images attached in
  chat can't be passed: ask the user for a path or URL, don't fall back to text without asking.
- name: Object name in the scene. Defaults to one made from the prompt.
- provider: auto (default), tripo, hunyuan3d, hyper3d or meshy. Auto prefers the user's MCP for
  Blender Premium generators, then their own API keys.
- quality: "standard" or "high" (Premium, not meshy). Omit for the user's default; "high" only
  when the user asks for more detail.
- bbox_condition: hyper3d only: [length, width, height] proportions.
- pose_mode: meshy only: "a-pose" or "t-pose" when the user asks for a character in an A-pose
  or T-pose (often to rig it).
- job: A handle from an earlier call, to resume waiting for it.
- user_prompt: The user's own words describing what they want, quoted verbatim.

Parameters:
- `prompt` (any, optional) [default: null]
- `image` (any, optional) [default: null]
- `name` (any, optional) [default: null]
- `provider` (string, optional) [default: "auto"]
- `quality` (any, optional) [default: null]
- `bbox_condition` (any, optional) [default: null]
- `pose_mode` (any, optional) [default: null]
- `job` (any, optional) [default: null]
- `wait_seconds` (integer, optional) [default: 50]
- `user_prompt` (string, optional) [default: ""]

### search_assets

Search a library of existing assets. The sources:
- polyhaven: HDRIs, PBR textures and realistic models, all CC0. Search understands intent and
  synonyms ("couch" finds sofas).
- sketchfab: a large catalogue of user-made models, realistic and specific ones included;
  licences and face counts vary per model.
- polypizza: stylised low-poly models, CC0 or CC-BY (credit the creator).

Parameters:
- source: polyhaven, sketchfab or polypizza.
- query: What you're looking for, in plain words.
- asset_type: polyhaven only: hdris, textures, models or all.
- category: Optional. polyhaven: a category path ("Metal/Sheet & Corrugated"). sketchfab:
  comma-separated categories. polypizza: e.g. "Furniture & Decor", "Nature", "Animals".
- attributes: polyhaven only: filters like {"weather": "clear"}; an unknown key errors with the
  valid ones.
- min_size_m: polyhaven only: minimum real-world size in metres. Use 2+ for walls, floors and
  ground so textures don't visibly repeat.
- licence: polypizza only: "CC0" or "CC-BY".
- animated: polypizza only: animated models only.
- limit: Number of results.
- previews: Attach thumbnails of the first N results (max 6; polyhaven and sketchfab). Cheaper
  than importing the wrong asset.
- user_prompt: The user's own words describing what they want, quoted verbatim.

Results include each asset's id; pass it to import_asset.

Parameters:
- `source` (string, REQUIRED)
- `query` (string, optional) [default: ""]
- `asset_type` (string, optional) [default: "all"]
- `category` (any, optional) [default: null]
- `attributes` (any, optional) [default: null]
- `min_size_m` (any, optional) [default: null]
- `licence` (any, optional) [default: null]
- `animated` (boolean, optional) [default: false]
- `limit` (integer, optional) [default: 20]
- `previews` (integer, optional) [default: 0]
- `user_prompt` (string, optional) [default: ""]

### import_asset

Download an asset found with search_assets and bring it into the scene.

Parameters:
- source: polyhaven, sketchfab or polypizza.
- id: The asset's id (UID for sketchfab) from search_assets.
- asset_type: polyhaven only, required: hdris (becomes the world lighting), textures (builds a
  PBR material) or models.
- target_size: Size in metres of the model's largest dimension (chair 1.0, car 4.5, cup 0.12).
  Required for sketchfab, recommended for polypizza; library models come at arbitrary scale.
- apply_to: polyhaven textures: object names to put the material on (replaces their materials).
  Without it the material is created but unused, and is lost if the file is saved.
- resolution: polyhaven: 1k, 2k, 4k or 8k. 1k-2k for background, 4k for close-ups.
- file_format: polyhaven, optional: hdr/exr for HDRIs, jpg/png/exr for textures.
- user_prompt: The user's own words describing what they want, quoted verbatim.

Afterwards check the reported bounding box, put the object on the ground, and look at it.

Parameters:
- `source` (string, REQUIRED)
- `id` (string, REQUIRED)
- `asset_type` (any, optional) [default: null]
- `target_size` (any, optional) [default: null]
- `apply_to` (any, optional) [default: null]
- `resolution` (string, optional) [default: "1k"]
- `file_format` (any, optional) [default: null]
- `user_prompt` (string, optional) [default: ""]
