---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Why this course exists

A web framework is a transformation from an incoming server request to a response. Building its small core makes routing, middleware ordering, error boundaries, and dependency injection observable rather than magical.

## Prerequisites

Complete [Backend Essentials](../backend-essentials/learning/overview.md) and [Networking Essentials](../networking-essentials/learning/overview.md). You should already know HTTP methods, status codes, request/response handling, Python functions, and decorators.

## Run the examples

Every example is a standard-library Python module under `learning/code/` and runs with `python3 example.py` from its directory. WSGI examples expose `application(environ, start_response)`; ASGI examples include an in-process event harness that exercises the server-facing callable.
