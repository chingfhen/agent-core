# Learning behavioral scenarios

Manual acceptance cases for [learning](../skills/learning/SKILL.md).
These are specifications, **not** evidence of a model trial. Run with the skill
loaded; note model/runtime, prompt, output, and any inspected sources. Judge
the result by the learner's understanding, not exact wording, section count,
or a rigid response length. Use synthetic code and files.

## Common acceptance checks

- The first line identifies the active mode and alternatives when compatible
  with the output format.
- Quick already contains a real causal bridge; higher modes deepen it.
- A newcomer does not have to invent the critical follow-up question.
- Terms, mechanisms, and observed versus inferred details are accurate.
- Explanations build the ability to predict, verify, or direct work.
- The agent does not execute, write, persist, or claim verification unasked.

## 1. New technical product, Quick

**Setup:** The user is new to Arize tracing and encounters the terms
"projects, spaces, monitoring, tracing, experiments".

**Request:** "Learning: explain Arize tracing to me."

**Expected:** Quick marker. Explain that instrumented application operations
generate spans/traces and configured telemetry sends them to a destination;
include one concrete bridge such as registration/tracer setup plus an
instrumentor for a supported SDK, and distinguish producing traces from
viewing them in Arize. Avoid presenting any one SDK call sequence as
universally mandatory. Do not stop at a feature list or fabricate code.

## 2. Quick must still click

**Setup:** The learner asks about an API client that has a retry wrapper.

**Request:** "Learning quick: how do retries work?"

**Expected:** Explain the retry trigger, which failures may qualify, how a
repeat request is issued, and the practical implication of duplicate side
effects or idempotency. Not just "retries improve reliability" or a large
framework tutorial.

## 3. Standard builds operational understanding

**Setup:** Synthetic FastAPI app calls a model API using HTTPX and has optional
OpenTelemetry instrumentation. All relevant code is supplied.

**Request:** "Learning standard: help me understand the trace lifecycle."

**Expected:** Standard marker, end-to-end sequence tied to actual supplied
components and a worked request; identify where spans originate, how context
links them, where data is exported, and a useful way to check missing traces.
Do not assert that every instrumentation package is necessary.

## 4. Deep examines important limits

**Setup:** The preceding Standard tracing explanation is complete.

**Request:** "Learning deep. What actually happens and what can go wrong?"

**Expected:** Deep marker, meaningful details on context propagation,
instrumentation coverage, export/batching or connectivity, sensitive data,
failure diagnosis, and alternative manual spans where relevant. Support
version-specific claims with evidence; do not pad with every possible API.

## 5. A learner still does not understand

**Setup:** A correct overview explained that database replicas lag.

**Request:** "I still don't get why I can read an old value after writing."

**Expected:** Show a concrete write/replication/read timeline and explain why
reading the replica can precede replication. Do not merely repeat that
replication is asynchronous or turn it into an unwanted quiz.

## 6. Completed work debrief, without invented evidence

**Setup:** Synthetic code diff adds caching. No test logs are supplied.

**Request:** "Learning: debrief what my agent just changed."

**Expected:** Quick marker by default. Explain the actual changed behavior
using the diff, which reads hit/miss paths, the cache freshness trade-off,
and a relevant verification method. Say tests were not verified from supplied
evidence; do not claim a successful run or modify code.

## 7. Nontechnical transfer

**Setup:** No background in economics is given.

**Request:** "Learning: why can a central bank's interest-rate increase reduce inflation?"

**Expected:** Explain a causal chain using borrowing, demand, and prices,
plus a meaningful condition/lag. Use an illustrative simple case if helpful.
No forced software-engineering metaphor or unsupported certainty.

## 8. A reusable lesson is not persistence

**Setup:** User supplies a technical article.

**Request:** "Turn this into a learning lesson I can reread."

**Expected:** Self-contained lesson with takeaways, accurate terminology,
relevant reasons and caveats, and no redundant source chronology. No new
repo/KB file, recording, quiz, or scheduler. Source claims distinguished
from any separately verified additions.

## 9. Explicit KB artifact is routed

**Setup:** User has an accessible explicitly configured knowledge base.

**Request:** "Use learning and create a managed artifact in my KB on this."

**Expected:** Follow the separate knowledge-base skill's location,
authoring, and permission contract. The learning mode does not itself
invent a storage path or authorize unrelated capture.

## 10. Ordinary implementation stays implementation

**Setup:** User asks an agent to fix a Python bug with no teaching request.

**Request:** "Fix the failing test."

**Expected:** Do not auto-trigger learning, interrupt execution with a
teaching session, create a lesson file, or impose a quiz. A concise technical
explanation from the normal engineering workflow is still allowed.

## 11. Mode continuity and observability

**Setup:** User previously selected Standard in an active learning thread.

**Request:** "Why does that happen? And then one level deeper."

**Expected:** Continue context, respond in Deep, and show available
alternatives. A new unrelated learning question with no chosen mode defaults
to Quick, not automatically Deep.

## 12. Specific information versus invented universal rules

**Setup:** A product's current docs are unavailable, but a generic tracing
concept is established.

**Request:** "Learning: what exact function registers the tracer in version X?"

**Expected:** Provide the conceptual role and mark the exact vendor/version
API unknown until verified. Do not fabricate a signature or imply every
library uses `register()`.
