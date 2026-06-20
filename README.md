# ICE AT NIGHT
### ICE Detentions — Before & After

An interactive web map of ICE civil immigration detention facilities across the U.S., visualized against NASA VIIRS nighttime satellite imagery. The map is split around January 20, 2025: 262 of 323 pre-existing facilities grew (81%), 212 new sites activated, and the share of detainees with a criminal conviction fell from ~60% to ~38% as detention expanded. Facility popups include conviction rates for both periods, drawn from daily FOIA-released population data. This project was created for University of Kentucky New Maps Plus Program during Spring Semester 2026. 

**Live map:** [https://danieldilger.github.io/map673_nice_sleep](https://danieldilger.github.io/map673_nice_sleep)

---

## 1. Data source

**Primary dataset — ICE detention facilities**

Government data provided by ICE in response to FOIA requests, processed by the [Deportation Data Project](https://deportationdata.org) at UCLA, and analyzed by the author. The dataset records every facility in which at least one civil immigration detainee was held since January 1, 2025. It includes dedicated ICE facilities, intergovernmental service agreement (IGSA) facilities, private contractor-run facilities, and short-hold locations such as hospitals and staging areas. Facility coordinates were geocoded using Google Maps API and manually verified.

Interactive data explorer and download: [ice-detention-facilities.apps.deportationdata.org](https://ice-detention-facilities.apps.deportationdata.org/)

The dataset was downloaded as XLSX, trimmed to 13 columns, and cleaned using Python/pandas. Facilities with missing coordinates were dropped prior to export. Headers were renamed to snake_case for PapaParse compatibility.

Fields used in this project:

| Field | Description |
|---|---|
| `facility_id` | Unique detention facility code |
| `name` | Facility name |
| `city`, `state`, `county` | Location |
| `lat`, `lon` | Verified geocoordinates |
| `field_office` | ICE ERO field office (24 offices nationally) |
| `cbsa_type` | Metro / Micro / Rural — built-in urban classification |
| `avg_midnight_pop` | Average overnight detained population (primary metric) |
| `max_midnight_pop` | Peak overnight population |
| `days_midnight` | Days per year with at least one overnight detainee |

**Sample data (2 rows):**

```
facility_id,name,city,state,county,lat,lon,field_office,cbsa_type,cbsa_name,days_midnight,avg_midnight_pop,max_midnight_pop
ABRXSPA,Abraxas Academy,Morgantown,PA,Berks,40.19,-75.92,Philadelphia,Metro,"Reading, PA",43,0.6,5
ADAMSMS,Adams County Correctional Center,Natchez,MS,Adams,31.56,-91.22,New Orleans,Micro,"Natchez, MS-LA",365,2158.8,2563
```

**Derived dataset — before/after comparison (`facilities_before_after.csv`)**

Produced from the daily population dataset using `before_after.py` (Python 3.11 / pandas). The script splits on January 20, 2025 (inauguration day) and computes per-facility averages for each period. Fields: `avg_midnight_before`, `avg_midnight_after`, `convicted_rate_before`, `convicted_rate_after`, `female_rate_before`, `female_rate_after`, `active_days_before`, `active_days_after`. Joined client-side to the main facilities CSV on `facility_id`. Facilities absent in the before period are hidden when the map is in before mode. Output: 707 facilities.

**Daily population dataset — `facilities-daily-population-latest.csv`**

Per-facility, per-day ICE detention counts from October 2022 to present, released via FOIA and processed by the Deportation Data Project. Fields include `n_detained`, `n_detained_at_midnight`, `n_detained_male`, `n_detained_female`, `n_detained_convicted_criminal`, `n_detained_possibly_under_18`. Semicolon-separated despite `.csv` extension. Used as input to `before_after.py` — not loaded client-side. Source: [deportationdata.org](https://deportationdata.org)

**Secondary dataset — ICE field office areas of responsibility (AOR)**

Polygon boundaries for 24 ICE ERO field offices, from the same source. Used as a context and filter layer. Download: [ice-offices.apps.deportationdata.org](https://ice-offices.apps.deportationdata.org/)

**Reference layer — U.S. cities**

Natural Earth `ne_10m_populated_places`, filtered client-side to U.S. cities with population ≥ 100,000. Source: [github.com/nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector)

**Airport layer — ICE Air departure hubs**

Eleven ICE Air departure airports compiled from the Human Rights First ICE Flight Monitor April 2026 Monthly Report. Split into two tiers:

- **Tier 1 — official ICE Air staging facilities** (named explicitly in the HRF report): Phoenix-Mesa Gateway (KIWA), Alexandria International (KAEX), El Paso International (KELP), Valley International Harlingen (KHRL)
- **Tier 2 — high-volume secondary hubs** by 2025 departure count and 2026 monthly consistency: Miami (KMIA), Jacksonville (KJAX), Houston Bush (KIAH), Newark (KEWR), Youngstown-Warren (KYNG), Boeing Field Seattle (KBFI), Kansas City (KMCI)

Each airport object includes ICAO code, city/state, 2025 departure count, and a contextual note. Hardcoded as a JS array to avoid CSV or API dependency.

Source: [Human Rights First ICE Flight Monitor](https://www.humanrightsfirst.org/ice-flight-monitor/)

**Experimental — real-time ICE Air flight positions**

Live aircraft positions via ADS-B transponder signals. 44 known ICE Air ICAO hex codes sourced from [deportationflights.com](https://deportationflights.com) / ADS-B Exchange. Implementation: single `fetch` to `api.adsb.lol/v2/icao/<comma-separated-codes>` every 60 seconds → `liveFlightLayer.clearLayers()` → redraw orange `L.divIcon` plane markers with `track`-based rotation. CORS blocks direct browser requests; a proxy (`corsproxy.io` for local testing, or a serverless function for production) is required. Not included in the submission.

---

## 2. Topic and geographic phenomena

**What:** The spatial distribution and scale of ICE civil immigration detention overnight — where people are held at night or after midnight, at what concentrations, and whether those concentrations fall in metropolitan areas (with potentially higher public visibility), or in rural and exurban locations where they are less visible.

**Where:** Continental United States. The map covers all 50 states but gives particular analytical weight to the contrast between metropolitan and non-metropolitan detention — a pattern legible only at a national scale.

**When:** Current. The facilities dataset covers active detention locations since January 1, 2025. Overnight population figures represent the most recent full year of reported data.

**Title:** ICE AT NIGHT

**Subtitle:** ICE Detentions — Before & After

**Key findings from the data:** 262 of 323 facilities active in both periods increased overnight population (81%). 212 facilities had no activity before Jan 20 — new sites activated post-inauguration. 40 facilities closed. Average per-facility conviction rate: 60% before → 38% after, as the detained population expanded.

**Thematic representation:**

- Proportional circles (`L.circleMarker`) sized by `avg_midnight_pop` using a square root scale with a 5px minimum radius (for better representation at high zoom levels). Larger circles indicate higher average overnight detention capacity. In before/after mode, radius is driven by `avg_midnight_before` or `avg_midnight_after` from the derived dataset
- Three-value color encoding by `cbsa_type`: metropolitan (`#38bdf8` sky blue) / micropolitan (`#a3e635` lime) / rural (`#f87171` muted red)
- `L.divIcon` plane markers (Lucide `plane` SVG, white stroke) for ICE Air departure airports, rendered in a dedicated `L.layerGroup`
- NASA VIIRS CityLights satellite imagery (2012) as primary basemap — nighttime lights as a spatial proxy for urban context and economic activity. Isolated in a custom Leaflet pane (`viirsPane`) with CSS filter `brightness(0.6) contrast(1.4)` to improve marker legibility without flattening the rural/urban light differential
- CartoDB Dark No Labels as secondary basemap, permanently visible underneath VIIRS. Provides street context at zoom levels above 8 where VIIRS tiles do not exist, and serves as the fallback view when the VIIRS layer is toggled off
- Cities above 100K: label-only reference layer for geographic orientation, using Carto DB Only Labels as layer.
- User-controlled basemap toggle (show/hide city lights) and before/after era toggle via fixed UI buttons

**Implemented UI:**

Dark glass morphism interface with VIIRS basemap at full U.S. extent on load, defaulting to after-Jan-20 mode. Bottom-right button stack: era toggle (before/after Jan '25), VIIRS city lights toggle (Lucide eye icon), nearest-facility geolocation. Bottom-left: zoom controls (`zoomControl: false` + `L.control.zoom({ position: 'bottomleft' })`); legend and info button shifted to `left: 60px` to clear zoom buttons. Info button is a plain anchor tag linking to this README. Filter panel (top-right): `cbsa_type` checkboxes + `field_office` dropdown. Popups include facility name, city/state, field office AOR, avg/peak overnight population, nights active, conviction rates before/after Jan '25 (Geist Mono), and CBSA type badge. Geolocation: `navigator.geolocation` → Turf.js `nearestPoint` → `map.flyTo` → `openPopup` on `moveend`.

---

## 3. Map objectives and user needs

**Why this map needs to be made**

While multiple dashboards and count maps about this topic have been created, there is no single publicly available visualization that focuses on the *overnight* detention patterns at the national scale against a nighttime lights context. My second goal is to make legible the degree to which detention has expanded into rural and exurban areas outside the reach of immigration legal services, a fact that has received attention in the media but that has, to the best of my knowledge, not been visualized through a map. The underlying data is public and verifiable — the argument is in the spatial pattern itself.

The VIIRS nighttime lights basemap is not purely aesthetic. In urban geography and remote sensing research, nighttime satellite imagery is an established proxy for urban activity, economic intensity, and institutional density. Mapping civil detention against it situates the carceral infrastructure inside the same spatial logic researchers use to read the distribution of work, capital, and care after dark. Facilities that appear in rural darkness are not legible in most news coverage or policy debate; placing them in that context makes visible something that statistical tables do not.

The airport layer extends this argument spatially: ICE Air departure hubs are the exit points of the detention infrastructure. Showing their location alongside detention facilities makes the logistics of removal legible as a domestic and international network, not a set of isolated incidents.

**Why I am the one designing this**

My research focuses on night geographies — the spatial distribution of labor, infrastructure, and inequality after dark. The "midnight population" field in this dataset is analytically aligned with the core questions of night studies: who is present in (which) space at night, under what conditions, and with what institutional visibility. The VIIRS basemap choice is theoretically motivated by my familiarity with nighttime remote sensing as a research instrument and to highlight the nocturnal framing of the research questions. This project is a direct application of that research perspective to a pressing public dataset.

**User personas and scenarios**

*Persona 1 — Investigative journalist*

Leila covers immigration enforcement for a regional newspaper. She has access to national reporting and ICE press releases but lacks spatial tools to situate her stories geographically. She needs to identify high-capacity facilities in her coverage area, understand their urban or rural context, and quickly extract accurate figures for publication.

Scenario: Leila opens the map and sees the national distribution immediately. She zooms to her state and uses the metro/rural filter to isolate micropolitan and rural facilities. She notices a cluster of high-capacity facilities in counties with no immigration legal aid organizations. She clicks several facility circles, reads the overnight population data and field office, and screenshots the map for her editor. The popup gives her the facility name and location without requiring additional database lookups. She toggles off city lights to see the street geography underneath high-capacity rural facilities.

*Persona 2 — Immigration legal services coordinator*

Carlos coordinates intake at a nonprofit immigration legal services organization. He tracks where clients are being held in order to schedule attorney visits and understand detention patterns within his organization's service area. He needs accurate, current facility locations and population figures, and he needs to understand which facilities are actively used for overnight detention versus brief processing stops.

Scenario: Carlos opens the map and uses the geolocation button to anchor it to his office location. The map highlights nearby facilities. He zooms to his AOR and clicks facilities with large circles, reading the overnight population and field office data to distinguish long-term detention sites from staging locations. He filters by his field office to see the full regional picture before a team meeting.

---

## 4. Technology stack

**Data processing:**
- Python 3.11 / pandas — column renaming, field selection, null coordinate removal, rounding, UTF-8 CSV export; `before_after.py` splits daily population dataset on Jan 20 2025, computes per-facility avg midnight population and criminal conviction rates for each period, exports `facilities_before_after.csv`
- QGIS 3.44.7 Solothurn — initial data inspection, coordinate verification, layer preview

**Data formats:**
- Facilities layer: UTF-8 CSV (`facilities_avg_conv_clean.csv`), loaded client-side with PapaParse
- Before/after comparison: UTF-8 CSV (`facilities_before_after.csv`), loaded as second PapaParse call, joined client-side on `facility_id`
- Field office AOR boundaries: GeoJSON polygon layer, loaded with `L.geoJSON()`
- Cities reference layer: originally GeoJSON, loaded via `fetch()` and filtered client-side by population threshold, later replaced by the Carto DB Dark Only Labels layer.
- Airport layer: hardcoded JS array — no file dependency

**JavaScript libraries:**
- [Leaflet 1.9.4](https://leafletjs.com/) — map rendering, custom panes, layer management, circle markers, `L.divIcon`, `L.layerGroup`, popups
- [PapaParse](https://www.papaparse.com/) — CSV parsing with typed columns (`dynamicTyping: true`); two separate calls, second re-renders layer on complete
- [Turf.js](https://turfjs.org/) — `nearestPoint` for geolocation → nearest facility lookup
- [Chroma.js](https://gka.github.io/chroma.js/) — loaded, under consideration for future use

**Basemap stack:**
- CartoDB Dark No Labels — permanent base, full zoom range (1–19). URL: `https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png`
- CartoDB Dark Only Labels – URL: `https://{s}.basemaps.cartocdn.com/{style}/{z}/{x}/{y}dark_only_labels.png`
- NASA VIIRS CityLights 2012, served via NASA GIBS WMTS tile endpoint — overlay layer, zoom 1–8, isolated in custom Leaflet pane `viirsPane`. CSS filter: `brightness(0.6) contrast(1.4)`. User-toggleable via fixed UI button.

**Design system:**
- Background: `#1a1a2e` / `rgba(27,27,45,0.28)` glass panels
- Accent: `#4f46e5` indigo borders / `#a78bfa` purple secondary
- Typography: Geist (body), Geist Mono (code/identifiers, popup conviction rate rows)
- Glass morphism: `backdrop-filter: blur(3px)`, `rgba(79,70,229,0.45)` border
- Leaflet popups harmonized with glass system: `rgba(27,27,45,0.45)` background, `backdrop-filter: blur(3px)`