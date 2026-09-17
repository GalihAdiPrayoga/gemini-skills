# Output Template

Use this template when producing a plugin upgrade plan.

```markdown
# Claude Superpowers Upgrade Plan

## Executive summary
- Current state: [prototype, usable draft, strong candidate, production-ready]
- Biggest risk: [one sentence]
- Highest-impact upgrade: [one sentence]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Capability map
| Capability | Current design | Recommended upgrade | Priority |
|---|---|---|---|
| Commands | ... | ... | Must-have |
| Hooks | ... | ... | Should-have |
| MCP tools | ... | ... | Must-have |
| Subagents | ... | ... | Optional |
| Context files | ... | ... | Must-have |
| Validation | ... | ... | Must-have |

## Real-case workflow matrix
| Feature | Trigger | Input | Steps | Validation | Fallback |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

## Edge-case hardening
| Edge case | Risk | Fix |
|---|---|---|
| ... | ... | ... |

## Security and tool-safety plan
- Read-only tools: [list]
- Local write tools: [list]
- External write tools requiring approval: [list]
- Destructive tools requiring explicit approval and rollback: [list]
- Prompt injection boundaries: [where untrusted content appears]

## Recommended file structure
```text
plugin-name/
├── README.md
├── CLAUDE.md
├── commands/
├── hooks/
├── mcp/
├── subagents/
├── skills/
├── tests/
└── docs/
```

## Implementation roadmap
### Phase 1: Stabilize core
- [ ] Define commands and input/output contracts.
- [ ] Add context file rules.
- [ ] Add validation for main workflow.

### Phase 2: Add real-case depth
- [ ] Add workflow examples.
- [ ] Add edge-case handling.
- [ ] Add fallback behavior.

### Phase 3: Harden and release
- [ ] Add tool permission model.
- [ ] Add prompt injection tests.
- [ ] Add release checklist and docs.

## Release readiness checklist
- [ ] Install instructions
- [ ] Config example
- [ ] Command examples
- [ ] Hook docs
- [ ] MCP permission table
- [ ] Subagent responsibilities
- [ ] Test prompts
- [ ] Failure handling
- [ ] Rollback path
- [ ] Changelog
```

## Prioritization Labels

Use these labels consistently:

- Must-have: required to make the plugin safe or useful in real cases.
- Should-have: important for reliability or scale.
- Optional: useful enhancement but not blocking.
- Avoid: feature should not be implemented as proposed.

## Tone

Be direct and practical. Avoid hype. Prefer concrete implementation notes over motivational language.
