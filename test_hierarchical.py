#!/usr/bin/env python3
"""
Test script to demonstrate hierarchical JSON display
"""

import json
from json_converter import display_hierarchical_json, load_json_file

# Load the sample data
data = load_json_file('data.json')

print("Testing Hierarchical Display:")
print("=" * 60)

# Test with grid format
display_hierarchical_json(data, "grid", 50)

print("\n" + "=" * 60)
print("Testing with ASCII format:")
display_hierarchical_json(data, "plain", 50)
