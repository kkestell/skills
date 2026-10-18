---
name: kdiscuss
description: Refine a plan, argument, or idea through a bounded discussion with another agent. Use for challenging assumptions and resolving design questions, not implementation or code review. Never use it unless the user invokes it or explicitly asks for it, or a skill the user invoked runs it.
argument-hint: "<claude|codex|opencode> <topic or artifact path>"
---

Use this skill only when the user invokes it or explicitly asks for it, or when a skill the user invoked runs it. Never use it on your own initiative.

## Objective

Develop a stronger proposal with another agent. Finish with agreed improvements and an honest account of anything still unsettled.

## Establish the work

1. Read `<discussion> $ARGUMENTS </discussion>`. The first argument selects `claude`, `codex`, or `opencode`; the rest names the topic or artifact. If either is missing or the agent is unsupported, ask for the missing information and stop.
2. Read the named artifact and the evidence needed to judge it. For a code plan, inspect the relevant code and tests. Establish the goal, constraints, current proposal, and questions that could change the outcome. Do not invent requirements to fill a gap.
3. Use the selected agent through this skill's `scripts/discuss.py`. It selects Claude Code with Fable and high effort, Codex with GPT-6.1 Sol and high effort, or OpenCode with DeepSeek V4.1 Flash from the DeepSeek provider and max effort. If the CLI, authentication, or model is unavailable, report the blocker; do not substitute another agent or model.

## Open the discussion

4. Read this skill's `references/discussion-rules.md` and follow it yourself. Write an opening message containing the goal, constraints, proposal, evidence, your initial assessment, and the most consequential uncertainties. The peer runs in the same workspace with read-only access, so point it at the relevant files, commits, and commands rather than pasting every fact, and quote only what it cannot read itself. Give the peer enough context to assess the proposal independently. The helper includes the discussion rules in the first message.
5. Create a temporary directory for the session state and message files. From the workspace root, send the opening message with the command below, replacing the script path with its absolute installed location. Keep the returned state path for every subsequent turn.

   ```bash
   python3 /path/to/kdiscuss/scripts/discuss.py --agent claude --state "$discussion_dir/session.json" < "$discussion_dir/opening.md"
   ```

   Use the selected agent in place of `claude`. The helper sends one message per call and prints the peer's reply. It preserves the peer's session and stops after six replies. Do not use a latest-session shortcut, fork the conversation, or start another session to evade the limit.

## Discuss

6. Evaluate each reply against the goal and available evidence. Check consequential factual claims yourself. Accept useful corrections, explain why an objection does not apply, or propose a concrete alternative. Supply any evidence the peer cannot inspect itself. Do not merely relay messages or treat the peer's confidence as proof.
7. Keep each response focused on what remains unsettled and how the proposal should change. Use the same session for the response:

   ```bash
   python3 /path/to/kdiscuss/scripts/discuss.py --state "$discussion_dir/session.json" < "$discussion_dir/response.md"
   ```

8. When the substantive issues appear resolved, send the complete revised proposal for confirmation, including accepted trade-offs and any remaining uncertainty. Reserve a reply for this confirmation. Count agreement only when both agents endorse that same proposal and neither has an unanswered material objection. If confirmation introduces a new concern, address it within the remaining turns.
9. Stop when the proposal is confirmed, six peer replies have been received, or another exchange would repeat the same arguments without new evidence. Preserve a useful disagreement: state the competing positions and the evidence or user decision that would settle it. If the helper fails, stop and report the incomplete discussion; do not restart or retry a turn whose delivery is uncertain.

## Finish

10. For a supplied plan, incorporate the agreed refinements in place, preserving its format and scope. Leave disputed changes out and report them. For another artifact, edit it only when requested; otherwise present the refined proposal in the final response. Do not implement the plan or commit unless the user asks.
11. End with a summary of the exchange in two parts:
    - **Overview.** Summarize what was discussed, what changed in the proposal, what was settled, and what remains unresolved. Name the other agent and distinguish confirmed agreement from a discussion that stopped early. Link any updated artifact.
    - **Messages.** List every message in order, numbered and labeled with its sender, and summarize each in a sentence or two. Use the `messages` recorded in the session state file. Leave out the discussion rules the helper prepends to the opening message and the turn counters it appends.

    Leave out the full transcript and execution details unless the user asks for them.
