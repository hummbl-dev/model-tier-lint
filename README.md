# model-tier-lint

Validate and lint a **model-tier catalog** — a JSON array of
`{model_id, tier, ...}` entries — against structural invariants (required
fields, no duplicate IDs, tiers from a known set).

Generic by design: the known-tier set is a caller override, so it lints any
tier catalog, not a specific vendor's routing table.

## Usage

```bash
python -m model_tier_lint lint catalog.json
```

## License

MIT.
