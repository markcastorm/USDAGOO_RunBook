# USDAGOO Runbook - Claude Working Context

## Project Status: COMPLETE & VALIDATED (100% Accuracy)
- Pipeline architecture fully implemented and verified against reference data.
- 100% accuracy achieved: 264/264 data points match exactly for years 2023-2026.
- Scraper successfully handles USDA's top-level and accordion-style report links.

---

## Final Pipeline Flow
`main.py` -> `orchestrator.py` -> `scraper.py` | `extractor.py` | `file_generator.py`

### 1. scraper.py (Final)
- **Tech**: Selenium Stealth + Chrome Auto-Download.
- **Logic**:
  - Dynamically detects the latest year or specific year from config.
  - Searches both the "Outlook Reports" top section and the "ckeditor-accordion" historical items.
  - Bypasses sticky UI overlays using JavaScript clicks.
  - Monitors the download directory for PDF completion.

### 2. extractor.py (Final)
- **Tech**: PyMuPDF (`fitz`) `find_tables()` + Pandas.
- **Logic**:
  - Robust row-by-row and column-by-column mapping.
  - Handles multi-line merged labels (Corn/Wheat style) and split cell structures (Soybean style).
  - Normalizes years (`2023/24` -> `2023`) and cleans labels of footnote markers.
  - Mapping: 100% field coverage for Corn, Soybean, Soybean Meal, Soybean Oil, and Wheat.

### 3. file_generator.py (Final)
- **Output**: Generates `.xls` (DATA & META) and `.zip` archive.
- **Format**: Follows the two-header-row standard (Row 0: Codes, Row 1: Descriptions).
- **Metadata**: Includes `LAST_RELEASE_DATE` extracted from PDF properties.

---

## Technical Successes
- **Accuracy**: Validated via `compare_outputs.py` against `USDAGOO_DATA_20240306 - 2026.csv`.
- **Speed**: Optimized search avoids full PDF reads, focusing on target pages (usually 6-10).
- **Headless**: Verified operation in `headless=new` mode with Stealth.

---

## Files Produced
| Category | Location |
|----------|----------|
| Source Code | Root directory (`*.py`) |
| Downloads | `downloads/<timestamp>/` |
| Output Files | `output/<timestamp>/` and `output/latest/` |
| Verification | `compare_outputs.py` and `test_extraction_all.py` |
