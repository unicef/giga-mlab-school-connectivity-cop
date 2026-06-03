# National Digital Learning Platforms — Structured Database

**Folder:** `2026-05-EduPlatformsDatabase`
**Date:** May 2026

---

## Base data

EdTech Hub (2023). *Mapping Digital Learning Platforms Across 184 Countries.*
https://edtechhub.org/2023/07/21/mapping-digital-learning-platforms-across-184-countries/

Original dataset covers 492 national government or government-endorsed digital learning platforms across 184 countries, assessed against minimum equity and access requirements (offline capability, smartphone compatibility, language coverage, account requirements, content quality indicators).

---

## File

### `edtech_national_platforms.csv`
492 rows across 184 countries. Includes all platforms from the EdTechHub source plus additions from IQB-Edu content geography research. Covers platforms regardless of availability or URL status — filter on `available` and `has_url` as needed.

---

## Key columns

| Column | Description |
|---|---|
| `platform_classification` | `national` / `collaboration` / `other` / `unknown` — positively derived from domain signals (ccTLD, `.gov.`/`.gob.`/`.edu.` labels, country name in URL) |
| `platform_format` | EdTech Hub classification: resource hub / LMS / other / unknown |
| `platform_type` | Underlying technology if annotated (YouTube, Google, Moodle, Learning Passport, etc.) |
| `source` | `EdTechHub` (base data) or `Claude` (IQB-Edu research addition) |
| `validated` | `False` for platforms not verified against official government sources |

---

## Intended use

This database supports IQB-Education content geography research: identifying which digital education platforms schools in a given country need to reach, and measuring whether those platforms are reachable and resolvable from school networks.
