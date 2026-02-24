import pandas as pd
import json
import os
import sys

class ReportService:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.students_df = None
        self.attendance_df = None
        self.merged_df = None

    def load_data(self):
        """Loads data from CSV files in the input directory."""
        students_path = os.path.join(self.input_dir, 'students.csv')
        attendance_path = os.path.join(self.input_dir, 'attendance.csv')

        if not os.path.exists(students_path):
            raise FileNotFoundError(f"Missing file: {students_path}")
        if not os.path.exists(attendance_path):
            raise FileNotFoundError(f"Missing file: {attendance_path}")

        try:
            self.students_df = pd.read_csv(students_path)
            self.attendance_df = pd.read_csv(attendance_path)
            print("Data loaded successfully.")
        except Exception as e:
            raise Exception(f"Error reading CSV files: {e}")

    def clean_data(self):
        """Cleans the data by handling missing values and duplicates."""
        if self.students_df is None or self.attendance_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # 1. Handle Missing Values & Types
        self.students_df['score'] = pd.to_numeric(self.students_df['score'], errors='coerce').fillna(0)
        self.attendance_df['attendance_percent'] = pd.to_numeric(self.attendance_df['attendance_percent'], errors='coerce').fillna(0)

        # 2. Handle Duplicates
        # If student appears multiple times in students.csv (e.g. daily scores), average them.
        # But if it's duplicate student records, we might want the latest or mean.
        # Assuming one row per student in final report, we group by student_id.
        
        # Clean names: take the first non-null name
        # We fill NaN first to key aggregation working
        self.students_df['name'] = self.students_df['name'].fillna('Unknown')
        
        # Aggregate students: mean score, first name
        students_agg = self.students_df.groupby('student_id').agg({
            'name': 'first',
            'score': 'mean'
        }).reset_index()

        # Aggregate attendance: mean percent
        attendance_agg = self.attendance_df.groupby('student_id').agg({
            'attendance_percent': 'mean'
        }).reset_index()

        # 3. Merge DataFrames
        self.merged_df = pd.merge(students_agg, attendance_agg, on='student_id', how='inner')
        self.merged_df['score'] = self.merged_df['score'].round(2)
        self.merged_df['attendance_percent'] = self.merged_df['attendance_percent'].round(2)

        print("Data cleaning complete.")

    def generate_reports(self):
        """Generates the required report files."""
        if self.merged_df is None:
            raise ValueError("Data not processed. Call clean_data() first.")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # --- Report 1: Student Summary (CSV) ---
        # Columns: studentId, name, attendancePercent, avgMarks, status
        report_df = self.merged_df.copy()
        report_df.rename(columns={'student_id': 'studentId', 'score': 'avgMarks', 'attendance_percent': 'attendancePercent'}, inplace=True)
        
        # Calculate Status (PASS if avgMarks >= 40)
        report_df['status'] = report_df['avgMarks'].apply(lambda x: 'PASS' if x >= 40 else 'FAIL')

        # Select columns
        report_df = report_df[['studentId', 'name', 'attendancePercent', 'avgMarks', 'status']]
        
        csv_path = os.path.join(self.output_dir, 'report.csv')
        report_df.to_csv(csv_path, index=False)
        print(f"Report generated: {csv_path}")

        # --- Report 2: Batch Summary (JSON) ---
        # Keys: totalStudents, avgAttendance, avgMarks, passCount, failCount, top3Students
        total_students = len(report_df)
        avg_attendance = report_df['attendancePercent'].mean()
        avg_marks = report_df['avgMarks'].mean()
        pass_count = len(report_df[report_df['status'] == 'PASS'])
        fail_count = len(report_df[report_df['status'] == 'FAIL'])
        
        # Top 3 Students
        top_students_df = report_df.nlargest(3, 'avgMarks')[['studentId', 'name', 'avgMarks']]
        top_3 = top_students_df.to_dict(orient='records')
        
        # Ensure native Python types for JSON serialization
        summary_data = {
            "totalStudents": int(total_students),
            "avgAttendance": float(round(avg_attendance, 2)) if not pd.isna(avg_attendance) else 0.0,
            "avgMarks": float(round(avg_marks, 2)) if not pd.isna(avg_marks) else 0.0,
            "passCount": int(pass_count),
            "failCount": int(fail_count),
            "top3Students": top_3
        }

        json_path = os.path.join(self.output_dir, 'summary.json')
        with open(json_path, 'w') as f:
            json.dump(summary_data, f, indent=4)
        print(f"Summary generated: {json_path}")
