# Degraded safety vs hidden failure

## Goal
Keep a primary service safe when an explicitly optional external enrichment is unavailable.

## Consumer
The primary service and the operator who must distinguish reduced capability from internal failure.

## Minimum mechanism to retain
Catch only the expected availability error at the owner boundary, remove the optional influence, expose the degraded reason, and keep primary safety behavior intact.

## Mechanism to reject
A broad catch that returns an empty success, reuses stale enrichment, silently retries, or converts internal computation defects into degraded operation.

## Deletion counterfactual
If removing the degradation branch makes internal defects visible without reducing correct handling of the known optional outage, the broader branch was hiding failure.

## Legitimate exception
A top-level owner may catch an unexpected failure to perform minimal safe shutdown and cleanup, then preserve failure through rethrow, error result, or nonzero exit.
