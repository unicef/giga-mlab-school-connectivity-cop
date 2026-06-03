# National Digital Learning Platforms — Structured Database

**Folder:** `2026-05-EduPlatformsDatabase`
**Prepared by:** Giga (UNICEF-ITU) — Maria Abravo Reyes
**Date:** May 2026

---

## Base data

EdTech Hub (2023). *Mapping Digital Learning Platforms Across 184 Countries.*
https://edtechhub.org/2023/07/21/mapping-digital-learning-platforms-across-184-countries/

Original dataset covers 492 national government or government-endorsed digital learning platforms across 184 countries, assessed against minimum equity and access requirements (offline capability, smartphone compatibility, language coverage, account requirements, content quality indicators).

---

## Files

### `edtech_national_platforms_tiered.csv`
Full dataset — 492 rows, all platforms including unavailable ones and those without a URL.

### `edtech_national_platforms_measurable.csv`
Filtered subset — 400 rows. Platforms that are: (1) currently available, (2) have a resolvable URL, (3) not hosted on generic infrastructure (e.g. sites.google.com). Adds 12 Mexico entries sourced from IQB-Edu content geography research (`source=Claude`, `validated=False`).

---

## Key columns

| Column | Description |
|---|---|
| `platform_classification` | `national` / `collaboration` / `other` / `unknown` — positively derived from domain signals (ccTLD, `.gov.`/`.gob.`/`.edu.` labels, country name in URL) |
| `platform_format` | EdTech Hub classification: resource hub / LMS / other / unknown |
| `platform_type` | Underlying technology if annotated (YouTube, Google, Moodle, Learning Passport, etc.) |
| `tier` | 1 = country-specific national platform · 2 = generic collaboration tool · 3 = other generic platform |
| `source` | `EdTechHub` (base data) or `Claude` (IQB-Edu research addition) |
| `validated` | `True` for EdTechHub records; `False` for Claude-sourced additions pending manual review |

---

## Intended use

This database supports IQB-Education content geography research: identifying which digital education platforms schools in a given country need to reach, and measuring whether those platforms are reachable and resolvable from school networks. The `domain` column is directly usable as an input to RIPE Atlas DNS measurements.
