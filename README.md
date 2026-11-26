# Loan Application Management System

## Overview

A Python-based command-line application designed to manage customer information, loan applications, and simulate core lending operations.

The project is being developed incrementally, following software engineering practices such as modular architecture, object-oriented programming, separation of concerns, exception handling, logging, and automated testing.

## Objectives

The application aims to provide the following capabilities:

- Customer registration and management
- Loan application management
- EMI calculation
- Loan eligibility assessment
- Repayment schedule generation
- CSV-based repayment analysis

## Technology Stack

- **Language:** Python
- **Programming Paradigm:** Object-Oriented Programming
- **Data Persistence:** JSON
- **Testing:** Pytest
- **Data Processing:** CSV
- **Version Control:** Git and GitHub

## Implemented Features

### Phase 1 — Project Foundation

- Configured Python project structure using the `src` layout.
- Configured virtual environment and project dependencies.
- Established Git version control.
- Configured pytest for automated testing.
- Implemented application logging.

### Phase 2 — Customer Management

- Implemented Customer model using Python dataclasses.
- Implemented unique customer ID generation.
- Implemented customer information validation.
- Implemented customer registration and retrieval.
- Implemented JSON-based customer persistence.
- Implemented customer repository and service layers.
- Added unit and integration tests.

## Project Structure

The application follows a modular architecture with separate packages for models, services, repositories, validators, utilities, and exceptions.

```text
loan-application-management/
│
├── src/
│   └── loan_management/
│       ├── models/
│       ├── services/
│       ├── repositories/
│       ├── validators/
│       ├── exceptions/
│       └── utils/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── data/
├── logs/
├── README.md
├── pyproject.toml
└── .gitignore
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd loan-application-management
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install the project in editable mode

```bash
pip install -e ".[dev]"
```

## Running Tests

Execute the complete test suite:

```bash
pytest -v
```

Execute integration tests only:

```bash
pytest tests/integration/ -v
```

## Project Status

**Currently under development.**

- Phase 1: Project Foundation — Completed
- Phase 2: Customer Management — Completed
- Phase 3: Loan Application Management — Planned
- Phase 4: EMI Calculation Engine — Planned
- Phase 5: Eligibility Assessment — Planned
- Phase 6: Repayment Schedule Generator — Planned
- Phase 7: CSV Repayment Analysis — Planned
- Phase 8: Integration and Quality Assurance — Planned
