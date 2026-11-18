---
name: fastapi-practices
description: Apply version-matched FastAPI and Pydantic implementation patterns when building or revising FastAPI routes, dependencies, request/response models, and API error handling. Use only for FastAPI code, not generic Python or architecture discussions.
disable-model-invocation: false
---

# FastAPI Practices

## Job and limits
Make a bounded FastAPI change fit the project's version, public contract, and runtime behavior. Use this during actual FastAPI route, dependency, and schema implementation/review. Do not install packages, change framework versions, move files, or replace the project's chosen ORM/environment solely because an upstream example prefers another tool. Applicable project instructions and existing working conventions take precedence.

## Procedure
1. Inspect the installed/version-pinned FastAPI and Pydantic versions, nearby endpoints, models, tests, OpenAPI generation, and actual run commands. Consult [FastAPI's official skill](https://github.com/fastapi/fastapi/blob/master/fastapi/.agents/skills/fastapi/SKILL.md) or version-matched docs only for patterns relevant to this change. If unavailable, mark version-sensitive assumptions.
2. Define explicit input and output models; separate request fields from internal records and returned fields. Use response validation/serialization that avoids exposing secrets or cross-user data. Keep intentional status codes, including validation and conflict responses, stable.
3. Prefer modern typed parameter/dependency declarations supported by the project's version. Reuse authentication/database dependencies; do not duplicate policy logic in each route. Keep authorization on server-side operations, not just frontend controls.
4. Choose sync or async handlers based on the actual called libraries. Do not block the event loop with synchronous I/O inside an async handler. Manage database transactions and resource cleanup at a clear owner; avoid check-then-write races for revisions or ownership.
5. Inspect the resulting OpenAPI contract and affected callers when modifying externally consumed endpoints. For app/agent clients sharing operations, preserve the same backend rules and predictable error semantics.
6. Execute the smallest relevant tests or runtime checks permitted by the task; add focused checks for newly consequential behavior and report commands, results, and unverified paths. Do not claim a contract or deployment works because types compile.

## Stop condition
The changed endpoint follows the existing project and version's patterns, its relevant data/security boundaries and contract are accounted for, and concrete checks or limits are reported. No blanket refactor, arbitrary test quota, or infrastructure setup.

## Sources and evidence
Based on [FastAPI's official skill](https://github.com/fastapi/fastapi/blob/master/fastapi/.agents/skills/fastapi/SKILL.md). The 2026 SWE-Skills-Bench reported positive average results for a FastAPI skill in its tested configurations; that is not a guarantee for this adapted text or another agent.
