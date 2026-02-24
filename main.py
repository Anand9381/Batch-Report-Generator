import argparse
import sys
import os
import pandas as pd
from report_service import ReportService

def main():
    parser = argparse.ArgumentParser(description="Batch Report Generator")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input directory")
    parser.add_argument("--output", "-o", type=str, required=True, help="Output directory")
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
        
    try:
        service = ReportService(input_dir, output_dir)
        service.load_data()
        service.clean_data()
        service.generate_reports()
        print("\nBatch report generation completed successfully.")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
