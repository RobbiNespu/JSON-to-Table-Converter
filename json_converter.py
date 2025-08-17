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
import re

# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'
    BG_GRAY = '\033[100m'

def is_color_supported() -> bool:
    """Check if terminal supports color output."""
    import os
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty() and os.environ.get('TERM') != 'dumb'

def colorize(text: str, color: str, enabled: bool = True) -> str:
    """Add color to text if color output is enabled."""
    if not enabled or not is_color_supported():
        return text
    return f"{color}{text}{Colors.END}"

def highlight_value(value: Any, enabled: bool = True) -> str:
    """Highlight different types of values with colors."""
    if not enabled:
        return str(value)
    
    value_str = str(value)
    
    # Numbers
    if isinstance(value, (int, float)):
        return colorize(value_str, Colors.CYAN)
    
    # Strings that look like dates
    if isinstance(value, str) and re.match(r'\d{1,2}/\d{1,2}/\d{4}', value_str):
        return colorize(value_str, Colors.YELLOW)
    
    # Strings that look like keys/IDs
    if isinstance(value, str) and re.match(r'^[A-Z0-9_-]+$', value_str):
        return colorize(value_str, Colors.GREEN)
    
    # Empty values
    if value_str in ['', 'null', 'None']:
        return colorize(value_str, Colors.RED)
    
    # Default string color
    return colorize(value_str, Colors.BLUE)

def colorize_table(table_str: str, enabled: bool = True) -> str:
    """Add colors to table output."""
    if not enabled:
        return table_str
    
    lines = table_str.split('\n')
    colored_lines = []
    
    for i, line in enumerate(lines):
        if i == 0:  # Header
            colored_lines.append(colorize(line, Colors.BOLD + Colors.BG_GRAY))
        elif '|' in line and not line.startswith('+') and not line.startswith('='):
            # Data rows - colorize values
            parts = line.split('|')
            colored_parts = []
            for j, part in enumerate(parts):
                if j == 0:  # Index column
                    colored_parts.append(colorize(part.strip(), Colors.YELLOW))
                else:
                    # Try to extract and colorize the value
                    value = part.strip()
                    if value and not value.startswith('-'):
                        colored_parts.append(highlight_value(value))
                    else:
                        colored_parts.append(part)
            colored_lines.append('|'.join(colored_parts))
        else:
            # Separator lines
            colored_lines.append(colorize(line, Colors.GRAY if hasattr(Colors, 'GRAY') else ''))
    
    return '\n'.join(colored_lines)

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

def display_table(df: pd.DataFrame, table_format: str = "grid", max_width: int = 100, color_enabled: bool = True) -> None:
    """Display DataFrame as a formatted table."""
    if df.empty:
        print(colorize("No data to display.", Colors.RED, color_enabled))
        return

    # Truncate long strings for better display
    df_display = df.copy()
    for col in df_display.columns:
        if df_display[col].dtype == 'object':
            df_display[col] = df_display[col].astype(str).apply(
                lambda x: x[:max_width] + "..." if len(x) > max_width else x
            )

    # Display table
    table_info = f"\nTable ({len(df)} rows, {len(df.columns)} columns):"
    print(colorize(table_info, Colors.HEADER, color_enabled))
    print(colorize("=" * 50, Colors.BOLD, color_enabled))
    
    table_str = tabulate(df_display, headers='keys', tablefmt=table_format, showindex=True)
    if color_enabled and table_format in ["plain", "simple"]:
        table_str = colorize_table(table_str, color_enabled)
    
    print(table_str)
    print(colorize("=" * 50, Colors.BOLD, color_enabled))

def display_hierarchical_table(data: Any, table_format: str = "grid", max_width: int = 100, indent: int = 0, color_enabled: bool = True) -> None:
    """Display JSON data in a hierarchical table format similar to the image."""
    prefix = "  " * indent
    
    if isinstance(data, dict):
        print(colorize(f"{prefix}┌─ Object ({len(data)} keys)", Colors.BOLD, color_enabled))
        for i, (key, value) in enumerate(data.items()):
            is_last = i == len(data) - 1
            connector = "└─" if is_last else "├─"
            
            if isinstance(value, dict):
                print(colorize(f"{prefix}{connector} {key}: ", Colors.GREEN, color_enabled) + 
                      colorize(f"Object ({len(value)} keys)", Colors.CYAN, color_enabled))
                display_hierarchical_table(value, table_format, max_width, indent + 2, color_enabled)
            elif isinstance(value, list):
                print(colorize(f"{prefix}{connector} {key}: ", Colors.GREEN, color_enabled) + 
                      colorize(f"Array ({len(value)} items)", Colors.YELLOW, color_enabled))
                display_hierarchical_table(value, table_format, max_width, indent + 2, color_enabled)
            else:
                print(colorize(f"{prefix}{connector} {key}: ", Colors.GREEN, color_enabled) + 
                      highlight_value(value, color_enabled))
                
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
            
            print(colorize(f"{prefix}└─ Table:", Colors.BOLD, color_enabled))
            table_str = tabulate(df_display, headers='keys', tablefmt=table_format, showindex=False)
            
            # Colorize table if using plain/simple format
            if color_enabled and table_format in ["plain", "simple"]:
                table_str = colorize_table(table_str, color_enabled)
            
            # Indent each line of the table
            for line in table_str.split('\n'):
                print(f"{prefix}   {line}")
        else:
            # Simple array
            print(colorize(f"{prefix}└─ Array ({len(data)} items)", Colors.YELLOW, color_enabled))
            for i, item in enumerate(data):
                is_last = i == len(data) - 1
                connector = "└─" if is_last else "├─"
                print(colorize(f"{prefix}   {connector} [{i}]: ", Colors.CYAN, color_enabled) + 
                      highlight_value(item, color_enabled))
    else:
        print(colorize(f"{prefix}└─ ", Colors.BOLD, color_enabled) + highlight_value(data, color_enabled))

def display_hierarchical_json(data: Any, table_format: str = "grid", max_width: int = 100, color_enabled: bool = True) -> None:
    """Display JSON data in a hierarchical format with proper table formatting."""
    print(colorize("\nJSON Structure Display:", Colors.HEADER, color_enabled))
    print(colorize("=" * 60, Colors.BOLD, color_enabled))
    display_hierarchical_table(data, table_format, max_width, color_enabled=color_enabled)
    print(colorize("=" * 60, Colors.BOLD, color_enabled))

def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """Save DataFrame to CSV file."""
    try:
        df.to_csv(output_path, index=False)
        print(f"\nData saved to: {output_path}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def analyze_structure(data: Any, indent: int = 0, color_enabled: bool = True) -> None:
    """Analyze and display JSON structure."""
    prefix = "  " * indent

    if isinstance(data, dict):
        print(colorize(f"{prefix}Object ({len(data)} keys):", Colors.BOLD, color_enabled))
        for key, value in data.items():
            print(colorize(f"{prefix}  - {key}: ", Colors.GREEN, color_enabled) + 
                  colorize(f"{type(value).__name__}", Colors.CYAN, color_enabled))
            if isinstance(value, (dict, list)) and indent < 2:
                analyze_structure(value, indent + 2, color_enabled)
    elif isinstance(data, list):
        print(colorize(f"{prefix}Array ({len(data)} items):", Colors.YELLOW, color_enabled))
        if data:
            item_types = set(type(item).__name__ for item in data)
            print(colorize(f"{prefix}  Item types: ", Colors.BLUE, color_enabled) + 
                  colorize(f"{', '.join(item_types)}", Colors.CYAN, color_enabled))
            if len(data) > 0 and isinstance(data[0], (dict, list)) and indent < 2:
                print(colorize(f"{prefix}  Sample item structure:", Colors.BOLD, color_enabled))
                analyze_structure(data[0], indent + 2, color_enabled)
    else:
        print(colorize(f"{prefix}Value: ", Colors.BLUE, color_enabled) + 
              colorize(f"{type(data).__name__}", Colors.CYAN, color_enabled))

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
    parser.add_argument("--color", action="store_true",
                       help="Enable colored output (default: auto-detect)")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")

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
        print(colorize("\nJSON Structure Analysis:", Colors.HEADER, color_enabled))
        print(colorize("-" * 30, Colors.BOLD, color_enabled))
        analyze_structure(data, color_enabled=color_enabled)
        print()

    # Convert to DataFrame
    print("Converting to tabular format...")
    df = json_to_dataframe(data)

    # Determine color setting
    if args.color:
        color_enabled = True
    elif args.no_color:
        color_enabled = False
    else:
        color_enabled = is_color_supported()  # Auto-detect
    
    # Display table
    table_format = "plain" if args.ascii else args.format
    
    if args.hierarchical:
        display_hierarchical_json(data, table_format, args.width, color_enabled)
    else:
        display_table(df, table_format, args.width, color_enabled)

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
                "StorerKey": "CUSTOMER",
                "Sku": "978129244860",
                "ExternLineno": 202,
                "ExternReceiptKey": "ASN-EXT-0001"
            },
            {
                "QtyReceived": 15,
                "StorerKey": "CUSTOMER",
                "Sku": "978129243103",
                "ExternLineno": 203,
                "ExternReceiptKey": "ASN-EXT-0001"
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
                    "StorerKey": "CUSTOMER",
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
            "ExternReceiptKey": "ASN-EXT-0001"
        }
    }

    print("Example Usage:")
    print("=" * 50)

    # Convert to DataFrame
    df = json_to_dataframe(sample_data)

    # Display regular table
    display_table(df, "grid", 30, color_enabled=True)

    # Show hierarchical display
    print("\nHierarchical Display:")
    display_hierarchical_json(sample_data, "grid", 30, color_enabled=True)

    # Show structure
    print("\nStructure Analysis:")
    analyze_structure(sample_data, color_enabled=True)

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
        print("  --color            Enable colored output")
        print("  --no-color         Disable colored output")
        print("  -o, --output       Output CSV file path")
        print("  -w, --width        Maximum column width for display")
        print("  -s, --structure    Show JSON structure analysis")
        print("\nRunning example...")
        example_usage()
