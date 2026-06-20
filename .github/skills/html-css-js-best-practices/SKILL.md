---
name: html-css-js-best-practices
description: "Use when creating, editing, or modifying any HTML, CSS, or JavaScript file. Enforces semantic markup, accessible styling, secure and modern JS patterns. Triggers on: new HTML page, add CSS styles, write JS logic, frontend component, form, UI, layout, script, stylesheet."
argument-hint: "Optional: area of focus — html | css | js | security | accessibility | all"
---

# HTML / CSS / JavaScript Best Practices

## When to Use

Load this skill whenever you are:
- Creating or editing `.html`, `.css`, or `.js` files
- Adding UI components, forms, layouts, or scripts
- Reviewing frontend code for quality, security, or accessibility

---

## HTML Best Practices

### Structure & Semantics
- Always start with `<!DOCTYPE html>` and a `<html lang="...">` attribute.
- Use semantic elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>` — never `<div>` for everything.
- One `<h1>` per page; maintain a logical heading hierarchy (`h1` → `h2` → `h3`).
- Include `<meta charset="UTF-8">` and `<meta name="viewport" content="width=device-width, initial-scale=1.0">` in every `<head>`.

### Accessibility (a11y)
- Every `<img>` must have a descriptive `alt` attribute (empty `alt=""` for decorative images).
- Every `<input>` must have an associated `<label>` (use `for`/`id` pairing or wrap the input).
- Use `aria-label`, `aria-describedby`, or `role` attributes when native semantics are insufficient.
- Ensure keyboard navigability — interactive elements must be reachable via `Tab` and operable via `Enter`/`Space`.
- Use `<button>` for actions, `<a href>` for navigation — never a `<div onclick>` for either.

### Performance & Loading
- Load CSS in `<head>`; load JS at the end of `<body>` or use `defer` / `async` on `<script>` tags.
- Prefer external files over inline `<style>` or `<script>` blocks (except for critical CSS or tiny snippets).

### Security
- Never place raw user-supplied data directly inside HTML without sanitization.
- Avoid `target="_blank"` without `rel="noopener noreferrer"` to prevent reverse tabnapping.

---

## CSS Best Practices

### Naming & Organization
- Use a consistent naming convention: prefer **BEM** (`block__element--modifier`) for component-based styles.
- Group related rules: layout → typography → colors → spacing → animation.
- Define reusable values as **CSS custom properties** (`--color-primary: #2e7d32;`) in `:root`.

### Layout
- Use **Flexbox** for one-dimensional layouts, **CSS Grid** for two-dimensional layouts.
- Avoid `float` for layout; use it only for text-wrapping around images.
- Never use fixed pixel widths that break responsiveness; prefer `%`, `rem`, `em`, `clamp()`.

### Responsive Design
- Follow a **mobile-first** approach: base styles target small screens, media queries add complexity for larger screens.
- Use `min-width` queries: `@media (min-width: 768px) { ... }`.

### Accessibility
- Ensure a minimum color contrast ratio of **4.5:1** for normal text (WCAG AA).
- Never remove the `:focus` outline without replacing it with a visible alternative.
- Use `prefers-reduced-motion` to disable or reduce animations for users who prefer it.

### Maintainability
- Avoid `!important` — if you need it, the specificity architecture is broken.
- Keep selectors shallow (max 3 levels deep) to avoid specificity wars.
- Remove dead/unused rules before committing.

---

## JavaScript Best Practices

### Syntax & Style
- Always use `const` by default; use `let` only when reassignment is needed; never use `var`.
- Use **strict mode**: add `"use strict";` at the top of scripts (automatic in ES modules).
- Prefer **arrow functions** for callbacks; use named function declarations for top-level logic.
- Use **template literals** instead of string concatenation.
- Use **optional chaining** (`?.`) and **nullish coalescing** (`??`) to handle nullable values safely.

### Async Patterns
- Use `async/await` over raw Promises `.then()/.catch()` chains for readability.
- Always handle errors: wrap `await` calls in `try/catch` or attach `.catch()`.
- Never use synchronous XHR or blocking operations on the main thread.

### DOM Interaction
- Cache DOM queries in variables rather than querying the DOM repeatedly.
- Use `element.textContent` to insert plain text — **never `element.innerHTML` with user-supplied data** (XSS risk).
- Prefer **event delegation** over attaching individual listeners to many elements.
- Use `document.addEventListener('DOMContentLoaded', ...)` or place scripts with `defer` to ensure the DOM is ready.

### Security (OWASP)
| Risk | Mitigation |
|------|-----------|
| XSS | Use `textContent`; sanitize before `innerHTML`; use a trusted sanitizer library (e.g. DOMPurify) |
| Prototype pollution | Avoid `Object.assign({}, userInput)` with untrusted data; use `JSON.parse(JSON.stringify(...))` or structured clone |
| `eval()` | Never use `eval()`, `new Function(str)`, or `setTimeout(string)` |
| Hardcoded secrets | Never embed API keys, tokens, or passwords in client-side JS |
| Open redirect | Validate URLs before `window.location` assignments |

### Modules & Structure
- Prefer **ES Modules** (`import`/`export`) over IIFE globals.
- Keep functions small and single-purpose; extract reusable logic into named helpers.
- Validate all inputs at the boundary (form submissions, API responses) before use.

---

## Checklist Before Finishing

- [ ] HTML is valid and uses semantic elements
- [ ] All images have `alt` text; all inputs have labels
- [ ] CSS uses custom properties for repeated values
- [ ] No `!important`, no broken focus states
- [ ] JS uses `const`/`let`, no `var`, no `eval()`
- [ ] User data is never inserted raw into the DOM
- [ ] Async code has error handling
- [ ] No hardcoded secrets or credentials in JS
- [ ] Responsive layout works on mobile screen sizes
- [ ] Keyboard navigation works for all interactive elements
