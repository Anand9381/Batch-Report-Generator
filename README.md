# Batch Report Generator

A Python project that processes raw student data (CSV files) and generates clean, structured reports using Pandas and OOP principles.

## Features
- **Data Cleaning**: Handles missing values (fills with defaults), removes duplicates, and ensures correct data types.
- **Reporting**:
  - Generates a per-student summary CSV (`output/report.csv`).
  - Generates an overall batch metrics JSON (`output/summary.json`).
- **Robustness**: Gracefully handles missing input files and errors.

## Project Structure
```
Batch Report Generator/
├── input_data/          # Contains raw CSV files
│   ├── students.csv
│   └── attendance.csv
├── output/              # Generated reports (created automatically)
│   ├── report.csv
│   └── summary.json
├── main.py              # Entry point script
├── report_service.py    # Business logic and ReportService class
└── README.md            # Project documentation
```

## How to Run

1. **Install Dependencies** (if needed):
   This project requires `pandas`.
   ```bash
   pip install pandas
   ```

2. **Execute the Script**:
   Run the `main.py` script specifying the input and output directories:
   ```bash
   python main.py --input input_data --output output
   ```

   **Short command:**
   ```bash
   python main.py -i input_data -o output
   ```

## Output Files

1. **`output/report.csv`**:
   - Contains a list of students with their ID, Name, Attendance %, Average Marks, and Status (PASS/FAIL).
   - PASS critera: Average Marks >= 40.

2. **`output/summary.json`**:
   - Contains overall statistics for the batch:
     - Total number of students
     - Average attendance and marks
     - Count of passed and failed students
     - List of top 3 students by marks
## GitHub Repository Link
```bash
  https://github.com/Anand9381/Batch-Report-Generator.git
   ```
