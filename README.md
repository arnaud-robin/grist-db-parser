# Grist DB parser

This Python script `grist_parser.py` provides functionality to convert [Grist](https://github.com/gristlabs/grist-core) code view types to [DBML](https://github.com/holistics/dbml) language. It's designed to help with representing a document database structure definition as well as visualize it on [dbdiagram.io](https://dbdiagram.io/).

## Installation

Clone this repository using Git:
```bash
git clone https://github.com/arnaud-robin/grist-db-parser
```

## Usage 
To use this script, import the `parse_grist_code` function and pass the Grist type as a parameter:

```python
from grist_parser import parse_grist_code, write_dbml_to_file
dbml_code = parse_grist_code("examples/grist_inventory_manager.py")
write_dbml_to_file(dbml_code, "examples/inventory_manager.dbml")
```

The dbml file can then be uploaded on [dbdiagram.io](https://dbdiagram.io/) for visualization. The grist template used as example can be found [here](https://templates.getgrist.com/sXsBGDTKau1F/Inventory-Manager).

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your proposed changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
