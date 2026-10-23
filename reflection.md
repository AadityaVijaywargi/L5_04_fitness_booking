# Reflection

The handout PDF does not print the reflection questions, so these answer the four standard questions for this lab.

## 1. Which issues were the easiest and which were the hardest to fix?

The easiest were the mechanical ones: Flake8's blank-line messages, the f-string, `.items()` and the rename. The tool says exactly what to change and the fix cannot change behaviour. The Bandit finding was also quick to fix, but it needed a decision: instead of quoting the prefix for the shell, I removed the shell entirely and used `pathlib`, which is safer than trying to sanitise the string. The hardest were the logic bugs, because no tool reported them. I only found the off-by-one in the capacity check, the accepted "Pilates" class and the negative capacity by running the program and noticing that Yoga had four people booked at capacity three. Fixing those meant deciding what the program *should* do (reject unknown classes, raise on negative seats, treat bad input as zero guests).

## 2. Did the tools report any false positives, or miss anything?

I did not see a clear false positive. Every Pylint, Flake8 and Bandit message pointed at something real, although a few are judgement calls: the missing-docstring messages are style rather than defects, and Bandit's B605 is only dangerous if `prefix` can be influenced by a user (here it was a default argument, so it was a latent risk rather than an active exploit). The bigger lesson was what the tools missed. None of them caught the off-by-one comparison, unknown classes, negative capacity, duplicate bookings, mixed `int`/`str` IDs or the unvalidated `int(input())`. Static analysis checks patterns, not intent, so a perfect 10/10 score can still sit on top of wrong behaviour.

## 3. How would you integrate static analysis into a real workflow?

I would run Flake8 (or a formatter such as Black) in a pre-commit hook so style problems never reach review, and run all three tools in CI on every pull request, failing the build on any Bandit High/Medium finding and on a Pylint score below a threshold such as 9.5. Teams usually agree on a shared configuration (`.pylintrc`, `setup.cfg`) so the rules are consistent, and use targeted `# noqa` or `# nosec` comments with a written reason for the rare real false positive. Running the tools in an editor gives feedback while typing. They complement code review and tests rather than replace them.

## 4. What tangible improvements did you see after fixing the issues?

The measurable change was Pylint from 6.60 to 10.00, Bandit from 1 High issue to none, and Flake8 from 10 findings to none. The practical changes matter more: the code can no longer be turned into a shell command, it no longer leaks an open file or shares one hidden list between calls, errors are handled by name instead of being swallowed, and the program refuses bad input instead of crashing. It is also easier to read and reuse: every function has a docstring, names follow PEP 8, and importing the module no longer runs the demo, so it could now be unit tested. Running it again shows the behaviour is correct (Yoga stops at 3 members, Pilates is rejected, `-2` capacity is refused).
