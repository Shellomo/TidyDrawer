# TidyDrawer

TidyDrawer is an intelligent file organization tool that automatically sorts and manages your files based on customizable rules and actions.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Automatic file organization based on customizable rules
- Support for various file attributes (name, type, size, date, etc.)
- Extensible action system (currently supports file moving)
- YAML-based template configuration
- Detailed logging for all operations

## Installation

To install TidyDrawer, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tidydrawer.git
   ```
2. Navigate to the project directory:
   ```
   cd tidydrawer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use TidyDrawer:

1. Create a YAML template file with your desired rules and actions (see [Configuration](#configuration) for details).
2. Run the TidyDrawer engine:

```python
from tidydrawer.engine import TidyDrawerEngine

engine = TidyDrawerEngine()
engine.load_template("path/to/your/template.yaml")
results = engine.process_folder("path/to/target/folder")
print(results)
```

## Configuration

TidyDrawer uses YAML templates for configuration. Here's a basic example:

```yaml
version: 1
rules:
  - action: move_to_documents
    priority: 1
    conditions:
      - attribute: file_group
        operator: in
        values:
          - common_document
          - document

actions:
  move_to_documents:
    type: move
    destination: Documents
```

For more detailed configuration options, please refer to the documentation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.