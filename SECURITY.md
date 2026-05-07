# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the defense implementations, the example code, or any infrastructure shipped from this repository, **please do not open a public issue**.

Instead, email **luisa@nubia-labs.com** with:

- A description of the vulnerability and the impact you believe it has.
- Steps to reproduce (a minimal proof-of-concept is ideal).
- The version or commit you tested against.
- Any suggested fixes, if you have them.

You'll get an acknowledgement within **5 business days**. We'll work with you to confirm the issue, agree on a fix, and coordinate disclosure. Please give us a reasonable window — typically 30 days, longer for complex issues — before publishing details.

## Scope

This repository is primarily a **learning and reference resource**. The defense implementations are written for clarity, not as drop-in production controls. With that in mind:

- **In scope:** Bugs in defense implementations that materially weaken the protection they claim to provide; security issues in the example LLM client, scenario, or benchmark code; issues in the published docs site; issues in CI workflows.
- **Out of scope:** Demonstrations that prompt injection itself is possible (yes, that's the point of the repo); reports against third-party tools the repo references; theoretical issues with no practical exploit path.

## After a Fix

Once a fix lands, the relevant `CHANGELOG.md` entry will credit the reporter (unless they prefer to remain anonymous) and link to the patch.

## General Bugs

For non-security bugs, typos, or content corrections, regular GitHub issues and pull requests are welcome.
