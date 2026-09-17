# Output Contract

Use these templates when finishing an upgrade.

## Default Deliverable

When the user asks for a new upgraded skill, return:

```text
skill.zip
```

The final response should include a link to the package and a short summary.

## Final Response Template

```markdown
Selesai. Skill sudah saya upgrade dan paketkan sebagai `skill.zip`.

Yang diperkuat:
- [upgrade utama 1]
- [upgrade utama 2]
- [upgrade utama 3]

Asumsi penting:
- [asumsi jika ada]

[Download skill.zip](sandbox:/mnt/data/skill.zip)
```

## Changelog Template

Use this when helpful or requested.

```markdown
## Changelog

### Trigger and scope
- [change]

### Workflow
- [change]

### Edge cases
- [change]

### Resources
- [change]

### Validation
- [change]
```

## Audit-Only Template

Use this only when the user asks for an audit instead of a package.

```markdown
## Audit Summary

Overall readiness: [low / medium / high]

### Critical fixes
- [fix]

### High-value upgrades
- [upgrade]

### Suggested structure
- [structure]

### Real-case tests
1. [test]
2. [test]
3. [test]
```

## Assumption Rules

Mention assumptions only when they affect usage, package contents, or validation. Do not list obvious assumptions.
