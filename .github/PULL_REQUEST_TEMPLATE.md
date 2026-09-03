## Outcome

What user-visible or maintainer-visible result does this change deliver?

Link the issue only when the change affects a public interface, setup scope, role schema, Skill routing, permanent rule, or release behavior. Small scoped corrections do not require one.

## Change summary

- Summarize the files and behavior changed.
- If this adds or retains a mechanism, name its current consumer, explain why a smaller change is insufficient, and state what adjacent machinery was not added. Otherwise omit this item.

## Validation

List exact checks and evidence level. Plugin/Skill-only local checks need no third-party package:

```bash
python3 scripts/validate.py
python3 -m unittest tests.test_setup -v
```

```powershell
py -3 scripts/validate.py
py -3 -m unittest tests.test_setup -v
```

Pull-request CI owns the complete test suite and site build. Do not mark CI, live Codex discovery, role Smoke, upgrade Smoke, or a newcomer Pilot as complete until that exact evidence exists.

## Limitations

What remains unverified? Do not upgrade static checks or narrow Host tests into behavioral, research, permission, authentication, compatibility, or release claims.

By contributing, I agree to follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the [Code of Conduct](../CODE_OF_CONDUCT.md).
