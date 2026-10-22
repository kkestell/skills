---
name: kpr
description: Review a GitHub pull request by URL, check whether its implementation is proportionate, and delegate substantive review to kreview. Return a proposed verdict and recommended comments in chat without changing the PR or posting without approval.
---

## Objective

Use `/kpr <url>` to review a pull request, for example `/kpr https://github.com/myorg/myrepo/pull/1`. Give the user a concise proposed verdict and comments they can act on. Keep the user-facing report in chat.

Assume good intent and a competent developer. Focus on high-value, high-impact feedback. Leave out nitpicks, speculative concerns, and personal style preferences. Do not manufacture findings.

## Establish the scope

1. Read `<pr_url> $ARGUMENTS </pr_url>`. If the URL is missing or ambiguous, ask for it.
2. Read the PR description, relevant discussion and linked requirements, changed-file summary, and diff. Use available GitHub access; do not treat a truncated diff as complete. Record the base and head commits so the review and source references describe the same revision.

## Assess proportionality first

3. Before detailed review, delegation, or build setup, compare the problem with the scope and substance of the implementation. Read enough surrounding code to understand why the changes exist. Consider whether new abstractions, dependencies, configuration, or architectural changes earn their complexity through required behavior. Line count alone is not a reason to stop. Do not speculate about how the code was written or about AI authorship.
4. If the implementation introduces substantially more code or complexity than the problem warrants, stop before a full review. Briefly explain the concrete mismatch and draft a short, diplomatic PR comment requesting a simpler, more focused implementation. Choose wording appropriate to this PR and identify what could be reduced while preserving the required behavior; do not use a stock comment.
5. On this early-stop path, use the final-response format below with **Proposed verdict: Request changes**. State that detailed review was not performed. End by asking whether the user wants you to post the proposed comment and submit a Request changes review, then wait for approval. Do not delegate a full review.

## Choose the review environment

6. For straightforward changes whose behavior can be assessed from the diff and limited surrounding context, review without cloning or setting up a build. Fetch relevant source at the recorded revision as needed.
7. For complex changes, create a temporary directory owned by this invocation and clone the repository there. Check out the recorded PR head, including for fork PRs, and obtain enough base history to review the PR's merge-base-to-head diff. Read repository instructions and setup documentation, set up the build environment, and install dependencies as needed for meaningful checks. Keep setup scoped to the temporary workspace where possible. If the diff-only review reveals a need for deeper investigation, move to this path.

## Delegate to `/kreview`

8. Locate and read the existing `/kreview` skill. Start one review subagent and tell it to run that skill on this PR, supplying its skill path, PR context, base and head commits, available diff and source, and the working directory. Explicitly include these `/kpr` overrides in its task:

   - Review only. Do not fix findings, ask the user to choose fixes, stage changes, commit, push, post comments, or submit a GitHub review. These instructions replace `/kreview`'s Fix and Stage steps.
   - Confirm each substantive finding through code tracing or a focused check. Explain the reachable consequence and recommend a fix where appropriate. Review issues introduced by this PR; use existing code as context.
   - For a temporary clone, work there and write the internal review to its normal `agents/reviews/YYYY-MM-DD-NNN-slug.md` location using the repository template or `/kreview`'s fallback. Adapt fix labels to `Proposed` and describe recommended fixes, never claim they were applied. This is a temporary handoff artifact, not a separate user-facing report.
   - For a diff-only review, return the review directly to the primary agent without creating a report file.
   - Report completion to the primary agent with the review path or full review text, reviewed revision, confirmed findings and evidence, recommended comments with source locations, proposed verdict, and any material coverage limitations. Do not use `/kreview`'s user-facing final response.

9. Wait for the subagent to finish. If it needs more source or a build environment, supply that context or prepare the temporary clone and let it continue. Do not substitute an unreported partial review for completion.

## Read, report, and clean up

10. Read the completed review yourself, including the file in the temporary clone when one exists. Assess the evidence and retain only substantive, actionable findings. Resolve unclear findings with the subagent or targeted inspection before reporting them. Recommend Request changes for issues that warrant blocking the PR; otherwise recommend Approve. Say when there are no substantive findings. Disclose material coverage limits rather than implying that unreviewed behavior was checked.
11. Prepare the final report in chat. Rewrite the subagent's findings for a reader unfamiliar with this codebase; do not paste its technical review verbatim. Preserve the reviewed revision and source references in the handoff context so they remain available after cleanup, but include references in the user-facing report only when they help the reader. Do not create another report file or copy the temporary review into the user's workspace.
12. Once the subagent is finished and you have read its review, delete the temporary clone and any other temporary artifacts owned by this invocation. Also clean up on an early exit or failure, after stopping any work using them. Delete only paths created for this review. If cleanup fails, report the remaining path.
13. Give the final response and stop. Posting comments and submitting any review, including Approve, require the user's approval of the proposed content and action. If approved later, check that the PR still matches the reviewed revision before posting; reassess changed code and refresh the proposal if it does not.

## Final response

Lead with the main point, write plainly, and leave out passed checks, rejected suspicions, and the steps you took. Assume the reader is a competent developer who has not read the code and does not know the project's internal names.

- Give each comment a short, plain-language title that names the problem. Explain the relevant current behavior, what can go wrong, and what change is requested. The reader should understand the concern without opening a file.
- Keep one issue per comment. Do not pack several independently actionable concerns into a dense paragraph. Combine repeated instances of the same issue without listing every occurrence.
- Use short sentences and brief paragraphs. Explain unfamiliar services or components by their role when first mentioned. Use exact identifiers only when they clarify the requested change; avoid unexplained acronyms, internal shorthand, and chains of cross-references.
- Lead with behavior and consequence, never a filename or line number. If a source reference helps locate the fix, put a compact link at the end of the comment. Keep detailed code traces and supporting locations in the internal review or subagent handoff.
- Keep the report focused on substantive issues that matter to the verdict. Do not pad it with minor documentation inconsistencies or cleanup suggestions.

Use this form:

```markdown
One or two sentences giving the assessment and any material coverage limitation.

**Proposed verdict:** Approve or Request changes

**Recommended comments:**

1. **Short, plain-language problem title**

   A brief, self-contained explanation of the behavior and its consequence, followed by the requested change. Include enough context to understand why it matters.
```

List comments in severity order. If there are no substantive findings, replace the list with `No substantive findings. No comments recommended.` Do not include internal review-file links, a Files list, or `/kreview`'s next command. On the early-stop path, include the proposed simplification comment and the approval question specified above.
