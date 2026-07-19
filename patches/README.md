# Patch series

The overlay is split into a numbered patch series. Apply them in order with
`scripts/apply.sh`.

| Patch | Focus | Files |
|-------|-------|-------|
| `0001-computer-use.patch` | CuaDriver integration, computer-use tool, and related tests/fixtures. | `tools/computer_use/*`, `tools/computer_use_tool.py`, `tests/computer_use/*`, `tests/tools/test_computer_use*.py` |
| `0002-agent-context.patch` | Context compaction, message projection, working sets, and related agent tests. | `agent/*`, `tests/agent/*`, `tests/run_agent/test_message_sequence_repair.py` |
| `0003-cli-gateway-tools.patch` | CLI, gateway, TUI, helper tools (`approval.py`, `mcp_tool.py`, `tool_search.py`), and related tests. | `cli.py`, `gateway/*`, `hermes_cli/*`, `tui_gateway/*`, `run_agent.py`, `model_tools.py`, `tools/approval.py`, `tools/mcp_tool.py`, `tools/tool_search.py`, `tests/cli/*`, `tests/gateway/*`, `tests/hermes_cli/*`, `tests/tui_gateway/*`, `tests/tools/test_mcp_tool.py`, `tests/tools/test_tool_search.py` |
| `0004-docs.patch` | Documentation updates. | `website/docs/user-guide/configuration.md` |

To verify the series applies cleanly to the pinned upstream base without
modifying a checkout, run:

```bash
scripts/check.sh /path/to/clean/hermes-agent
```
