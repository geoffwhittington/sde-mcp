#!/usr/bin/env python3
"""
Show which tools are tested in the integration test suite.

This script analyzes prompts_tool_mapping.csv and shows:
- Which tools are tested
- How many test cases cover each tool
- Test coverage by category
- Which tools are NOT tested
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path
import sys

# All available tools in the server (from README and codebase)
ALL_TOOLS = {
    # Projects
    'list_projects', 'get_project', 'create_project', 'create_project_from_code',
    'update_project', 'delete_project', 'list_profiles',
    # Applications
    'list_applications', 'get_application', 'create_application', 'update_application',
    # Surveys
    'get_project_survey', 'get_survey_answers_for_project', 'update_project_survey',
    'find_survey_answers', 'set_project_survey_by_text', 'add_survey_answers_by_text',
    'remove_survey_answers_by_text', 'commit_survey_draft',
    # Countermeasures
    'list_countermeasures', 'get_countermeasure', 'update_countermeasure', 'add_countermeasure_note',
    # Users
    'list_users', 'get_user', 'get_current_user',
    # Business Units
    'list_business_units', 'get_business_unit',
    # Scans
    'list_scan_connections', 'scan_repository', 'get_scan_status', 'list_scans',
    # Reports
    'list_advanced_reports', 'get_advanced_report', 'run_advanced_report',
    'create_advanced_report', 'execute_cube_query',
    # Diagrams
    'list_project_diagrams', 'get_diagram', 'create_diagram', 'update_diagram', 'delete_diagram',
    # Generic
    'test_connection', 'api_request',
}


def analyze_tests():
    """Analyze the CSV file and show test coverage."""
    csv_path = Path(__file__).parent / "prompts_tool_mapping.csv"
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found", file=sys.stderr)
        sys.exit(1)
    
    tools_tested = Counter()
    tools_by_category = defaultdict(list)
    total_tests = 0
    tests_by_priority = Counter()
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_tests += 1
            expected_tools = [t.strip() for t in row['expected_tools'].split(',')]
            category = row.get('category', 'uncategorized')
            priority = row.get('priority', 'medium')
            
            tests_by_priority[priority] += 1
            
            for tool in expected_tools:
                tools_tested[tool] += 1
                if tool not in tools_by_category[category]:
                    tools_by_category[category].append(tool)
    
    tested_tools_set = set(tools_tested.keys())
    untested_tools = sorted(ALL_TOOLS - tested_tools_set)
    
    print("=" * 70)
    print("Integration Test Coverage Summary")
    print("=" * 70)
    print(f"\nTotal test cases: {total_tests}")
    print(f"Total unique tools tested: {len(tools_tested)}")
    print(f"Total tools available: {len(ALL_TOOLS)}")
    print(f"Coverage: {len(tools_tested)}/{len(ALL_TOOLS)} ({100*len(tools_tested)/len(ALL_TOOLS):.1f}%)")
    
    print(f"\nTests by priority:")
    for priority in ['high', 'medium', 'low']:
        count = tests_by_priority.get(priority, 0)
        if count > 0:
            print(f"  {priority:10s}: {count:2d} test(s)")
    
    print(f"\nTools tested (with test count):")
    print("-" * 70)
    for tool, count in sorted(tools_tested.items()):
        print(f"  {tool:45s} {count:2d} test(s)")
    
    if untested_tools:
        print(f"\n⚠️  Tools NOT tested ({len(untested_tools)}):")
        print("-" * 70)
        for tool in untested_tools:
            print(f"  {tool}")
    
    print(f"\nTools by category:")
    print("-" * 70)
    for category in sorted(tools_by_category.keys()):
        tools = sorted(tools_by_category[category])
        print(f"  {category:20s}: {', '.join(tools)}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    analyze_tests()

