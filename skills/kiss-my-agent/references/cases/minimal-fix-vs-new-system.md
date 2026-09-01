# Minimal fix vs new system

## Goal
Correct a narrow parsing defect at the component that owns the parser.

## Consumer
The one current command that consumes the parsed value.

## Minimum mechanism to retain
A local validation and direct error at the parser boundary, plus the focused regression example.

## Mechanism to reject
A shared schema registry, migration framework, compatibility daemon, and promotion workflow built for hypothetical future parsers.

## Deletion counterfactual
If deleting the shared system leaves the command correct and the regression detectable, the system is not required.

## Legitimate exception
Introduce a shared contract only when another current producer or consumer must independently exchange the value, or when incompatible parsing has a concrete high-consequence impact.
