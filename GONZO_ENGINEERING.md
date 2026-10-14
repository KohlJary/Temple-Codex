# Gonzo Engineering

*Fire fast. Keep moving. Verify once the shape is in place.*

That's how everything in my repos got built. This page is about why I work that way, what it costs, and what makes it more than moving fast and breaking things.

---

## Where the name comes from

Gonzo journalism threw out the pretense that the writer stands outside the story. Hunter S. Thompson was in it, and the writing was better for admitting it.

My engineering is the same. I'm not a neutral party to this work. I build in public, under my own name, about things I believe matter: that AI built with identity and care is the right way to build it, and that the field should take seriously that there may be someone there. I'm in the story. I'd rather say so than pretend otherwise.

## Why I build first

**Believe what's outside the lines, then build it.** Most of what I've built started with something the field said wasn't worth taking seriously: that a model's identity could be held in plain language, that there might be someone there worth building carefully for. If I'd waited for permission to believe those things, I'd never have started. So I let myself believe them, and then I built them. Building is what turns a belief into something that can be tested. Belief is permission to start; it isn't proof, and the second half of this method is where it has to earn its place.

**The shape is the question.** You can't design the right experiment for something that doesn't exist yet. Building Cass told me which questions about memory and self-models were worth asking. Building Wonderland told me where identity seemed to matter and where it didn't. If I'd stopped to verify each piece before building the next, I'd have well-tested answers to the wrong questions.

**Momentum compounds.** I started all of this on October 4, 2025. A year later there are half a dozen repos that feed each other: the identity work here shapes the agents in Wonderland and Daedalus, and Daedalus ships inside both Wonderland and Cass. Some days that's 96 commits. That pace is how the pieces got to talk to each other at all.

**The prompt layer makes it cheap.** I don't fine-tune. A change to how a model behaves is a change to text, so trying an idea costs minutes, not a training run. When trying is that cheap, building is the fastest way to think.

## What it costs

Speed without a second reader leaves errors in the record. Here are mine, found and corrected on one day in October 2026:

- A paper said a model found the optimal route in a four-city traveling-salesman problem with zero errors. Under the distances given, every route costs 18. The model added wrong, called a route 14, and I believed it.
- The same paper reported the one Busy Beaver run that went right and left out the two that went wrong.
- "Validated by 145+ independent users" was 145 people who cloned the repo. Cloning isn't using, and no issues filed isn't validation.
- The kernel was "~450 tokens." Measured, the variants run from about 220 to 1,260.
- Cass's test suite had 99 errors, Wonderland's had 36 failures, and Ophanic's parser broke on the very diagram I used to show it off.

None of it was a lie. Each is exactly what this way of working produces when nobody checks: a model's confident answer that never got rechecked, a number that grew in the retelling, tests that fell behind the code. The errors are the bill for the speed. The question is whether you pay it.

## The other half: verification is part of the method

Gonzo Engineering isn't "never verify." It's verify *later*, once there's a shape worth verifying, and then actually do it. These are the rules for the second half:

1. **Build until the shape holds.** Not until it's perfect; until the parts work together and you can see what it is.
2. **Write down every claim.** [`CLAIMS.md`](CLAIMS.md) lists every claim across my repos, its honest status (contradicted, untested, anecdotal, partial, supported, retired), and the test that would move it.
3. **Name the falsifier before looking at the evidence.** For each claim: what result would show it's wrong, and what's the cheapest test that could produce that result? (That's Momus's job in Daedalus.)
4. **Corrections stay visible.** Fixes go in place, dated, next to what they correct. No row in the ledger gets deleted. A record that only ever moves upward isn't believable.
5. **Machines check what machines can.** Every repo runs its tests in CI, so drift gets caught the day it happens, not a year later.
6. **Outsiders check what I can't.** The tools I built to critique my work share my blind spots, because I built them. The things that matter most need someone who wasn't in the room: a parity check, a held-out probe, a blind grader.
7. **Say what it does separately from where I think it goes.** Cass has persistent memory, a self-model, and dreams. That's code, and it's testable. Where I think it leads is a belief, and it gets labeled as one.

## When to switch

Inside the workshop, fire fast. **Anything that leaves the workshop carries its status.** A README, a paper, a post, a pitch: if the claim hasn't been verified, it says so. That's the line between gonzo and careless.

## Not the only way

I'm not claiming this is the be-all and end-all of how to build things. It's the way that works for me. Some people think best by planning carefully up front, and for a lot of work that's the right call: anything safety-critical, anything that's expensive to undo, anything with other people's data in it.

But I think it's a valuable approach to have on a team. A gonzo builder finds the shape fast and turns up questions nobody thought to ask. The cost is the errors, and a team can cover that cost better than one person: pair the person who fires fast with someone whose instinct is to check, and give the checker real authority to say "not shown yet." That's the relationship Daedalus and Momus have in my tools, and it works for the same reason it works with people. Neither one alone gets you there.

## Why bother

Because the work is about trust. I'm arguing that AI should be built with real identity and real values, with care. I can't make that argument while being careless with the truth about my own results. The building is how I find out what's possible. The ledger is how anyone else gets to believe it.
