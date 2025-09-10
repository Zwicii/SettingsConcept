# Settings Management System

A Python-based settings management system using Pydantic models for type-safe configuration with JSON schema generation and user override capabilities.

## Features

- **Type-safe Settings**: Pydantic models with validation for all configuration parameters
- **JSON Schema Generation**: Automatic generation of JSON schemas for documentation and validation
- **User Overrides**: Support for user-specific configuration overrides via JSON files
- **Deep Merging**: Intelligent merging of default and user settings using deepmerge
- **Updatable Fields**: Fine-grained control over which fields can be updated by users

## Project Structure

```
settings/
├── models.py              # Core Pydantic models and SettingsMixin
├── settings_demo.ipynb    # Interactive demo notebook
├── settings/              # Generated configuration files
│   ├── AppSettings.schema.json
│   ├── AppSettings.brain.json
│   ├── SystemSettings.schema.json
│   └── SystemSettings.user.json
└── pyproject.toml         # Project dependencies
```

## Models

### AppSettings
Application-level configuration including:
- **Object Detection**: CNN network selection, minimum object size, confidence threshold
- **Tracker**: Minimum seen count, maximum unseen count

### SystemSettings
System-level configuration including:
- **NMEA**: IP address and port configuration for NMEA data

## Usage

### Basic Usage

```python
from models import AppSettings, SystemSettings

# Create settings with default values
app_settings = AppSettings()
system_settings = SystemSettings()

# Generate JSON schemas
app_settings.generate_schema(base_path="settings")
system_settings.generate_schema(base_path="settings")
```

### Loading with User Overrides

```python
# Load settings with user overrides applied
app_settings = AppSettings.load_with_overrides("custom_settings.json")
system_settings = SystemSettings.load_with_overrides()
```

### Updating Settings

```python
# Update settings from a JSON file
settings.update("path/to/overrides.json")
```

## Configuration Fields

### Object Detection
- `cnn_network`: CNN network type (DAN, AHOY, YOLO, CERULEAN)
- `min_object_size`: Minimum object size threshold (default: 6)
- `cnn_confidence_threshold`: Confidence threshold for detections (default: 0.5)

### Tracker
- `count_min_seen`: Minimum times an object must be seen (default: 10)
- `count_max_unseen`: Maximum times an object can be unseen (default: 20)

### NMEA
- `ip_address`: NMEA server IP address (default: "127.0.0.1")
- `port`: NMEA server port (default: 8080)

## Field Updatability

Fields can be marked as updatable or non-updatable using the `json_schema_extra` parameter:

```python
updatable_field = Field(default=value, json_schema_extra={"updatable": True})
non_updatable_field = Field(default=value, json_schema_extra={"updatable": False})
```

## Dependencies

- `pydantic>=2.11.7`: Data validation and settings management
- `deepmerge>=2.0`: Deep merging of configuration dictionaries
- `ipykernel>=6.30.1`: Jupyter notebook support

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Demo

Run the interactive demo notebook to explore the settings system:

```bash
jupyter notebook settings_demo.ipynb
```

## Development

The project uses modern Python packaging with `pyproject.toml` and supports Python 3.11+.
