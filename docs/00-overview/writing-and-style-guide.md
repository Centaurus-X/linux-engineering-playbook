# Writing and Style Guide

## Language

All documentation should be written in English.

## Structure

Use this structure for technical guides:

```markdown
# Title

## Scope

## Tested Environment

## Prerequisites

## Installation

## Configuration

## Validation

## Troubleshooting

## Rollback

## Security Notes

## References
```

Use only the sections that make sense for the topic, but keep the order stable.

## Command Blocks

Use fenced code blocks with a language tag:

```bash
sudo apt update
```

```python
print("hello")
```

## Safety Notes

Use clear warnings for risky operations:

```markdown
> [!WARNING]
> This operation changes host networking. Test it in a lab before production use.
```

## Style

Prefer:

- One command per line
- Reproducible paths
- Explicit validation commands
- Rollback steps
- Safe defaults

Avoid:

- Hardcoded personal paths
- Unexplained commands
- Mixed German and English
- Global security bypasses
- Long shell one-liners where readability suffers
