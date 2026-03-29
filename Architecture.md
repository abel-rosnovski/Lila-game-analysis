# Architecture Overview

## Tech Choices

| Component       | Choice          | Why                                       |
| --------------- | --------------- | ----------------------------------------- |
| Frontend        | Streamlit       | Fast UI development, no frontend overhead |
| Data Processing | Pandas          | Efficient tabular transformations         |
| Visualization   | Matplotlib      | Flexible and lightweight plotting         |
| Deployment      | Streamlit Cloud | Simple hosting with quick iteration       |

---

##  Data Flow

1. Raw parquet files contain player movement and event logs
2. Data is preprocessed into an optimized dataset:

   * Movement sampled per match
   * All key events retained
3. Streamlit app loads the optimized dataset
4. Filters (map, date, match) are applied
5. Coordinates are transformed into minimap space
6. Data is visualized on top of map images

---

##  Coordinate Mapping

Game world coordinates (x, z) do not directly map to minimap pixels.

### Approach:

1. Define map-specific parameters:

   * Origin (bottom-left reference)
   * Scale factor

2. Normalize coordinates:

   * Convert world position → relative position

3. Transform to pixel space:

   * Scale to 1024 × 1024 minimap
   * Flip Y-axis to match image coordinate system

### Formula:

* u = (x - origin_x) / scale
* v = (z - origin_z) / scale
* pixel_x = u * 1024
* pixel_y = (1 - v) * 1024

---

##  Assumptions

* Numeric user_ids represent bots
* Map scale approximated based on visual alignment
* Movement sampling preserves spatial distribution

---

##  Tradeoffs

| Decision          | Alternative       | Tradeoff                            |
| ----------------- | ----------------- | ----------------------------------- |
| Optimized dataset | Full dataset      | Faster performance vs full fidelity |
| Sampling movement | Full logs         | Reduced size vs minor detail loss   |
| Static maps       | Dynamic rendering | Simplicity vs flexibility           |

---

##  Design Philosophy

The system prioritizes:

* Interpretability
* Performance
* Interactive exploration

Over:

* Perfect data fidelity
