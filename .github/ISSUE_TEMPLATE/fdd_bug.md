---
name: "FDD Bug"
about: "Template for resolving bugs and unexpected behavior."
title: "<action> the <result> <by | for | of | to> a(n) <object>"
labels: ["bug"]
assignees: ""
---

> [!TIP]
> Keep answers concise (2-5 bullet points or sentences per section). If your issue is larger than that, please separate it into smaller, linked issues. [Contact the developers]() if you need help splitting up a "god-issue".
>
> **Title Format:** Please ensure your issue title follows the FDD syntax above (e.g., *"Restore the connection stability of the Proxy-API"*).

### 1. The Bug
**Expected vs. Actual Behavior**
> * What was the intended solution or value you were looking for?
> * What actually happened instead?

[Your answer here]

**Reproduction**
> * How to provoke this bug again?
> * Which exact component(s) from the framework didn't work?
> * How would you verify it was fixed? 

[Your answer here]

### 2. Proposed Solution (Root Cause & Fix)
**Implementation Path**
> * What is the suspected root cause or the most likely code fix? 
> * *(It is open-source etiquette to attempt a guess, but if you have no idea, you can just write "Unknown" and put more time into documenting the bug if possible.)*

[Your answer here]

### 3. Constraints & Tech-Stack
**Limitations, Environment & Timing**
> * List the hardware (e.g., Zedboard), OS, software environment used. List everything that is part of the flow that produces the bug.

[Your answer here]

### 4. Appendix & Checklist
Please supply the following if applicable to help us debug faster:
- [ ] Stacktrace(s) as pure text files (`.txt`, `.md`, `.json`)
- [ ] Meaningful screenshots of the error or hardware state
- [ ] Relevant manifests (if they differ from the stable framework)
- [ ] Boilerplate code or test-payloads (`.py`, `.yaml`) to reproduce the bug

> *Final Check: Did you answer all sections? If a section doesn't apply, please write "N/A" and provide one reason why.*