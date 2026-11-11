# LAB 7: Fuzzing for Input Validation Bugs

**Course:** Software Engineering Lab  
**Student SRN:** PES1UG24AM106  
**Topic:** Property-Based Fuzz Testing with Hypothesis  

---

## Overview

In this lab, we use **Hypothesis** to perform property-based fuzz testing on the ride share fare calculation module (`ride_share_fare.py` / `processor.py`). Fuzzing generates randomized, malformed, and edge-case inputs to automatically discover unhandled crashes, which are then defensively remediated.

## Deliverables in this Folder

1. **`LAB7_Fuzzing_PES1UG24AM106.pdf` / `Lab_7_Report.pdf`**: Complete lab report document containing terminal screenshots and vulnerability analysis.
2. **`ride_share_fare.py` & `processor.py`**: Fixed and defensively hardened application scripts.
3. **`test_ride_share_fare.py` & `test_processor.py`**: Hypothesis fuzz testing suites asserting crash immunity across random Unicode strings and null inputs.
4. **`screenshots/`**: High-resolution terminal capture images for each step.

---

## How to Run

### 1. Install Dependencies
```bash
pip install hypothesis pytest
```

### 2. Run Application
```bash
python ride_share_fare.py
```

### 3. Run Hypothesis Fuzz Tests
```bash
pytest test_ride_share_fare.py
# or
pytest test_processor.py
```
*(All 3 tests pass 100% across generated fuzz inputs)*
