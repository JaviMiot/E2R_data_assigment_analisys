# E2R Accessibility Analysis

This repository contains student assignment submissions for an ICT Accessibility course focusing on E2R (Easy-to-Read) analysis and adaptation.

## Directory Structure

- `data/`: Consolidated CSV output files.
- `logs/`: Processing reports and logs.
- `notebooks/`: Jupyter notebooks for data analysis.
- `practices/`: Student submission directories.
- `scripts/`: Python automation scripts for data extraction and cleaning.

## Setup

1. Create a virtual environment: `python3 -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install openpyxl xlrd pandas numpy jupyter`

## Usage

### 1. Data Consolidation
Extract data from student Excel files into a single CSV:
```bash
python3 scripts/part2/consolidate_part2_to_csv.py
python3 scripts/part3/consolidate_part3_to_csv.py
```

### 2. Data Cleaning (Part II)
Standardize the consolidated data:
```bash
python3 scripts/part2/clean_part2_data.py
```

### 3. Dataset Preparation (Part III)
Prepare the Part III dataset for analysis:
```bash
python3 scripts/part3/prepare_part3_analysis_dataset.py
```

### 4. Analysis
Run the Jupyter notebooks for detailed analysis:
```bash
jupyter notebook notebooks/part2_e2r_analysis.ipynb
jupyter notebook notebooks/part3_e2r_analysis.ipynb
```


