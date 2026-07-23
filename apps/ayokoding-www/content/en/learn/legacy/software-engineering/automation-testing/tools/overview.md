---
title: "Overview"
weight: 100000
date: 2025-12-29T00:00:00+07:00
draft: false
description: "Testing tools and frameworks — Playwright for end-to-end tests, Testing Library for component tests, and Vitest for unit tests"
tags: ["testing", "automation-testing", "playwright", "testing-library", "vitest"]
---

This section covers the tools that automate software testing across the pyramid — from fast unit tests to full end-to-end browser tests. Each tool includes annotated, runnable By Example tutorials.

## Tools in This Section

- **[Playwright](/en/learn/software-engineering/automation-testing/tools/playwright)** - End-to-end browser automation and testing across Chromium, Firefox, and WebKit, with auto-waiting, tracing, and parallel execution. Includes both By Example and In-the-Field production guides.
- **[Testing Library](/en/learn/software-engineering/automation-testing/tools/testing-library)** - User-centric component and DOM testing that queries the UI the way users do, encouraging accessible, behavior-focused tests.
- **[Vitest](/en/learn/software-engineering/automation-testing/tools/vitest)** - Fast, Vite-native unit test runner with a Jest-compatible API, watch mode, and built-in coverage.

## The Testing Pyramid

These tools map onto the classic testing pyramid:

- **Unit tests (most numerous)** → **Vitest** — fast, isolated tests of individual functions and modules.
- **Component / integration tests** → **Testing Library** — verify rendered UI behavior and component interaction.
- **End-to-end tests (fewest)** → **Playwright** — exercise the whole application through a real browser.

## Learning Approach

Each tool provides a **By Example** tutorial with annotated, runnable code:

- **Beginner** - Core concepts, first tests, basic assertions
- **Intermediate** - Realistic suites, fixtures, mocking, and async testing
- **Advanced** - Complex scenarios, optimization, CI integration, and production patterns

## Getting Started

- **Testing units and functions?** → [Vitest](/en/learn/software-engineering/automation-testing/tools/vitest)
- **Testing UI components?** → [Testing Library](/en/learn/software-engineering/automation-testing/tools/testing-library)
- **Testing full user flows in a browser?** → [Playwright](/en/learn/software-engineering/automation-testing/tools/playwright)

A healthy suite uses all three: many Vitest unit tests, fewer Testing Library component tests, and a focused set of Playwright end-to-end tests.
