#!/usr/bin/env python3
"""
Pipeline to analyze synthetic patient data and find top 5 most common medical conditions.

Loads patients.csv, conditions.csv, and encounters.csv, cleans the data,
and calculates the most frequently occurring conditions.
"""

import csv
import sys
from pathlib import Path
from collections import Counter


def load_csv(filepath):
    """Load a CSV file and return list of dictionaries."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        print(f"✓ Loaded {len(data)} records from {filepath.name}")
        return data
    except FileNotFoundError:
        print(f"✗ Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading {filepath}: {e}", file=sys.stderr)
        sys.exit(1)


def clean_data(data):
    """Clean data by stripping whitespace from all values."""
    cleaned = []
    for row in data:
        cleaned_row = {k: v.strip() if v else '' for k, v in row.items()}
        cleaned.append(cleaned_row)
    return cleaned


def analyze_top_conditions(conditions_data, top_n=5):
    """Analyze conditions and return top N most common."""
    descriptions = [
        row['DESCRIPTION'] 
        for row in conditions_data 
        if row.get('DESCRIPTION')
    ]
    
    condition_counts = Counter(descriptions)
    
    top_conditions = condition_counts.most_common(top_n)
    
    return top_conditions, len(descriptions)


def main():
    """Main pipeline execution."""
    print("=" * 70)
    print("SYNTHETIC PATIENT DATA ANALYSIS PIPELINE")
    print("=" * 70)
    print()
    
    data_dir = Path(__file__).parent / 'record' / 'set100' / 'csv'
    patients_file = data_dir / 'patients.csv'
    conditions_file = data_dir / 'conditions.csv'
    encounters_file = data_dir / 'encounters.csv'
    
    print("Loading CSV files...")
    patients = load_csv(patients_file)
    conditions = load_csv(conditions_file)
    encounters = load_csv(encounters_file)
    print()
    
    print("Cleaning data...")
    patients = clean_data(patients)
    conditions = clean_data(conditions)
    encounters = clean_data(encounters)
    print("✓ Data cleaned (whitespace stripped, empty values handled)")
    print()
    
    print("Analyzing top 5 most common medical conditions...")
    top_conditions, total_conditions = analyze_top_conditions(conditions, top_n=5)
    print()
    
    print("=" * 70)
    print("RESULTS: TOP 5 MOST COMMON MEDICAL CONDITIONS")
    print("=" * 70)
    print(f"Total condition records analyzed: {total_conditions}")
    print()
    
    for rank, (condition, count) in enumerate(top_conditions, 1):
        percentage = (count / total_conditions) * 100
        print(f"{rank}. {condition}")
        print(f"   Count: {count} ({percentage:.1f}% of all conditions)")
        print()
    
    print("=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
