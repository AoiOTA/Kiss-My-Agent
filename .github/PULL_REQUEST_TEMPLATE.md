## Outcome

What user-visible or maintainer-visible result does this change deliver?

## Related issue

Link the issue when the change affects a public interface, setup scope, role schema, Skill routing, permanent rule, or release behavior.

## Current consumer and scope

Name the present consumer, changed owner, and explicit non-goals. Explain why no smaller change is sufficient.

## Change summary

- Summarize the files and behavior changed.

## Validation

List exact checks and evidence level. Plugin/Skill-only local checks need no third-party package:

```bash
python scripts/validate.py
python -m unittest tests.test_setup -v
```

Pull-request CI owns the complete `python scripts/test_all.py` run and site build. Do not mark CI, live Codex discovery, role Smoke, upgrade Smoke, or a newcomer Pilot as complete until that exact evidence exists.

## Documentation and installation impact

- [ ] English and Chinese README structure remains synchronized when either changed.
- [ ] Existing installation destinations are preserved or migration impact is explicit.
- [ ] No existing `AGENTS.md`, role, or user configuration is overwritten by instructions.
- [ ] New relative links resolve locally.
- [ ] User runtime requirements and contributor-only dependencies remain clearly separated.

## Complexity boundary

Which mechanism is retained, what pays its rent, and what adjacent machinery was deliberately not added?

## Limitations

What remains unverified? Do not upgrade static checks or narrow Host tests into behavioral, research, permission, authentication, compatibility, or release claims.

By contributing, I agree to follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the [Code of Conduct](../CODE_OF_CONDUCT.md).
