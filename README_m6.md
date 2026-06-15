# N/ICE SLEEP
### Overnight civil immigration detention in the United States

An interactive web map of ICE civil immigration detention facilities across the U.S., visualized against NASA VIIRS nighttime satellite imagery. The map explores where people are held after midnight, at what concentrations, and in what urban or rural context — asking whether and how the geography of overnight detention intersects with the geography of artificial light at night.

---

## 1. Data source

**Primary dataset — ICE detention facilities**

Government data provided by ICE in response to FOIA requests, processed by the [Deportation Data Project](https://deportationdata.org) at UCLA, and analyzed by the author. The dataset records every facility in which at least one civil immigration detainee was held since January 1, 2025. It includes dedicated ICE facilities, intergovernmental service agreement (IGSA) facilities, private contractor-run facilities, and short-hold locations such as hospitals and staging areas. Facility coordinates were geocoded using ArcGIS and Google Maps APIs and manually verified.

Interactive data explorer and download: [ice-detention-facilities.apps.deportationdata.org](https://ice-detention-facilities.apps.deportationdata.org/)

The dataset was downloaded as XLSX, trimmed to 13 columns, and cleaned using Python/pandas. Facilities with missing coordinates were dropped prior to export.

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

**Sample data (3 rows):**

```
facility_id,name,city,state,county,lat,lon,field_office,cbsa_type,cbsa_name,days_midnight,avg_midnight_pop,max_midnight_pop
ABRXSPA,Abraxas Academy,Morgantown,PA,Berks,40.19,-75.92,Philadelphia,Metro,"Reading, PA",43,0.6,5
ADAMSMS,Adams County Correctional Center,Natchez,MS,Adams,31.56,-91.22,New Orleans,Micro,"Natchez, MS-LA",365,2158.8,2563
```

**Secondary dataset — ICE field office areas of responsibility (AOR)**

Polygon boundaries for 24 ICE ERO field offices, from the same source. Used as a context and filter layer. Download: [ice-offices.apps.deportationdata.org](https://ice-offices.apps.deportationdata.org/)

**Reference layer — U.S. cities**

Natural Earth `ne_10m_populated_places`, filtered client-side to U.S. cities with population ≥ 100,000. Source: [github.com/nvkelso/natural-earth-vector](https://github.com/nvkelso/natural-earth-vector)

**Planned addition**

Major airport locations for ICE air deportation hubs, via OurAirports or FAA data. Planned for a later development module. Specific flights operated by carriers known to lease airplanes for this purpose could be fetched via https://api.developer.iata.org/collection/open-air or through a free API key that can be obtained from https://aviationstack.com/.

## 2. Topic and geographic phenomena

**What:** The spatial distribution and scale of ICE civil immigration detention overnight — where people are held at night or after midnight, at what concentrations, and whether those concentrations fall in metropolitan areas (with potentially higher public visibility), or in rural and exurban locations where they are less visible.

**Where:** Continental United States. The map covers all 50 states but gives particular analytical weight to the contrast between metropolitan and non-metropolitan detention — a pattern legible only at a national scale.

**When:** Current. The facilities dataset covers active detention locations since January 1, 2025. Overnight population figures represent the most recent full year of reported data. A separate daily population time series (October 2022–present) is available and planned for a future temporal feature (a time comparison through an aggregate figure per year).

**Title:** N/ICE SLEEP

**Subtitle:** Overnight immigration detention in the United States

**Thematic representation:**

- Proportional circles (`L.circleMarker`) sized by `avg_midnight_pop` — larger circles indicate higher average overnight detention capacity
- Three-value color encoding by `cbsa_type`: metropolitan / micropolitan / rural
- NASA VIIRS CityLights satellite imagery (2012) as basemap — nighttime lights as a spatial proxy for urban intensity, economic activity, and institutional visibility
- Cities above 100K: used for reference and for better orientation -> label-only layer

**Anticipated UI:**

Dark interface with the VIIRS basemap loaded at full U.S. extent on load. All facility circles rendered immediately. A sidebar or overlay panel shows map title, subtitle, and legend. A filter control allows users to toggle visibility by `cbsa_type` or `field_office` AOR. Clicking a circle opens a popup with facility name, location, overnight population figures, and field office. A geolocation button identifies the nearest ICE facility to the user's position. Code comments will mark a planned time slider position for future temporal exploration.

---

## 3. Map objectives and user needs

**Why this map needs to be made**

While multiple dashboards and count maps about this topic have been created, there is no single publicly available visualization that focuses on the *overnight* detention patterns at the national scale against a nighttime lights context. My second goal is to make legible the degree to which detention has expanded into rural and exurban areas outside the reach of immigration legal services, a fact that has received attention in the media but that has, to the best of my knowledge, not been visualized through a map. The underlying data is public and verifiable — the argument is in the spatial pattern itself.

The VIIRS nighttime lights basemap is not purely aesthetic. In urban geography and remote sensing research, nighttime satellite imagery is an established proxy for urban activity, economic intensity, and institutional density. Mapping civil detention against it situates the carceral infrastructure inside the same spatial logic researchers use to read the distribution of work, capital, and care after dark. Facilities that appear in rural darkness are not legible in most news coverage or policy debate; placing them in that context makes visible something that statistical tables do not.

**Why I am the one designing this**

My research focuses on night geographies — the spatial distribution of labor, infrastructure, and inequality after dark. The "midnight population" field in this dataset is analytically aligned with the core questions of night studies: who is present in space at night, under what conditions, and with what institutional visibility. The VIIRS basemap choice is theoretically motivated by my familiarity with nighttime remote sensing as a research instrument and to highlight the nocturnal framing of the research questions. This project is a direct application of that research perspective to a pressing public dataset.

**User personas and scenarios**

*Persona 1 — Investigative journalist*

Leila covers immigration enforcement for a regional newspaper. She has access to national reporting and ICE press releases but lacks spatial tools to situate her stories geographically. She needs to identify high-capacity facilities in her coverage area, understand their urban or rural context, and quickly extract accurate figures for publication.

Scenario: Leila opens the map and sees the national distribution immediately. She zooms to her state and uses the metro/rural filter to isolate micropolitan and rural facilities. She notices a cluster of high-capacity facilities in counties with no immigration legal aid organizations. She clicks several facility circles, reads the overnight population data and field office, and screenshots the map for her editor. The popup gives her the facility name and location without requiring additional database lookups.

*Persona 2 — Immigration legal services coordinator*

Carlos coordinates intake at a nonprofit immigration legal services organization. He tracks where clients are being held in order to schedule attorney visits and understand detention patterns within his organization's service area. He needs accurate, current facility locations and population figures, and he needs to understand which facilities are actively used for overnight detention versus brief processing stops.

Scenario: Carlos opens the map and uses the geolocation button to anchor it to his office location. The map highlights nearby facilities. He zooms to his AOR and clicks facilities with large circles, reading the overnight population and field office data to distinguish long-term detention sites from staging locations. He filters by his field office to see the full regional picture before a team planning meeting.

---

## 4. Anticipated technology stack

**Data processing:**
- Python 3.11 / pandas — column renaming, field selection, null coordinate removal, rounding, UTF-8 CSV export
- QGIS 3.x — initial data inspection, coordinate verification, layer preview

**Data formats:**
- Facilities layer: UTF-8 CSV, loaded client-side with PapaParse
- Field office AOR boundaries: GeoJSON polygon layer, loaded with `L.geoJSON()`
- Cities reference layer: GeoJSON, loaded via `fetch()` and filtered client-side by population threshold

**JavaScript libraries:**
- [Leaflet 1.9.4](https://leafletjs.com/) — map rendering, layer management, circle markers, popups
- [PapaParse](https://www.papaparse.com/) — CSV parsing with typed columns
- [Chroma.js](https://gka.github.io/chroma.js/) — categorical color scale for `cbsa_type`
- [Turf.js](https://turfjs.org/) — nearest-facility calculation from geolocated user position
- [Simple Statistics](https://simplestatistics.org/) — natural breaks classification for proportional symbol scaling (under consideration)

**Basemap:**
- NASA VIIRS CityLights 2012, served via NASA GIBS WMTS tile endpoint
