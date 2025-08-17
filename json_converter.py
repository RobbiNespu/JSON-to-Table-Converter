#!/usr/bin/env python3
"""
JSON to Tabular Converter
A Python script to convert JSON files into tabular format and display them as tables.
"""

import json
import pandas as pd
from tabulate import tabulate
import argparse
import sys
from pathlib import Path
from typing import Union, Dict, List, Any
import flatten_json

def load_json_file(file_path: str) -> Union[Dict, List]:
    """Load and parse JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def flatten_nested_json(data: Any) -> List[Dict]:
    """Flatten nested JSON structures."""
    if isinstance(data, list):
        flattened_list = []
        for item in data:
            if isinstance(item, dict):
                flattened_list.append(flatten_json.flatten(item))
            else:
                flattened_list.append({"value": item})
        return flattened_list
    elif isinstance(data, dict):
        return [flatten_json.flatten(data)]
    else:
        return [{"value": data}]

def json_to_dataframe(data: Union[Dict, List]) -> pd.DataFrame:
    """Convert JSON data to pandas DataFrame."""

    # Handle different JSON structures
    if isinstance(data, list):
        if not data:
            return pd.DataFrame()

        # If list contains dictionaries, create DataFrame directly
        if all(isinstance(item, dict) for item in data):
            # Flatten nested dictionaries
            flattened_data = []
            for item in data:
                flattened_data.append(flatten_json.flatten(item))
            return pd.DataFrame(flattened_data)
        else:
            # Mixed types or simple values
            return pd.DataFrame(data, columns=["Value"])

    elif isinstance(data, dict):
        # Check if it's a nested structure that should be flattened
        flattened = flatten_json.flatten(data)

        # Convert to single-row DataFrame if it's a single object
        if len(flattened) == len(data):  # No nested structures
            return pd.DataFrame([data])
        else:
            # Flattened nested structure
            return pd.DataFrame([flattened])

    else:
        # Simple value
        return pd.DataFrame([{"Value": data}])

def display_table(df: pd.DataFrame, table_format: str = "grid", max_width: int = 100) -> None:
    """Display DataFrame as a formatted table."""
    if df.empty:
        print("No data to display.")
        return

    # Truncate long strings for better display
    df_display = df.copy()
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            df_display[col] = df_display[col].astype(str).apply(
                lambda x: x[:max_width] + "..." if len(x) > max_width else x
            )

    # Display table
    print(f"\nTable ({len(df)} rows, {len(df.columns)} columns):")
    print("=" * 50)
    print(tabulate(df_display, headers='keys', tablefmt=table_format, showindex=True))
    print("=" * 50)

def display_hierarchical_table(data: Any, table_format: str = "grid", max_width: int = 100, indent: int = 0) -> None:
    """Display JSON data in a hierarchical table format similar to the image."""
    prefix = "  " * indent
    
    if isinstance(data, dict):
        print(f"{prefix}┌─ Object ({len(data)} keys)")
        for i, (key, value) in enumerate(data.items()):
            is_last = i == len(data) - 1
            connector = "└─" if is_last else "├─"
            
            if isinstance(value, dict):
                print(f"{prefix}{connector} {key}: Object ({len(value)} keys)")
                display_hierarchical_table(value, table_format, max_width, indent + 2)
            elif isinstance(value, list):
                print(f"{prefix}{connector} {key}: Array ({len(value)} items)")
                display_hierarchical_table(value, table_format, max_width, indent + 2)
            else:
                print(f"{prefix}{connector} {key}: {value}")
                
    elif isinstance(data, list):
        if data and isinstance(data[0], dict):
            # Display as table for array of objects
            df = pd.DataFrame(data)
            df_display = df.copy()
            
            # Truncate long strings
            for col in df_display.columns:
                if df_display[col].dtype == 'object':
                    df_display[col] = df_display[col].astype(str).apply(
                        lambda x: x[:max_width] + "..." if len(x) > max_width else x
                    )
            
            # Add index column
            df_display.insert(0, 'Index', range(len(df_display)))
            
            print(f"{prefix}└─ Table:")
            table_str = tabulate(df_display, headers='keys', tablefmt=table_format, showindex=False)
            # Indent each line of the table
            for line in table_str.split('\n'):
                print(f"{prefix}   {line}")
        else:
            # Simple array
            print(f"{prefix}└─ Array ({len(data)} items)")
            for i, item in enumerate(data):
                is_last = i == len(data) - 1
                connector = "└─" if is_last else "├─"
                print(f"{prefix}   {connector} [{i}]: {item}")
    else:
        print(f"{prefix}└─ {data}")

def display_hierarchical_json(data: Any, table_format: str = "grid", max_width: int = 100) -> None:
    """Display JSON data in a hierarchical format with proper table formatting."""
    print("\nJSON Structure Display:")
    print("=" * 60)
    display_hierarchical_table(data, table_format, max_width)
    print("=" * 60)

def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to CSV file."""
    try:
        df.to_csv(output_path, index=False)
        print(f"\nData saved to: {output_path}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def analyze_structure(data: Any, indent: int = 0) -> None:
    """Analyze and display JSON structure."""
    prefix = "  " * indent

    if isinstance(data, dict):
        print(f"{prefix}Object ({len(data)} keys):")
        for key, value in data.items():
            print(f"{prefix}  - {key}: {type(value).__name__}")
            if isinstance(value, (dict, list)) and indent < 2:
                analyze_structure(value, indent + 2)
    elif isinstance(data, list):
        print(f"{prefix}Array ({len(data)} items):")
        if data:
            item_types = set(type(item).__name__ for item in data)
            print(f"{prefix}  Item types: {', '.join(item_types)}")
            if len(data) > 0 and isinstance(data[0], (dict, list)) and indent < 2:
                print(f"{prefix}  Sample item structure:")
                analyze_structure(data[0], indent + 2)
    else:
        print(f"{prefix}Value: {type(data).__name__}")

def main():
    parser = argparse.ArgumentParser(description="Convert JSON files to tabular format")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("-f", "--format", choices=["grid", "plain", "simple", "github", "fancy_grid"],
                       default="grid", help="Table format (default: grid)")
    parser.add_argument("-o", "--output", help="Output CSV file path (optional)")
    parser.add_argument("-w", "--width", type=int, default=50,
                       help="Maximum column width for display (default: 50)")
    parser.add_argument("-s", "--structure", action="store_true",
                       help="Show JSON structure analysis")
    parser.add_argument("-a", "--ascii", action="store_true",
                       help="Output table in ASCII format")
    parser.add_argument("--hierarchical", action="store_true",
                       help="Display JSON in hierarchical format with nested tables")

    args = parser.parse_args()

    # Verify file exists
    if not Path(args.json_file).exists():
        print(f"Error: File '{args.json_file}' does not exist.")
        sys.exit(1)

    # Load JSON data
    print(f"Loading JSON file: {args.json_file}")
    data = load_json_file(args.json_file)

    # Show structure analysis if requested
    if args.structure:
        print("\nJSON Structure Analysis:")
        print("-" * 30)
        analyze_structure(data)
        print()

    # Convert to DataFrame
    print("Converting to tabular format...")
    df = json_to_dataframe(data)

    # Display table
    table_format = "plain" if args.ascii else args.format
    
    if args.hierarchical:
        display_hierarchical_json(data, table_format, args.width)
    else:
        display_table(df, table_format, args.width)

    # Show basic statistics
    print(f"\nDataFrame Info:")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Data types: {df.dtypes.to_dict()}")

    # Save to CSV if requested
    if args.output:
        save_to_csv(df, args.output)

# Example usage function for testing
def example_usage():
    """Example of how to use the functions directly in code."""

    # Sample JSON data (like the one in your image)
    sample_data = {
        "Type": "IR",
        "WODetail": [
            {
                "QtyReceived": 10,
                "StorerKey": "ML3PL-PP129",
                "Sku": "978129244860",
                "ExternLineno": 202,
                "ExternReceiptKey": "ALRA20221111"
            },
            {
                "QtyReceived": 15,
                "StorerKey": "ML3PL-PP129",
                "Sku": "978129243103",
                "ExternLineno": 203,
                "ExternReceiptKey": "ALRA20221111"
            }
        ],
        "POIR": {
            "Suer2": 0,
            "ReceiptKey": "000001675",
            "ReceiptDate": "11/18/2022 14:37:31",
            "AsnDetail": [
                {
                    "Status": "AVL",
                    "QtyReceived": 10,
                    "StorerKey": "ML3PL-PP129",
                    "ToLoc": "STAGE",
                    "Suer1": 0,
                    "Suer2": 0,
                    "Suer3": "",
                    "Sku": "978129244860",
                    "ReturnType": 202,
                    "ExternLineno": 202,
                    "purchaseorderdocument": "",
                    "ExternReceiptKey": "WMS000001675"
                }
            ],
            "ExternReceiptKey": "ALRA20221111"
        }
    }

    print("Example Usage:")
    print("=" * 50)

    # Convert to DataFrame
    df = json_to_dataframe(sample_data)

    # Display regular table
    display_table(df, "grid", 30)

    # Show hierarchical display
    print("\nHierarchical Display:")
    display_hierarchical_json(sample_data, "grid", 30)

    # Show structure
    print("\nStructure Analysis:")
    analyze_structure(sample_data)

if __name__ == "__main__":
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        main()
    else:
        print("JSON to Table Converter")
        print("Usage: python json_converter.py <json_file> [options]")
        print("\nOptions:")
        print("  -f, --format       Table format (grid, plain, simple, github, fancy_grid)")
        print("  -a, --ascii        Output table in ASCII format")
        print("  --hierarchical     Display JSON in hierarchical format with nested tables")
        print("  -o, --output       Output CSV file path")
        print("  -w, --width        Maximum column width for display")
        print("  -s, --structure    Show JSON structure analysis")
        print("\nRunning example...")
        example_usage()
