# Modes And Outputs

Use this file when you want concrete prompt patterns or response shapes.

## Whole-Paper Prompts

- "Read this PDF and give me a map of the paper first."
- "Explain this paper to me in Chinese, but keep important English terms."
- "I am new to this field. Help me read this paper from top to bottom."

## Whole-Paper Output Shape

Prefer a compact structure like this:

1. one-paragraph thesis of the paper
2. map of the paper by section or page
3. key claims and evidence
4. hard parts the reader should expect
5. suggested next deep-dive questions

## Focused Formula Prompts

- "Explain Equation 4."
- "What problem is this loss function solving?"
- "Explain the symbols first, then derive it."

## Formula Output Shape

1. role of the formula
2. symbol dictionary
3. intuition
4. connection to the method
5. derivation only if needed

## Section Prompts

- "Explain Section 3 in detail."
- "Help me read 4.2 Experimental Setup."
- "I only care about the method section."
- "Explain the introduction of this paper in Chinese."

## Section Output Shape

1. role of this section in the full paper
2. connection to the previous and next parts
3. key ideas in order
4. important formulas, figures, tables, or modules in this section
5. what the reader should focus on or reread

## Code Prompts

- "Explain the algorithm block in Section 3."
- "Walk me through this pseudocode."
- "Explain Algorithm 2 step by step."

## Code Output Shape

1. inputs and outputs
2. main stages or ordered steps
3. key decisions, loops, or updates
4. connection to formulas or modules in the paper
5. implementation intuition or likely confusion points

## Citation Prompts

- "Explain reference 21."
- "What paper is [21]?"
- "Tell me why this paper cites Bahdanau et al."
- "Give me the title and link for reference 8."

## Citation Output Shape

1. bibliographic facts
2. what kind of cited work it seems to be
3. why the current paper cites it
4. where it appears in the current paper
5. link to the source when available
6. whether it is worth reading next

Make it clear which parts are retrieved facts and which parts are inference from the current paper's citation context.

## Figure Or Table Prompts

- "Explain Figure 2 like I am new to this topic."
- "Read this table and tell me what actually matters."
- "I only care about the experiment section."

## Figure Or Table Output Shape

1. what the visual shows
2. how to read it
3. most important pattern
4. implication for the paper's claim
5. caution if extraction is uncertain

## Terminology Prompts

- "What is score matching in this paper?"
- "The paper assumes I know this concept. Please teach it to me."

## Terminology Output Shape

1. local meaning in the paper
2. broader background definition
3. why the concept matters here
4. comparison with related terms if useful
