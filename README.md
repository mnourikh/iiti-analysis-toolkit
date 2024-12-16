
# IITI Analysis Toolkit (HS)

This toolkit provides methods for analyzing Intra-Industry Trade (IITI) and related indices, including:
- **Weighted Intra-Industry Trade Index (WIITI)**
- **Marginal Intra-Industry Trade Index (MIITI)**

## Features
1. Aggregates trade data by HS code levels (e.g., 2-digit, 4-digit).
2. Computes IITI, WIITI, and MIITI for export and import datasets.
3. Saves results to Excel files, including:
   - Summary results per year (IITI, WIITI, MIITI).
   - Top-ranked WIITI results for each year.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Prepare your export and import data in Parquet format.
2. Update file paths in `iiti_analysis_toolkit.py`.
3. Run the script:
   ```bash
   python iiti_analysis_toolkit.py
   ```

## Requirements
- Python 3.7 or later
- Libraries: pandas, numpy, os, openpyxl

## License
This project is licensed under the MIT License.
