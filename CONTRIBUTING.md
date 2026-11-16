# Contributing to i40-SAFTCH: Industry 4.0 Star-API Framework for Testing Continuously on Hardware
First off, thank you for considering contributing to the project! It's people like you that make the open-source and hardware-in-the-loop community such a great place to learn, inspire, and create. 

This document outlines the process for contributing to the repository. Please take a moment to review these guidelines before submitting a pull request or creating an issue.

## i40-SAFTCH Development Guidelines
Contributing to this framework is guided by three core philosophies. We expect all code to align with these principles to ensure our staging and deployment processes remain robust and reliable.

1. **Left-Shifting**
We believe in moving quality assurance, testing, and validation as early into the development cycle as possible. Contributors are expected to validate and verify their logic locally before opening a pull request. Catching an error on your own machine is always faster and cheaper than waiting for a continuous integration pipeline to reject it. 

2. **Fail Fast and Loudly**
When a system encounters an invalid state, it should halt immediately and with maximum visibility. We do not accept silent failures, ignored exceptions, or processes that limp along with corrupted data to fail somewhere else downstream. If a configuration is wrong or a test fails, the process must crash instantly and output a clear, undeniable error.

3. **Offensive Programming (over Defensive Programming)**
Instead of writing endless fallback logic to gracefully handle invalid inputs or unexpected behaviors, we expect code to assert its requirements aggressively. If an internal contract is violated, the code should crash intentionally rather than trying to guess a safe alternative. This forces bugs out into the open immediately and holds the caller accountable for providing correct data, rather than sweeping root causes under the rug.

## Non-Code Contributions: Feature Requests, Bug Reports, and Discussions
When thinking about contributing to an open-source project, the first thought is almost always to *contribute source code*. While contributing code is a vital part of open-source development, it is not the only way! Feature requests, bug reports, and [talking to other SAFTCH contributors](https://github.com/merlinseela/i40-saftch/discussions) are just as vital as writing code.

### Feature Requests and Bug Reports
When creating a new ticket (i.e., a GitHub Issue), SAFTCH provides specific templates for each type. We expect contributors to follow the guidelines within them. If you realize your issue does not fit one of the templates, or if you have difficulty filling them out, feel free to ask for assistance in the [discussion forum](https://github.com/merlinseela/i40-saftch/discussions)!

## Contributing Source Code
If you are ready to write code, update documentation, or expand the automated infrastructure, your contributions must adhere to our dual-branch architecture. We separate active integration from stable production to ensure the highest code quality and reliability.

**1. Forking and the Testing Branch**
To contribute, you will need to fork the repository. Our default branch is set to `testing`. All active development, integrations, and automated pipelines run against this branch. You can name your local working branch whatever you like, as long as it is based on your fork's `testing` branch. 

**2. Pre-flight Validation (Left-Shifting via your Fork)**
We believe in catching errors as early as possible. To save your local battery and eliminate complex environment setups, we rely on GitHub Actions for pre-flight checks. When you fork the repository and push commits to your `testing` branch, our automated linting and syntax workflows will run directly in your fork's cloud environment. (Note: You may need to navigate to the 'Actions' tab on your fork and click "Enable Workflows" the first time). Please ensure these basic checks pass on your fork before opening a pull request.

**3. Opening the Pull Request**
When opening a pull request, ensure it targets the upstream `testing` branch (GitHub should select this automatically). Your pull request title must follow the Conventional Commits specification (e.g., `feat:`, `fix:`, `chore:`). For a complete list of valid prefixes and examples, please refer to our [Conventional Commits Cheat Sheet](/docs/repository_governance/cheatsheet_conventional_commits.md). You do not need to use FDD syntax here! Instead, provide a concise summary of the overarching technical change. Inside the body of your pull request, you must explicitly link the specific issue(s) your code resolves (e.g., "Resolves #12"). Providing bullet points to further document the changes is highly appreciated and will lead to a faster review of your pull request!

**4. The Automated Gauntlet (Fail Loudly)**
Once your pull request is open, our CI/CD pipelines will execute. You are responsible for monitoring these checks. If your code triggers a failure, the pipeline will fail loudly. Review the logs, address the highlighted issues, and push the necessary fixes to your branch.

**5. Peer Review and Protected Files**
Certain structural files (such as legal documents, CI pipelines, and templates) are protected by repository `CODEOWNERS` and require mandatory approval from core maintainers. Once all automated checks pass and reviews are approved, a maintainer will merge your work into the `testing` branch.

**6. The Release Cycle (Testing vs. Main)**
Once your code is merged into `testing`, your job is done! The `testing` branch regularly generates snapshot releases, allowing developers to utilize bleeding-edge features immediately. The `main` branch remains locked as our pristine, stable version. Core maintainers periodically audit and manually promote code from `testing` into `main` for official, production-ready releases.