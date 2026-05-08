# Tauri — Cross-Platform Desktop Apps with Web Technologies

> GitHub Stars: 90k+ | Language: Rust + TypeScript | Category: Desktop Framework

## What Is Tauri?

Tauri lets you build cross-platform desktop applications using web technologies (HTML, CSS, TypeScript) for the UI and Rust for the backend. It's the modern alternative to Electron — smaller binaries, lower memory usage, and native performance.

## Why We Dissect This Project

Tauri represents the **best of both worlds**: web developer ergonomics with systems programming performance. It demonstrates:
- How to design a secure IPC (inter-process communication) bridge
- How TypeScript and Rust can work together seamlessly
- How to build cross-platform apps with a single codebase
- The "command" pattern for frontend-backend communication

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              Frontend (WebView)                 │
│  HTML + CSS + TypeScript                        │
│  invoke('greet', { name: 'Alice' })             │
├─────────────────────────────────────────────────┤
│              Tauri IPC Bridge                   │
│  Serialized commands, event system              │
├─────────────────────────────────────────────────┤
│              Rust Backend                       │
│  Commands, State, File System, OS APIs          │
│  #[tauri::command] fn greet(name: &str)         │
├─────────────────────────────────────────────────┤
│              Operating System                   │
│  Windows / macOS / Linux                        │
└─────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Security by Default
Tauri commands are explicitly declared. The frontend can only call what you expose — no arbitrary system access.

### 2. Small Binaries
Tauri uses the system's native WebView (WebKit on macOS, WebView2 on Windows) instead of bundling Chromium. Result: ~3MB vs ~150MB.

### 3. Command Pattern
Frontend calls `invoke('command_name', args)`. The Rust side has `#[tauri::command]` functions that handle them.

### 4. Event System
Bidirectional communication: frontend can emit events to backend, backend can emit events to frontend.

## Learning Objectives

After dissecting Tauri, you will understand:
- How IPC bridges work between frontend and backend
- The command pattern for cross-language communication
- How to design secure APIs that limit attack surface
- How TypeScript types can be generated from Rust code

## Files in This Module

| File | Description |
|------|-------------|
| [patterns.md](./patterns.md) | Core design patterns analysis |
| [dissect.ts](./dissect.ts) | Atomic code dissection with inline tests |
