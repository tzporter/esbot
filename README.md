<p align="center">
  <img src="./assets/esbot_logo.png" alt="ESBot Logo" width="180" />
</p>

<p align="center">
  <img alt="CI" src="https://github.com/tzporter/esbot/actions/workflows/ci.yml/badge.svg">
  <a href="LICENSE"><img alt="Educational" src="https://img.shields.io/badge/status-educational-blue"></a>
  <a href="docs/"><img alt="Docs" src="https://img.shields.io/badge/docs-available-brightgreen"></a>
  <a href="LICENSE"><img alt="License: Apache-2.0" src="https://img.shields.io/badge/license-Apache--2.0-blue"></a>
  <img alt="Labs" src="https://img.shields.io/badge/labs-12_planned-informational">
  <img alt="Made at HSE Esslingen" src="https://img.shields.io/badge/made%20at-HSE%20Esslingen-0a7ea4">
</p>

## ESBot (HSE Esslingen Software Testing Course)

> IMPORTANT: This repository is for educational purposes only. It may contain unfinished, faulty, or even non-executable code used solely for teaching during the Software Testing course. Do not use this repository for any production system.

### Overview
ESBot is a teaching project developed during the Software Testing course (SoSe 2026) at Esslingen University (HSE). ESBot is an AI-powered learning assistant that offers structured, chat-based learning sessions, focusing on explanations, examples, and lightweight quizzes for course content. Technically, ESBot follows a minimal three-tier architecture (frontend UI, application backend, and database) with an optional LLM inference component (e.g., Ollama, vLLM, LM Studio) integrated via the backend, making it well-suited for exploring integration and testing of AI-enabled systems.

For additional background, high-level expectations, and detailed system requirements, see the concept document in `docs/esbot.md`.

### Course Context and Objectives
- Learn and apply practical techniques in software testing across the development lifecycle
- Practice requirements engineering, collaboration, code reviews, and quality assurance
- Experience test design (black-/white-box), automation, CI, performance testing, and more

### Planned Lab Exercises and Submissions
Submissions for each exercise shall be organized in the `docs` folder.

- Group Formation & Project Setup
- Project Specification, Use Cases and Context Diagrams
- Perform a UX Evaluation
- Basic App Functionality & Unit Testing
- ATTD & BDD Implementations
- Project/Code Reviews & Static Analysis
- Design Black-/White-Box Test Cases
- Mock- & Integration Testing
- Local Test Automation via GitHooks
- Setting up own CI Pipeline
- Performance & Load Testing
- Automated UI Testing

### Documentation
- Project concept and expectations: [`docs/esbot.md`](docs/esbot.md)
- All lab deliverables and write-ups: `docs/`

### Notes
- The repository content evolves during the course and may intentionally include defects for learning purposes.
- If you discover issues, document them and propose fixes as part of your exercises (e.g., via pull requests or notes in `docs/`).


### License
This project is licensed under Apache 2.0. See: [LICENSE](LICENSE)
