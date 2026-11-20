---
group: Frontend and UX
id: "13"
version: 0.4
reviewed: 2026-11-17
---

# 13 · Frontend and UX

For projects with a user interface.

## 13.1 Accessibility from the first screen
- applies: interfaces has web-ui
- rule: Target WCAG 2.2 AA: semantic HTML, keyboard navigation, labels, sufficient contrast. Run automated accessibility checks in CI.
- why: Retrofitting accessibility is far more expensive than building it in, and it may be legally required (see 09.9).

## 13.2 Internationalisation ready
- applies: interfaces has web-ui AND stage>=mvp
- rule: Always format dates, numbers and currency by locale. Externalise user-facing strings into an i18n library when a second language is planned or likely.
- why: Extracting strings later touches every screen.
- alternatives: single hard-coded language
- choose-when: externalise strings only when a second locale is planned or likely; single-language internal tools keep strings inline

## 13.3 Component structure
- applies: interfaces has web-ui
- rule: Build the UI from reusable components following one design system; keep business logic out of view components.
- why: Consistent UI and testable logic.

## 13.4 Web performance
- applies: interfaces has web-ui AND stage=production
- rule: Monitor Core Web Vitals from real users and keep them in the "good" range.
- why: Directly affects user experience and search ranking.
