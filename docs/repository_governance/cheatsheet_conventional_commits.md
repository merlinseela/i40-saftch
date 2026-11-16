# i40-SAFTCH Conventional Commit Cheat Sheet

To ensure our automated changelog generation works correctly across the SAFTCH monorepo, all pull request titles must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

- **Mandatory Format:** `prefix: description`
- *Optional Format:* `prefix(scope): description`

## Valid Prefixes
| Prefix | Example | Explanation |
| :--- | :--- | :--- |
| **feat** | `feat(ssot): add proxy route for daemon communication` | Introduces a completely new feature or capability to the framework. |
| **fix** | `fix(edge): resolve timeout error in edge interface` | Patches a bug or resolves an unintended behavior in the codebase. |
| **docs** | `docs(repo): update CONTRIBUTING.md with workflow steps` | Modifications strictly related to documentation (markdown files, inline comments). |
| **style** | `style(edge): enforce PEP8 formatting in core daemon` | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons). |
| **refactor** | `refactor(edge): simplify hardware state machine logic` | A structural code change that neither fixes a bug nor adds a feature, but improves code health. |
| **perf** | `perf(ssot): optimize matrix calculation for faster polling` | A code change explicitly designed to improve execution performance. |
| **test** | `test(edge): add unit tests for hardware mock` | Adding missing tests or correcting existing automated tests. |
| **build** | `build(ssot): update pip dependencies and setup.py` | Changes that affect the build system, package versions, or external dependencies. |
| **ci** | `ci(repo): configure GitHub Actions for pre-flight linting` | Changes to CI/CD configuration files, workflows, and automated scripts. |
| **chore** | `chore(repo): update .gitignore rules` | Routine tasks, maintenance, or minor adjustments that do not modify source code or tests. |

## Valid Scopes
The scope indicates the specific part of the framework your pull request modifies. Please use one of the following standard scopes:
- **`edge`** - Changes related to the hardware edge nodes or edge daemon.
- **`ssot`** - Changes related to the Single Source of Truth, proxy server, or API.
- **`repo`** - Global changes that affect the entire repository (e.g., license updates, global `.gitignore`).