![i40-SAFTCH Banner](github_banner.jpg)

[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=for-the-badge&logo=apache&logoColor=white)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github&logoColor=white)](CONTRIBUTING.md)

## 📖 Overview
**i40-SAFTCH** is an open-source, automated Hardware-in-the-Loop (HIL) testing framework designed for Industry 4.0 environments. It bridges the gap between high-level CI/CD pipelines and low-level hardware targets (such as FPGAs and SoC boards like the Zedboard), enabling seamless, automated testing of hardware designs as if they were standard software components.

By utilizing Asset Administration Shells (AAS) and a decoupled proxy architecture, i40-SAFTCH provides a scalable, standardized API to deploy, test, and validate hardware configurations continuously.

## ⚡ Core Philosophies
This framework is built on three strict engineering principles:
1. **Left-Shifting:** Quality assurance and testing happen as early as possible.
2. **Fail Fast and Loudly:** Invalid states cause immediate halts with maximum visibility. No silent failures.
3. **Offensive Programming:** We assert internal contracts aggressively rather than writing endless defensive fallbacks.

## 🏗️ Repository Architecture
i40-SAFTCH is structured as a monorepo, divided into distinct scopes to cleanly separate the hardware edge from the cloud/proxy infrastructure:

* **`/edge`**: Contains the edge daemons, hardware interfaces, and state machines running directly on the hardware targets (e.g., Zedboard/Zynq).
* **`/ssot`**: The Single Source of Truth. Contains the FastAPI proxy, AAS templates, and deployment configurations that manage the fleet of edge devices.
* **`/docs`**: Framework documentation, hardware specs, and repository governance (including our [Conventional Commits Cheat Sheet](docs/repository_governance/cheatsheet_conventional_commits.md)).
* **`/.github`**: CI/CD workflows, issue templates, and automated pre-flight checks.

## 🚀 Getting Started

> [!NOTE]  
> This section is currently under construction. Setting up the entire Toolchain (Single-Source-of-Truth, Edge Daemon) of this Framework is not a 10-minute task. BUT automation is on the way with later releases. If you want to know what is coming and want to help with the development, Check out the Issue-Section and Contributing guide!


