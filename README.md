# JSON to Table Converter

A powerful Python script that converts JSON files into tabular format and displays them as beautifully formatted tables. Perfect for data analysis, debugging, and presenting JSON data in a readable format.

## Features

- **Multiple Table Formats**: Support for grid, plain, simple, github, and fancy_grid table styles
- **ASCII Output**: Clean ASCII table format for maximum compatibility
- **Color Output**: Beautiful colored output with syntax highlighting for better readability
- **Schema Generation**: Automatically generate comprehensive JSON schemas with data type detection
- **Hierarchical Display**: Show JSON structure with nested tables and proper indentation
- **Nested JSON Handling**: Automatically flattens complex nested JSON structures
- **CSV Export**: Save converted data to CSV files
- **Structure Analysis**: Analyze and display JSON structure for better understanding
- **Customizable Display**: Adjust column widths and table formatting
- **Error Handling**: Robust error handling for file operations and JSON parsing

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Dependencies

Install the required packages:

```bash
pip install pandas tabulate flatten-json
```

Or install from the requirements file (if available):

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python json_converter.py <json_file>
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --format` | Table format (grid, plain, simple, github, fancy_grid) | grid |
| `-a, --ascii` | Output table in ASCII format | False |
| `--hierarchical` | Display JSON in hierarchical format with nested tables | False |
| `--color` | Enable colored output | Auto-detect |
| `--no-color` | Disable colored output | False |
| `--schema` | Generate and display JSON schema | False |
| `--schema-detailed` | Generate detailed schema with statistics | False |
| `--output-schema` | Save schema to file (.json, .yaml, .md) | None |
| `-o, --output` | Output CSV file path | None |
| `-w, --width` | Maximum column width for display | 50 |
| `-s, --structure` | Show JSON structure analysis | False |

### Examples

#### Basic table display
```bash
python json_converter.py data.json
```

#### ASCII table output
```bash
python json_converter.py data.json -a
```

#### Custom table format
```bash
python json_converter.py data.json -f simple
```

#### Save to CSV
```bash
python json_converter.py data.json -o output.csv
```

#### Show structure analysis
```bash
python json_converter.py data.json -s
```

#### Hierarchical display
```bash
python json_converter.py data.json --hierarchical
```

#### Hierarchical display with ASCII format
```bash
python json_converter.py data.json --hierarchical -a
```

#### Hierarchical display with custom width
```bash
python json_converter.py data.json --hierarchical -w 80
```

#### Hierarchical display with simple format
```bash
python json_converter.py data.json --hierarchical -f simple
```

#### Enable colored output
```bash
python json_converter.py data.json --color
```

#### Disable colored output
```bash
python json_converter.py data.json --no-color
```

#### Combine multiple options
```bash
python json_converter.py data.json -a -w 80 -o output.csv -s
```

#### Hierarchical display with multiple options
```bash
python json_converter.py data.json --hierarchical -a -w 80 -o output.csv
```

#### Colored hierarchical display
```bash
python json_converter.py data.json --hierarchical --color
```

#### Generate JSON schema
```bash
python json_converter.py data.json --schema
```

#### Generate detailed schema with statistics
```bash
python json_converter.py data.json --schema-detailed
```

#### Save schema to JSON file
```bash
python json_converter.py data.json --schema --output-schema schema.json
```

#### Save schema to YAML file
```bash
python json_converter.py data.json --schema --output-schema schema.yaml
```

#### Save schema to Markdown file
```bash
python json_converter.py data.json --schema --output-schema schema.md
```

## Table Formats

The script supports several table formats:

- **grid**: Default format with Unicode box-drawing characters
- **plain**: Simple ASCII format with basic characters
- **simple**: Clean format with minimal styling
- **github**: GitHub-style markdown table format
- **fancy_grid**: Enhanced grid format with better styling

## Color Output

The converter includes intelligent color highlighting to improve readability:

### Color Scheme
- **🔵 Blue**: Regular strings and text
- **🟢 Green**: Keys, IDs, and identifiers
- **🟡 Yellow**: Dates and timestamps
- **🔴 Red**: Empty values (null, empty strings)
- **🟣 Purple**: Headers and section titles
- **⚪ Cyan**: Numbers and counts
- **⚫ Bold**: Important structural elements

### Color Features
- **Auto-detection**: Automatically detects if your terminal supports colors
- **Smart highlighting**: Different data types are highlighted with appropriate colors
- **Manual control**: Use `--color` to force enable or `--no-color` to disable
- **Table enhancement**: Headers and data cells are colorized for better readability
- **Hierarchical display**: Tree structure elements are color-coded by type

## Schema Generation

The converter includes intelligent schema generation that automatically analyzes your JSON data and creates comprehensive schema definitions:

### Schema Features
- **Automatic Type Detection**: Identifies data types (string, integer, boolean, object, array)
- **Pattern Recognition**: Detects date formats, email addresses, IDs, and numeric patterns
- **Statistical Analysis**: Provides null rates, uniqueness, and value distributions
- **Required Field Detection**: Identifies mandatory fields based on data presence
- **Multiple Output Formats**: Export schemas as JSON, YAML, or Markdown

### Pattern Detection
The schema generator recognizes common data patterns:
- **📅 Dates**: MM/DD/YYYY and MM/DD/YYYY HH:MM:SS formats
- **📧 Emails**: Standard email address patterns
- **🔑 IDs/Keys**: Uppercase alphanumeric identifiers
- **🔢 Numbers**: Integer and decimal number formats
- **📝 Strings**: Text with length analysis

### Schema Output Example
```
📋 JSON Schema Analysis
============================================================
📁 root: object
  🔤 Type: string
     📝 Document type identifier
     💡 Example: IR
  📋 WODetail: array
    📁 item: object
      🔢 QtyReceived: integer
         📝 Quantity received
         💡 Example: 10
         📊 Null rate: 0.0%
      🔤 StorerKey: string
         📝 Identifier or key
         💡 Example: CUSTOMER
         🔑 Unique values: 1
      🔤 Sku: string
         📝 Numeric string
         💡 Example: 978129244860
  📁 POIR: object
    🔢 Suer2: integer
       📝 Integer number
       💡 Example: 0
    🔤 ReceiptKey: string
       📝 Numeric string
       💡 Example: 000001675
    🔤 ReceiptDate: string
       📝 Date and time in MM/DD/YYYY HH:MM:SS format
       💡 Example: 11/18/2022 14:37:31
============================================================
```

### Schema Export Formats

#### JSON Schema Format
```json
{
  "type": "object",
  "properties": {
    "Type": {
      "type": "string",
      "description": "Document type identifier",
      "example": "IR"
    },
    "WODetail": {
      "type": "array",
      "description": "Array of 2 objects",
      "items": {
        "type": "object",
        "properties": {
          "QtyReceived": {
            "type": "integer",
            "description": "Quantity received",
            "example": 10
          }
        },
        "required": ["QtyReceived", "StorerKey", "Sku"]
      }
    }
  }
}
```

#### YAML Format
```yaml
type: object
properties:
  Type:
    type: string
    description: Document type identifier
    example: IR
  WODetail:
    type: array
    description: Array of 2 objects
    items:
      type: object
      properties:
        QtyReceived:
          type: integer
          description: Quantity received
          example: 10
```

## JSON Structure Support

The converter handles various JSON structures:

### Simple Objects
```json
{
  "Type": "IR",
  "ReceiptKey": "0000001675",
  "ReceiptDate": "11/18/2022 14:37:31"
}
```

### Arrays of Objects
```json
[
  {
    "QtyReceived": 10,
    "StorerKey": "CUSTOMER",
    "Sku": 9781292244860,
    "ExternLineno": 202,
    "ExternReceiptKey": "ASN-EXT-0001"
  },
  {
    "QtyReceived": 15,
    "StorerKey": "CUSTOMER",
    "Sku": 9781292433103,
    "ExternLineno": 203,
    "ExternReceiptKey": "ASN-EXT-0001"
  }
]
```

### Nested Structures
```json
{
  "Type": "IR",
  "WODetail": [
    {
      "QtyReceived": 10,
      "StorerKey": "CUSTOMER",
      "Sku": 9781292244860,
      "ExternLineno": 202,
      "ExternReceiptKey": "ASN-EXT-0001"
    }
  ],
  "POIR": {
    "Susr2": 0,
    "ReceiptKey": "0000001675",
    "ReceiptDate": "11/18/2022 14:37:31",
    "AsnDetail": [
      {
        "Status": "AVL",
        "QtyReceived": 10,
        "StorerKey": "CUSTOMER",
        "ToLoc": "STAGE",
        "Sku": 9781292244860,
        "ExternLineno": 202,
        "ExternReceiptKey": "WMS0000001675"
      }
    ]
  }
}
```

### Mixed Data Types
```json
{
  "Type": "IR",
  "WODetail": [
    {"QtyReceived": 10, "StorerKey": "CUSTOMER"},
    {"QtyReceived": 15, "StorerKey": "CUSTOMER"}
  ],
  "POIR": {
    "Susr2": 0,
    "ReceiptKey": "0000001675",
    "AsnDetail": []
  }
}
```

## Output Examples

### Grid Format (Default)
```
Table (1 rows, 15 columns):
==================================================
  Type  WODetail_0_QtyReceived  WODetail_0_StorerKey  WODetail_0_Sku  WODetail_0_ExternLineno  WODetail_0_ExternReceiptKey  WODetail_1_QtyReceived  WODetail_1_StorerKey  WODetail_1_Sku  WODetail_1_ExternLineno  WODetail_1_ExternReceiptKey  POIR_Susr2  POIR_ReceiptKey  POIR_ReceiptDate  POIR_AsnDetail_0_Status  POIR_AsnDetail_0_QtyReceived  POIR_AsnDetail_0_StorerKey  POIR_AsnDetail_0_ToLoc  POIR_AsnDetail_0_Susr1  POIR_AsnDetail_0_Susr2  POIR_AsnDetail_0_Susr3  POIR_AsnDetail_0_Sku  POIR_AsnDetail_0_ReturnType  POIR_AsnDetail_0_ExternLineno  POIR_AsnDetail_0_purchaseorderdocument  POIR_AsnDetail_0_ExternReceiptKey  POIR_AsnDetail_1_Status  POIR_AsnDetail_1_QtyReceived  POIR_AsnDetail_1_StorerKey  POIR_AsnDetail_1_ToLoc  POIR_AsnDetail_1_Susr1  POIR_AsnDetail_1_Susr2  POIR_AsnDetail_1_Susr3  POIR_AsnDetail_1_Sku  POIR_AsnDetail_1_ReturnType  POIR_AsnDetail_1_ExternLineno  POIR_AsnDetail_1_purchaseorderdocument  POIR_AsnDetail_1_ExternReceiptKey  POIR_ExternReceiptKey
-----  ----------------------  --------------------  --------------  ----------------------  -------------------------  ----------------------  --------------------  --------------  ----------------------  -------------------------  -----------  ----------------  -----------------  -----------------------  -------------------------  -----------------------  -----------------  -----------------  -----------------  -----------------  --------------  ----------------------  -------------------------  -------------------------  -----------------------  -------------------------  -----------------------  -----------------  -----------------  -----------------  -----------------  --------------  ----------------------  -------------------------  -------------------------  -------------------------
  IR                       10  CUSTOMER          9781292244860                     202  ASN-EXT-0001                          15  CUSTOMER          9781292433103                     203  ASN-EXT-0001                          0  0000001675        11/18/2022 14:37:31  AVL                             10  CUSTOMER           STAGE                        0                         AVL                             15  CUSTOMER           STAGE                        0                         ASN-EXT-0001
==================================================
```

### ASCII Format
```
Table (1 rows, 15 columns):
==================================================
| Type | WODetail_0_QtyReceived | WODetail_0_StorerKey | WODetail_0_Sku | WODetail_0_ExternLineno | WODetail_0_ExternReceiptKey | WODetail_1_QtyReceived | WODetail_1_StorerKey | WODetail_1_Sku | WODetail_1_ExternLineno | WODetail_1_ExternReceiptKey | POIR_Susr2 | POIR_ReceiptKey | POIR_ReceiptDate | POIR_AsnDetail_0_Status | POIR_AsnDetail_0_QtyReceived | POIR_AsnDetail_0_StorerKey | POIR_AsnDetail_0_ToLoc | POIR_AsnDetail_0_Susr1 | POIR_AsnDetail_0_Susr2 | POIR_AsnDetail_0_Susr3 | POIR_AsnDetail_0_Sku | POIR_AsnDetail_0_ReturnType | POIR_AsnDetail_0_ExternLineno | POIR_AsnDetail_0_purchaseorderdocument | POIR_AsnDetail_0_ExternReceiptKey | POIR_AsnDetail_1_Status | POIR_AsnDetail_1_QtyReceived | POIR_AsnDetail_1_StorerKey | POIR_AsnDetail_1_ToLoc | POIR_AsnDetail_1_Susr1 | POIR_AsnDetail_1_Susr2 | POIR_AsnDetail_1_Susr3 | POIR_AsnDetail_1_Sku | POIR_AsnDetail_1_ReturnType | POIR_AsnDetail_1_ExternLineno | POIR_AsnDetail_1_purchaseorderdocument | POIR_AsnDetail_1_ExternReceiptKey | POIR_ExternReceiptKey |
|------|----------------------|---------------------|----------------|----------------------|---------------------------|----------------------|---------------------|----------------|----------------------|---------------------------|------------|----------------|-----------------|-----------------------|---------------------------|------------------------|-------------------|-------------------|-------------------|-------------------|----------------|------------------------|---------------------------|--------------------------------|---------------------------|-----------------------|---------------------------|------------------------|-------------------|-------------------|-------------------|-------------------|----------------|------------------------|---------------------------|--------------------------------|---------------------------|---------------------------|
| IR   | 10                   | CUSTOMER         | 9781292244860  | 202                  | ASN-EXT-0001              | 15                   | CUSTOMER         | 9781292433103  | 203                  | ASN-EXT-0001              | 0          | 0000001675     | 11/18/2022 14:37:31 | AVL                     | 10                          | CUSTOMER           | STAGE             | 0                 |                   |                   | 9781292244860  |                        | 202                        |                                | WMS0000001675              | AVL                     | 15                          | CUSTOMER           | STAGE             | 0                 |                   |                   | 9781292433103  |                        | 203                        |                                | WMS0000001675              | ASN-EXT-0001              |
==================================================
```

### Hierarchical Format
```
JSON Structure Display:
============================================================
┌─ Object (3 keys)
├─ Type: IR
├─ WODetail: Array (2 items)
└─ Table:
   +-------+-------------+-------------+------------------+----------------+---------------------+
   | Index | QtyReceived | StorerKey   | Sku              | ExternLineno   | ExternReceiptKey    |
   +-------+-------------+-------------+------------------+----------------+---------------------+
   |     0 |          10 | CUSTOMER | 9781292244860    |            202 | ASN-EXT-0001        |
   |     1 |          15 | CUSTOMER | 9781292433103    |            203 | ASN-EXT-0001        |
   +-------+-------------+-------------+------------------+----------------+---------------------+
└─ POIR: Object (4 keys)
   ├─ Susr2: 0
   ├─ ReceiptKey: 0000001675
   ├─ ReceiptDate: 11/18/2022 14:37:31
   ├─ AsnDetail: Array (2 items)
   └─ Table:
      +-------+--------+-------------+-------------+--------+-------+-------+-------+------------------+-------------+----------------+------------------------+---------------------+
      | Index | Status | QtyReceived | StorerKey   | ToLoc  | Susr1 | Susr2 | Susr3 | Sku              | ReturnType  | ExternLineno   | purchaseorderdocument | ExternReceiptKey    |
      +-------+--------+-------------+-------------+--------+-------+-------+-------+------------------+-------------+----------------+------------------------+---------------------+
      |     0 | AVL    |          10 | CUSTOMER | STAGE  |     0 |       |       | 9781292244860    |             |            202 |                       | WMS0000001675        |
      |     1 | AVL    |          15 | CUSTOMER | STAGE  |     0 |       |       | 9781292433103    |             |            203 |                       | WMS0000001675        |
      +-------+--------+-------------+-------------+--------+-------+-------+-------+------------------+-------------+----------------+------------------------+---------------------+
   └─ ExternReceiptKey: ASN-EXT-0001
============================================================
```

### Hierarchical Format with ASCII
```
JSON Structure Display:
============================================================
┌─ Object (3 keys)
├─ Type: IR
├─ WODetail: Array (2 items)
└─ Table:
   | Index | QtyReceived | StorerKey   | Sku              | ExternLineno | ExternReceiptKey |
   |-------|-------------|-------------|------------------|--------------|------------------|
   | 0     | 10          | CUSTOMER | 9781292244860    | 202          | ASN-EXT-0001     |
   | 1     | 15          | CUSTOMER | 9781292433103    | 203          | ASN-EXT-0001     |
└─ POIR: Object (4 keys)
   ├─ Susr2: 0
   ├─ ReceiptKey: 0000001675
   ├─ ReceiptDate: 11/18/2022 14:37:31
   ├─ AsnDetail: Array (2 items)
   └─ Table:
      | Index | Status | QtyReceived | StorerKey   | ToLoc | Susr1 | Susr2 | Susr3 | Sku              | ReturnType | ExternLineno | purchaseorderdocument | ExternReceiptKey |
      |-------|--------|-------------|-------------|-------|-------|-------|-------|------------------|------------|--------------|---------------------|------------------|
      | 0     | AVL    | 10          | CUSTOMER | STAGE | 0     |       |       | 9781292244860    |            | 202          |                     | WMS0000001675    |
      | 1     | AVL    | 15          | CUSTOMER | STAGE | 0     |       |       | 9781292433103    |            | 203          |                     | WMS0000001675    |
   └─ ExternReceiptKey: ASN-EXT-0001
============================================================
```

## Error Handling

The script includes comprehensive error handling for:

- **File Not Found**: Clear error message when JSON file doesn't exist
- **Invalid JSON**: Detailed parsing error information
- **Permission Issues**: File access permission errors
- **CSV Export Errors**: Issues with saving output files

## Programmatic Usage

You can also use the functions directly in your Python code:

```python
from json_converter import json_to_dataframe, display_table

# Load and convert JSON data
data = load_json_file('data.json')
df = json_to_dataframe(data)

# Display as table
display_table(df, format='grid', max_width=50)

# Save to CSV
df.to_csv('output.csv', index=False)
```

## File Structure

```
json-to-table/
├── json_converter.py    # Main converter script
├── data.json           # Sample JSON data file
└── README.md           # This file
```

## Requirements

- **pandas**: Data manipulation and analysis
- **tabulate**: Table formatting and display
- **flatten-json**: Nested JSON flattening
- **argparse**: Command line argument parsing
- **pathlib**: File path handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [GNU General Public License v3.0](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the error messages for guidance
2. Verify your JSON file is valid
3. Ensure all dependencies are installed
4. Try using the `-s` flag to analyze your JSON structure

