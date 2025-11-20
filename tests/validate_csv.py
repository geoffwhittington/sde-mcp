#!/usr/bin/env python3
"""
Utility script to validate the prompts_tool_mapping.csv file.

Usage:
    python tests/validate_csv.py
    python tests/validate_csv.py --csv path/to/custom.csv
"""
import argparse
import csv
import sys
from pathlib import Path


def validate_csv(csv_path: Path) -> tuple[bool, list[str]]:
    """
    Validate CSV structure and content.
    
    Returns:
        (is_valid, errors) - whether CSV is valid and list of errors
    """
    errors = []
    
    if not csv_path.exists():
        return False, [f"CSV file not found: {csv_path}"]
    
    required_columns = ['prompt', 'expected_tools']
    optional_columns = ['category', 'description', 'priority']
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            
            if not columns:
                return False, ["CSV file is empty or has no header row"]
            
            # Check required columns
            for col in required_columns:
                if col not in columns:
                    errors.append(f"Missing required column: {col}")
            
            # Validate rows
            for i, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                if not row.get('prompt', '').strip():
                    errors.append(f"Row {i}: prompt is empty")
                
                expected_tools = row.get('expected_tools', '').strip()
                if not expected_tools:
                    errors.append(f"Row {i}: expected_tools is empty")
                else:
                    # Validate tool names (basic check - no spaces, reasonable format)
                    tools = [t.strip() for t in expected_tools.split(',')]
                    for tool in tools:
                        if ' ' in tool and not tool.startswith('"'):
                            errors.append(f"Row {i}: tool '{tool}' contains spaces (use quotes if intentional)")
                
                # Validate priority if present
                priority = row.get('priority', '').strip().lower()
                if priority and priority not in ['high', 'medium', 'low', '']:
                    errors.append(f"Row {i}: invalid priority '{priority}' (must be high/medium/low)")
            
            # Count rows
            f.seek(0)
            row_count = sum(1 for _ in csv.DictReader(f))
            if row_count == 0:
                errors.append("CSV file has no data rows")
    
    except csv.Error as e:
        return False, [f"CSV parsing error: {e}"]
    except Exception as e:
        return False, [f"Error reading CSV: {e}"]
    
    return len(errors) == 0, errors


def print_summary(csv_path: Path):
    """Print a summary of the CSV file"""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        print(f"\nCSV Summary: {csv_path.name}")
        print(f"  Total test cases: {len(rows)}")
        
        # Count by category
        categories = {}
        priorities = {}
        for row in rows:
            cat = row.get('category', 'uncategorized')
            categories[cat] = categories.get(cat, 0) + 1
            
            prio = row.get('priority', 'medium')
            priorities[prio] = priorities.get(prio, 0) + 1
        
        if categories:
            print(f"\n  By category:")
            for cat, count in sorted(categories.items()):
                print(f"    {cat}: {count}")
        
        if priorities:
            print(f"\n  By priority:")
            for prio, count in sorted(priorities.items()):
                print(f"    {prio}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Validate prompts_tool_mapping.csv")
    parser.add_argument(
        '--csv',
        type=Path,
        default=None,
        help='Path to CSV file (default: tests/prompts_tool_mapping.csv)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Print summary statistics'
    )
    
    args = parser.parse_args()
    
    if args.csv:
        csv_path = args.csv
    else:
        csv_path = Path(__file__).parent / "prompts_tool_mapping.csv"
    
    is_valid, errors = validate_csv(csv_path)
    
    if args.summary:
        print_summary(csv_path)
    
    if not is_valid:
        print(f"\n❌ CSV validation failed:\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"\n✓ CSV file is valid: {csv_path}")
        if args.summary:
            print()
        sys.exit(0)


if __name__ == "__main__":
    main()

