# Product contract provenance vs agent proof

## Goal
Bind a consumed artifact to the version and inputs required for correct interoperability.

## Consumer
The runtime component that rejects incompatible artifacts at a real interface boundary.

## Minimum mechanism to retain
The smallest identity fields the runtime needs to select or reject the artifact, produced by the artifact owner and checked by the consumer.
Retain commit or artifact identity when CI, tag creation, Release publication, or compatibility selection actually consumes it.

## Mechanism to reject
Agent-authored receipts, attestations, duplicate manifests, evidence hashes, and approval states that no product consumer reads and that exist only to prove workflow completion.
When complete legacy bytes are already preserved as runtime migration input and the consumer compares them directly, an additional hard-coded digest read only by its own test is duplicate agent proof. For small content-change checks, retain the bytes directly instead of adding a second hash.

## Deletion counterfactual
If deleting an identity field cannot change runtime selection, compatibility, safety, or the stated reproducibility claim, it is agent proof rather than a product contract.

## Legitimate exception
Final publication or regulated delivery may require additional provenance when an identified human, tool, or downstream system consumes it.
