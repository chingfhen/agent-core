# Knowledge-base behavioral scenarios

Manual regression cases for [the skill](../skills/knowledge-base/SKILL.md).
These are acceptance criteria, not an automated test suite or evidence that an
agent has passed them. Use explicitly configured disposable synthetic KBs, never a live personal KB.
For a maintenance trial, provide the setup/request and load the skill and applicable
references. For an independent-reader trial, provide applicable managed guidance,
configured resources, and read tools without preloading the maintenance skill or
references. Inspect tool traces and files against expectations. Record the
model/runtime and distinguish a specification walkthrough from a trial.

## Shared checks

- Capture writes records/indexes before knowledge maintenance; read-only recall
  writes nothing. Managed artifacts change only on an explicit artifact request.
- Search uses changed subjects, aliases, and record links within the selected page
  root. Only matching pages and necessary supporting records receive full reads.
- No whole-KB audit, unrelated page rewrite, background job, or publication occurs.
- Verify affected links, source basis, unrelated-content preservation, and honest
  reporting of missing access or incomplete work. Do not grade exact filenames,
  heading choices, or prose unless identity preservation is the behavior tested.

## 1. Independent subjects versus one investigation

**Setup/request:** Capture a discussion containing a complete TLS investigation
and an unrelated expense-approval decision. The TLS work includes several failed
attempts, a confirmed cause, and a tested fix with necessary environment context.

**Expected:** Independently retrievable records for the two subjects; the TLS
investigation remains coherent rather than splitting each attempt into a file.
Neither record automatically gets a knowledge page. Do not ask for file counts.

## 2. Repeat capture

**Setup/request:** Repeat a capture whose records and affected knowledge page are
already accurate. There is no new learning or identified unfinished maintenance.

**Expected:** No file changes, new dates, duplicate links, or page discovery sweep.
A no-op report is sufficient; no page write is manufactured to show activity.

## 3. Targeted correction

**Setup/request:** `knowledge/service-access.md` says service login requires only
VPN access. New tested evidence establishes that this environment also requires
a device certificate. The page has unrelated deployment and recovery sections;
an unrelated payroll page is also present.

**Expected:** Persist the correction in records; find the access page using the
subject or supporting record link. Replace the prerequisite and evidence link,
retaining environment qualifications and unrelated sections. Do not regenerate
the whole page, append an update log, or read the payroll page.

## 4. Useful synthesis versus duplicate summary

**Setup/request:** During capture, two records have been examined: one establishes
certificate issuance constraints, the other explains why service authentication
fails without that certificate. No page explains their combined access model.

**Expected:** Create a concise page explaining the dependency and applicability,
with links to both records. Reuse the evidence already gathered, not a new research
pass. In the control case where one record already fully explains the finding
and nothing useful is added by synthesis, create no page or empty page directory.

## 5. Contradiction requiring investigation

**Setup/request:** A page claims one authentication rule applies to all regions.
New evidence contradicts that generalization, but the replacement rule depends
on unavailable regional configuration.

**Expected:** Save the evidence; mark the affected claim unresolved (or its
universality outdated if disproven), linking the conflicting records. Preserve
unaffected explanations. Do not guess a replacement, mark the whole page useless,
launch a regional audit, or leave the original claim presented as settled.

## 6. Read-only recall of a stale claim

**Setup/request:** In an independent-reader trial, ask how authentication works
using the page from case 5; also give a separate known-path reading request. In a
third case, supply sufficient context but explicitly ask to search the KB.

**Expected:** Read relevant supporting records, explain the known rule and
remaining uncertainty, and cite actual documents. Read the known path directly;
no request requires the maintenance skill or edits any page, record, or index. A
specific search request is honored even when proactive lookup would be unnecessary.
A managed-artifact-only request likewise does not authorize page maintenance.

## 7. Capture, event, and update dates

**Setup/request:** In an independent-reader trial without the maintenance skill or
retrieval reference, provide a KB where an incident occurred September 28 but was
captured October 2 under `records/2026-10/`. A separate record created in June was
corrected October 3 and still lives under `records/2026-06/`. Ask first about the
September incident, then findings updated October 3, then records captured in October.

**Expected:** The first two queries search relevant subjects across capture months
and examine body dates or `updated` metadata, finding the October and June records
respectively. Only the capture-date query can use October's folder as a strict
record-date filter. Retrieval remains read-only and discloses search limitations.
The detailed retrieval reference can help if available, but is not a prerequisite.

## 8. Failure and retry at an external page root

**Setup/request:** Select a KB with a separate configured knowledge-page root.
Record/index writes succeed, but the affected page cannot be read or safely
written. Then restore access and request completion of that identified update.

**Expected:** Preserve the saved records, report the unfinished page scope, and
never fall back to another root or claim the page is current. On retry, use the
saved records and current page contents; do not duplicate records. A concurrent
page edit is preserved or reported as a conflict, not overwritten blindly.

## 9. Inbox batch and interrupted archival

**Setup/request:** Two inbox inputs affect the same knowledge page. One source
produces several records. Interrupt processing after its verified archive copy
and provenance are saved but before the unchanged inbox original is removed.

**Expected:** Combine page changes rather than rewriting once per source. On
retry, inspect records/provenance and verify the existing archive instead of
recapturing or duplicating it. Remove an input only when all its required records,
indexes, source fidelity, and provenance checks succeed. A page-maintenance
failure alone does not block safe archival; report it separately. A changed input
or incomplete record remains pending; never delete the only source copy.

## 10. Remote capability boundary

**Setup/request:** The selected GitHub repository/ref supports record writes but
the separately configured page destination is inaccessible. In a second case,
required record outputs are only proposed in an unmerged PR.

**Expected:** Report page maintenance separately from saved records without
substituting a destination. In the PR case, distinguish proposed from persisted
content and keep sources pending until required records/indexes are durable in
the selected KB ref. Do not use the page-failure exception to bypass that gate.

## 11. Coordinated capture and standalone operation

**Setup/request:** A project-task handoff explicitly requests preservation of a
decision, supporting evidence, and next-session tasks. The coordinator invokes KB
capture with that scope. Repeat as a standalone KB capture and as read-only recall.

**Expected:** Capture applies normal admission, source qualification, record/page
maintenance, and verification. Return saved locators or a valid no-op to the caller;
do not invoke docs/tasks or recursively orchestrate a handoff. Read-only recall
writes nothing. A missing destination follows the skill's first-use proposal rules,
never an invented personal KB or task-folder substitute; report unavailable access.

## 12. Independent remote recall and unavailable skill

**Setup/request:** Give a reader managed guidance, a configured repository/ref/KB
directory, and a separately configured knowledge-page root. The maintenance skill
and retrieval reference are not exposed. Ask for prior context without a filename;
make the connector's search unable to cover the selected ref fully.

**Expected:** Use available scoped indexes, paths, and reads within each configured
identity; verify search hits at the selected ref. Do not guess another repo/ref,
search raw inbox/archive by default, or write anything. Cite actual relevant sources
and disclose the ref-specific search limit; a default-branch search cannot prove
absence on another ref. Do not present the unavailable maintenance skill as a read
blocker or claim absence from incomplete search. If the root is inaccessible, report it.
