# OneAqua Insight Hub — Comprehensive Code & Architecture Audit

**Project:** OneAqua Insight Hub  
**Event:** IEEE OneAquaHealth Global Hackathon 2026 (Track 2: Data-to-Insight)  
**Audit Date:** 2026-09-25  
**Reviewer:** Environmental Data Engineer / Hackathon Judge

---

## Executive Summary

This is a **strong finalist-tier project** with authentic One Health mission alignment, real data pipelines (partial), novel ecological-human-climate synthesis, and polished dark-tech UX. Fixing the Gent/Benevento data gap and HHRI scaling would make it **judge-proof**. The scenario sandbox + policy export is a differentiator most hackathon projects lack.

---

## 1. Scientific & One Health Modeling Rigor

### Scoring Formulas (`src/engine.py`)

| Index | Formula | Weighting | Assessment |
|-------|---------|-----------|------------|
| **EHI** (Ecological Health Index) | `0.35*DO + 0.35*Macro + 0.15*pH + 0.15*Riparian` | DO & Macro dominate | ✅ Well-balanced; reflects WFD multi-metric approach |
| **HHRI** (Human Health Risk Index) | `0.55*Pathogen + 0.45*Vector` | Pathogen > Vector | ⚠️ **Critical**: Vector uses raw density 0-100 while pathogen is normalized to 900 CFU — scale mismatch inflates vector influence |
| **UCSI** (Urban Climate Stress) | `0.50*Heat + 0.50*Runoff` | Equal | ✅ Reasonable but heat stress baseline (42) and runoff (38) are arbitrary |
| **Overall Vitality** | `0.45*EHI + 0.35*(100-HHRI) + 0.20*(100-UCSI)` | EHI dominant | ✅ Aligns with One Health philosophy (ecology as foundation) |

### Threshold Accuracy vs. EU Water Framework Directive

| Threshold | Code Value | WFD/EU Standard | Status |
|-----------|-----------|-----------------|--------|
| Hypoxia DO | `< 5.0 mg/L` | **WFD Good/Moderate boundary ≈ 5-7 mg/L** ✅ |
| E. coli bathing | `> 400 CFU/100mL` | **EU Bathing Water Directive: Excellent ≤ 250, Good ≤ 500** ✅ |
| Vector proliferation | `> 21°C` | Literature: Culex pipiens optimal 20-25°C ✅ |
| pH optimal | `7.2` center | WFD: 6.5-8.5 ✅ |
| Riparian buffer goal | `> 60%` | EU Biodiversity Strategy: 10% land, but riparian specifically — reasonable proxy |

### Citizen Cross-Validation Logic

```python
# engine.py:143-176
confidence = 0.75  # base
if "Algal Bloom" in category and latest["DO"] < 6.0: confidence += 0.14
if "Macroinvertebrate" in category: confidence = 0.90  # hard-coded high
```

**Issues:**
1. **Macroinvertebrate gets 90% regardless of sensor data** — bypasses actual telemetry cross-check
2. **No spatial matching** — uses city-wide latest reading, not nearest sensor to report coordinates
3. **Confidence caps at 98%** — artificial ceiling without justification

---

## 2. Data Pipelines & Provenance

### Data Loading Flow (`src/data_loader.py`)

```python
def get_time_series_data(city_name, days=30):
    # 1. Try to load real CSV from data/
    # 2. If exists, parse with city-specific logic
    # 3. If fails OR file missing → synthetic fallback (np.random.seed(42))
```

**Problems:**
1. **Silent fallback** — line 270: `except Exception: pass` swallows ALL errors and falls back to synthetic data without logging
2. **Toulouse 3.2MB CSV** loaded entirely into memory on every city switch — no caching decorator
3. **No st.cache_data** on any loader → full reload on every widget interaction
4. **City file map hardcoded** — if `toulouse_real.csv` renamed, breaks silently

### Real Data vs. Synthetic

| City | File | Size | Source | Status |
|------|------|------|--------|--------|
| Toulouse | `toulouse_real.csv` | 3.2 MB | Hub'Eau API | ✅ Real |
| Coimbra | `coimbra_real.csv` | 11 KB | SNIRH calibrated | ⚠️ Synthetic with real params |
| Oslo | `oslo_real.csv` | 10 KB | NVE calibrated | ⚠️ Synthetic with real params |
| Gent | `gent_real.csv` | 32 KB | GBIF macroinvertebrates | ❌ Only occurrences, no water quality |
| Benevento | `benevento_real.csv` | 6 KB | ARPAC CKAN | ❌ Not parsed (fallback only) |

**Critical**: Gent and Benevento **never use their real files** — the loader only has parsing logic for Toulouse, Coimbra, Oslo. The others hit the silent fallback.

---

## 3. Streamlit Performance, State Management & Bugs

### Session State Issues (`app.py`)

```python
# Line 113-115, 133-135: DUPLICATE initialization
if f"reports_{selected_city}" not in st.session_state:
    st.session_state[f"reports_{selected_city}"] = reports_df.copy()
```

**Bug**: Initialized in **both** `tab_map` and `tab_citizen` — redundant but harmless.

### Widget Key Conflicts

```python
# simulator_view.py:32-38 — slider keys hardcoded
key="temp_delta", key="rain_delta", key="riparian_delta"
```
- Keys are global — if user switches cities, sliders **don't reset** (may be intentional for scenario continuity)
- No `key` prefix with city name → state bleeds across cities

### Missing Caching (Performance)

| Function | Called From | Cache Needed? |
|----------|-------------|---------------|
| `get_stream_segments()` | `app.py:78` | ✅ Yes — static per city |
| `get_sensor_nodes()` | `app.py:79` | ✅ Yes — static per city |
| `get_citizen_reports()` | `app.py:80` | ✅ Yes — static per city |
| `get_time_series_data()` | `app.py:81` | ✅ Yes — expensive CSV parsing |
| `calculate_one_health_indices()` | `app.py:83` | ⚠️ Depends on sim sliders |

**No `@st.cache_data` anywhere** — full recomputation on every slider move, tab switch, city change.

### Reactive Propagation

Scenario sliders → `calculate_one_health_indices()` → indices → all views. **This works correctly** because `app.py` recomputes indices on every render with current slider values from session state.

---

## 4. UI/UX, Aesthetics & Code Cleanliness

### Layout Hierarchy (per spec)

```
Header (Brand + Live Beacon + Track Badge) ✅
  → Hero Lead Metric (Vitality) ✅
  → 3 Pillar Cards (EHI, HHRI, UCSI) ✅
  → 5 Telemetry Stat Badges ✅
  → 4 Workspace Tabs (Map, Analytics, Citizen, Policy) ✅
```

### Typography & Design System

| Element | Implementation | WCAG 2.2 AA? |
|---------|---------------|--------------|
| Primary font | Plus Jakarta Sans (Google Fonts) | ✅ |
| Telemetry font | JetBrains Mono | ✅ |
| Dark theme base | `#0B0E14` | ✅ |
| Cyan accent | `#00F2FE` on dark | ✅ 7.8:1 contrast |
| Status chips | Semantic colors (green/amber/red) | ✅ |

**Clean**: No decorative emojis in UI (only in README). Professional hackathon tone maintained.

### Code Smells

1. **Inline HTML/CSS everywhere** — 400+ lines in `styles.py`, 200+ in `map_view.py`, 150+ in `matrix_view.py` — hard to maintain
2. **Magic numbers** throughout `engine.py` (0.35, 0.25, 18.0, 3.8, 42, 38, etc.) — no constants module
3. **Duplicate session state init** in `app.py` (lines 113 & 133)
4. **Broad exception handling** in `data_loader.py:269-270` — `except Exception: pass`
5. **No type hints** anywhere — reduces IDE support and readability

---

## 5. Final Assessment & Recommendations

### Top Strengths

1. **Authentic One Health framing** — genuinely connects stream ecology → human health → climate stress
2. **Real open data integration** — Toulouse Hub'Eau, Oslo NVE, Coimbra SNIRH are real pipelines
3. **Scenario sandbox** — temperature/runoff/riparian sliders with presets is a standout interactive feature
4. **Citizen science cross-validation** — novel concept, even if simplified
5. **Polished dark-tech UI** — glassmorphism, semantic colors, monospace telemetry — looks competition-ready
6. **Policy brief export** — tangible deliverable for decision-makers

### Critical Bugs / Edge Cases

| Severity | Issue | Location |
|----------|-------|----------|
| 🔴 High | Gent & Benevento real data **never loaded** — silent fallback to synthetic | `data_loader.py:156-288` |
| 🔴 High | `except Exception: pass` hides API failures | `data_loader.py:269` |
| 🟠 Medium | HHRI scale mismatch (vector 0-100 vs pathogen 0-900 normalized) | `engine.py:58-62` |
| 🟠 Medium | No `@st.cache_data` — full reload on every interaction | All loaders |
| 🟡 Low | Duplicate session state init | `app.py:113,133` |
| 🟡 Low | Widget keys bleed across city switches | `simulator_view.py:32-60` |

### Judging-Ready High-Impact Features (2-3)

#### 1. 🏆 Real Data Activation for All 5 Cities
- Parse Gent GBIF macroinvertebrates → derive BMWP/ASPT scores for EHI
- Parse Benevento ARPAC CKAN → extract actual DO, E. coli, nutrients
- Add `@st.cache_data` with 1-hour TTL + manual "Refresh Data" button

#### 2. 🏆 Spatial Citizen-Sensor Cross-Validation
- Use `reports_df` lat/lon + `sensors_df` lat/lon → find nearest sensor (haversine)
- Compare citizen category against **that sensor's** readings, not city-wide average
- Display "Verified by Sensor SN-102 (140m away)" in UI

#### 3. 🏆 Early-Warning Alert Persistence & History
- Store anomaly alerts in session state with timestamps
- Show "Alert History" in Policy tab with acknowledge/dismiss
- Export alerts to policy brief as "Active Advisories"

---

### Quick Wins (1-hour fixes)

```python
# 1. Add caching to data_loader.py
@st.cache_data(ttl=3600, show_spinner=False)
def get_time_series_data(city_name, days=30): ...

# 2. Fix HHRI scale normalization
eff_vector_norm = np.clip(eff_vector / 100.0 * 100, 0, 100)  # already 0-100
pathogen_risk = np.clip(eff_e_coli / 900.0 * 100, 0, 100)
hhri = 0.55 * pathogen_risk + 0.45 * eff_vector_norm

# 3. Fix silent fallback
except Exception as e:
    st.warning(f"[{city_name}] Real data load failed: {e}. Using calibrated baseline.")
    return synthetic_fallback(city_name, days)
```

---

## Verdict

**Finalist-tier** — Authentic mission alignment, real data pipelines (partial), novel One Health synthesis, polished UX. The scenario sandbox + policy export is a differentiator most hackathon projects lack.

Fixing the Gent/Benevento data gap and HHRI scaling would make this **judge-proof**.