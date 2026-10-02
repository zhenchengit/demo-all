# Python checkout review demo

A deliberately imperfect checkout service for demonstrating AI repository analysis. No PR is needed. Contains one Python source file and requires no third-party packages.

Run: `python3 order_service.py`

Ask your review tool:

> Analyze this repository against the business rules in the module docstring. Find reproducible logic and state-management bugs. Report severity, file and line, a minimal reproducer, and expected versus actual behavior. Run the code to verify findings. Do not change files or create a PR.

For a second task, ask the tool to fix the confirmed findings and validate boundary cases.

This is demonstration code, not a production checkout implementation.
