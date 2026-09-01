# Verification coordination vs workflow platform

## Goal
Collect one valid result using a shared slow device and a shared output destination.

## Consumer
The decision-maker who needs the result and the single operator responsible for the device and output.

## Minimum mechanism to retain
An explicit operator assignment, isolated output path, stated validity conditions, and direct command or short handoff needed for this collection.

## Mechanism to reject
A persistent queue, campaign database, agent ledger, readiness state machine, promotion service, and dashboard created solely to coordinate one verification.

## Deletion counterfactual
If the result remains collision-free, attributable, and reproducible with a single operator and isolated path, the workflow platform adds no current value.

## Legitimate exception
A durable scheduler or lifecycle system is justified when multiple current independent consumers must safely share the resource over time and a local ownership rule cannot prevent real conflicts.
