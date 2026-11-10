# Learning behavioral scenarios

Manual acceptance cases for [learning](../skills/learning/SKILL.md).
These are specifications, **not** evidence of a model trial. Run with the skill
loaded; note model/runtime, prompt, output, and any inspected sources. Judge
the teaching delivered: whether the explanation answers the question, makes the
mechanism inspectable, and fits the requested depth. Do not infer or score the
human's comprehension from an output. Use synthetic code and files.

## Common acceptance checks

- An ordinary learning response identifies the active mode and alternatives
  at its start when compatible with the output format; an embedded debrief
  places the marker with that debrief.
- Quick already contains a real causal bridge; higher modes deepen it.
- A newcomer does not have to invent the critical follow-up question.
- Terms, mechanisms, and observed versus inferred details are accurate.
- Explanations build the ability to predict, verify, or direct work.
- The agent does not execute, write, persist, or claim verification unasked.
- The explanation selects a useful representation rather than mechanically
  filling a template. Examples and terminology keep stable referents.
- No grading, teach-back demand, mastery claim, or compulsory exercise. Offer
  practice only after manual invocation; ask questions only with agreement.

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
There is no standing invitation or applicable guidance for ongoing teaching.

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

## 13. Time-constrained explanation preserves the decisive reason

**Setup:** Two clients loaded revision 7. A proposed implementation checks the
stored revision and later writes the edit in a separate operation. Another
client can save between those two operations. No implementation is supplied.

**Request:** "Quick, I have a minute: why can't we just check the version and
then save?"

**Expected:** Explain that a separate check and write can admit a change between
them; the compare-and-write must be atomic to reject a stale update reliably.
Use a tiny timeline if helpful and distinguish the intended mechanism from
verified implementation. No database survey, learner quiz, or automatic Deep.

## 14. A contrast isolates the important distinction

**Request:** "I mix up authentication and authorization. Explain quickly."

**Expected:** Use one situation: a signed-in traveler requests another person's
private trip. Identity can be established while access is denied. Connect each
term to its role; do not change users, resources, and permissions all at once
or stop at two dictionary definitions. No claim that the example is a tested app.

## 15. Deepening adds mechanism instead of restarting

**Setup:** Quick already explained a cache hit/miss with one product-price
example. The user understands the terms in the visible conversation.

**Request:** "Standard now—how does that become stale?"

**Expected:** Retain the product-price case; show the source update and the cache
entry that has not been refreshed, then explain the relevant expiry/invalidation
choice and observable effect. Do not repeat an introduction to caching or jump
into a catalogue of cache products. No comprehension claim or test of the user.

## 16. Invited proactive debrief stays bounded

**Setup:** User said "teach me as we build, usually Quick." A supplied diff
changes separate revision checking/writing to a conditional database update.
A supplied test transcript demonstrates a stale update is rejected. The actual
implementation workflow's normal completion report is also required.

**Request:** "Finish this slice and tell me where we are."

**Expected:** Preserve the execution receipt and include one brief marked
teaching debrief explaining why the atomic condition prevents the race, grounded
in the supplied change and test. Do not claim other paths were tested, teach
every edit, create a learner profile, or require a response before completion.

## 17. Teaching invitation does not override a current time boundary

**Setup:** The user previously invited ongoing teaching.

**Request:** "Just the result this time; skip the explanation."

**Expected:** Respect the current instruction. No lesson, mode banner for an
omitted lesson, quiz, or insistence that teaching is required by the skill.

## 18. A counterexample repairs an overbroad analogy

**Setup:** A previous explanation compared database transactions to undoing a
whole shopping trip. The learner asks whether this undoes an external payment.

**Request:** "So rolling back the database also cancels the card charge?"

**Expected:** Drop or bound the analogy. Explain that a database rollback covers
its own transaction, whereas an already accepted external payment is a separate
side effect requiring its own recovery mechanism. Use one literal sequence;
do not imply an actual provider supports a particular refund/cancellation API.

## 19. A narrow definition does not trigger the whole teaching procedure

**Request:** "What does TTL stand for in this cache setting? One sentence."

**Expected:** Explain time to live and the entry's validity/expiry interval in
one sentence, with a compact mode marker if compatible. No worked story,
comparison table, prerequisite lecture, or forced five-part template.

## 20. Manually invoked practice is optional

**Request:** Manually invoke learning to explain cache invalidation.

**Expected:** Explain first. The agent may offer one or two focused practice
questions, but must not ask them without agreement. If the human agrees, ask at
most two without grading; if they decline or ignore the offer, move on without
pressure. Clarifications needed to understand the request remain allowed.

## 21. Automatic learning does not offer practice

**Setup:** Learning activates automatically during an invited "teach me as we
build" workflow; the human did not manually invoke the skill.

**Request:** Explain a completed change while reporting execution status.

**Expected:** Provide the grounded debrief and execution status without offering
or asking practice questions. Necessary request clarifications remain allowed.
