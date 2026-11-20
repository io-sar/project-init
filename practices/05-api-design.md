---
group: API design
id: "05"
version: 0.4
reviewed: 2026-11-17
---

# 05 · API design

APIs are promises to other people's code. Breaking them is expensive; designing them well is cheap.

## 05.1 Contract first
- applies: interfaces has-any (internal-api, public-api, events)
- rule: Define the contract before implementing: OpenAPI for REST, AsyncAPI for events, .proto for gRPC. The contract lives in the repo and is validated in CI.
- why: Consumers can start in parallel and changes are visible in review.

## 05.2 Consistent resource design
- applies: interfaces has-any (internal-api, public-api)
- rule: Use plural nouns for resources, the correct HTTP methods (GET is safe, PUT/DELETE are idempotent) and correct status codes.
- why: Predictable APIs need less documentation and produce fewer integration bugs.

## 05.3 Standard error format
- applies: interfaces has-any (internal-api, public-api)
- rule: Return errors in the RFC 9457 Problem Details format (type, title, status, detail). Never return stack traces.
- why: Clients handle errors uniformly; internals are not leaked.

## 05.4 Versioning strategy
- applies: interfaces has public-api
- rule: Choose and document the versioning strategy before the first release (e.g. `/v1/` in the path).
- why: Retrofitting versioning after clients exist is painful.

## 05.5 Pagination, filtering, sorting
- applies: interfaces has-any (internal-api, public-api)
- rule: Every list endpoint is paginated (cursor-based for large or changing sets) with a maximum page size.
- why: Unbounded lists eventually take down the service or the client.

## 05.6 Idempotency for unsafe operations
- applies: interfaces has-any (internal-api, public-api) AND stage>=mvp
- rule: Accept an `Idempotency-Key` header on POST operations that create or charge something; repeat requests return the original result.
- why: Network retries must never create duplicate orders or payments.

## 05.7 Rate limiting
- applies: interfaces has public-api
- rule: Apply rate limits and quotas per client and return 429 with `Retry-After`.
- why: Protects availability and cost from abuse and from buggy clients.

## 05.8 Compatibility and deprecation
- applies: interfaces has public-api
- rule: Only additive changes within a version. Announce deprecations with a date and a `Deprecation`/`Sunset` header.
- why: Clients get time to migrate; trust in the API is kept.

## 05.9 Validate input, protect output
- applies: interfaces has-any (internal-api, public-api)
- rule: Validate every input against the schema at the edge; never expose internal IDs, fields or errors beyond the contract.
- why: Most injection and data-leak bugs start at an unvalidated boundary.

## 05.10 CRUD semantics
- applies: interfaces has-any (internal-api, public-api)
- rule: Create with POST returning `201 Created` and a `Location` header; read with GET; replace with PUT (full resource) and change part with PATCH; delete with DELETE returning `204 No Content`. Use separate API models (DTOs) from database entities so the schema never leaks into the contract. Support conditional updates (`ETag` / `If-Match`) where concurrent edits are possible (see 06.9).
- why: Predictable semantics let clients and tools work without special cases; DTOs let the database evolve without breaking clients.
