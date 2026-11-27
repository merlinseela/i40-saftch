# i40-saftch Roadmap

> [!NOTE]
> This roadmap is a living document. It communicates the general direction and current baseline of the core maintainers and contributors, not a rigid schedule set in stone.
>
> Want to pull a feature forward, add support for another hardware target, or propose something not listed here? Contributions outside this baseline are explicitly welcome. Open a [Discussion](https://github.com/merlinseela/i40-saftch/discussions) to align before diving in.

| Status | Meaning | Release blocks |
| --- | --- | --- |
| Done | Completed work | v0.1.0 |
| Active | Work in progress | v0.1.1 |
| Planned | Work on the roadmap | v0.2.0, v0.3.0, v0.3.1 |
| Future | Work without a release version | Looking Ahead |

```mermaid
---
config:
  flowchart:
    wrappingWidth: 600
    padding: 20
---

flowchart TD
    v010["`**v0.1.0 ─ saftch Proof of Concept (PoC)** 
        ───────────────────────────────────────────────────────────
        • PoC: ZedBoard HiLDaemon + 
        &nbsp; &nbsp;FastAPI-Proxy as Anti-Corruption-Layer (ACL) +
        &nbsp; &nbsp;BaSyx-Backend
        `"]
    v011["`**v0.1.1 ─ saftch PoC Stabilization & Documentation Patch** 
        ───────────────────────────────────────────────────────────
        • Language-agnostic Documentation (LaD) of PoC
        • Align/Refactor of ZedBoard HiLDaemon to fit LaD 
        • Align/Refactor of FastAPI-ACL-Proxy to fit LaD
        • Migrate PoC Asset Administration Shell (AAS) templates from AASX to JSON
        `"]
    v020["`**v0.2.0 ─ Single-Target Fleet Management**
        ───────────────────────────────────────────────────────────
        • Multi-board registration (for ZedBoard)
        • Multi-board job routing across registered boards
        • AAS-based state tracking of HiLDaemon & Hardware Designs
        • Lightweight UI integrated in ACL
        • Pydantic payload validation
        • Unit testing for Fleet Management
        • LaD for Fleet Management and Testing
        `"]
    v030["`**v0.3.0 ─ Idempotent Setup**
        ───────────────────────────────────────────────────────────
        • HiLDaemon (ZedBoard) provisioning (setup.sh + systemd on PYNQ 2.7)
        • Singel-Source-of-Truth (SSOT) provisioning (docker compose + nginx template)
        • LaD for Linux-based HiLDaemon deployment
        • LaD for Linux-based Server deployment
        `"]
    v031["`**v0.3.1 ─ PYNQ 2.7 Hardening (ZedBoard)**
        ───────────────────────────────────────────────────────────
        • Strict auditing documentation of PYNQ 2.7 for headless deployment
        • Enhance HiLDaemon setup to harden PYNQ 2.7 for headless deployment
        `"]
    vXXX["`**vX.X.X ─ Looking Ahead**
        ───────────────────────────────────────────────────────────
        • Semantic Precision & Reproducibility (strictly AAS-aligned)
        • Edge/SSOT Resilience (Watchdogs, Zombie-HiLDaemon recovery (ZedBoard))
        • Multi-Hardware-Targets & Extensibility (Beyond ZedBoard)
        • Multi-Hardware-Design-Toolchain Compatibility (Beyond Vivado 2020.2)
        • Security Layer & User Management (OAuth2, AAS RBAC)
        • SSOT-Proxy Plugin Architecture (Pluggable matchers & schemas)
        `"]

    v010 --> v011 --> v020 --> v030 --> v031 --> vXXX

    classDef done fill:#1e3a2f,stroke:#4ade80,color:#f0fdf4,stroke-width:1px,text-align:left
    classDef active fill:#1e3a5f,stroke:#60a5fa,color:#eff6ff,stroke-width:1px, text-align:left
    classDef planned fill:#27272a,stroke:#71717a,color:#f4f4f5,stroke-width:1px, text-align:left
    classDef future fill:#2e1d47,stroke:#a78bfa,color:#f5f3ff,stroke-width:1px,stroke-dasharray:5 5,text-align:left

    class v010 done
    class v011 active
    class v020,v030,v031 planned
    class vXXX future

    subgraph statusLegend["Status legend"]
        direction LR
        legendDone["Done"]:::done
        legendActive["Active"]:::active
        legendPlanned["Planned"]:::planned
        legendFuture["Future"]:::future
    end
```
