# TAP_TU_SyntheticModelGenerator

A tool for generating synthetic Vehicle Routing Problem (VRP) instances by sampling from OpenStreetMap (OSM) data.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/TAP_TU_SyntheticModelGenerator.git
cd TAP_TU_SyntheticModelGenerator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The `osm_synthesiser.py` script generates synthetic VRP problems by sampling from OpenStreetMap data. It takes several command-line arguments:

- `-s, --scenario_file`: Input scenario JSON definition file (required)
- `-o, --output`: Output JSON file (required)
- `-r, --random_seed`: Seed for random number generation (optional)
- `-c, --cache_directory`: OSMnx cache directory (optional, defaults to 'C:\tmp\osmnxcache')
- `-h, --help`: Print help message

### Basic Example

```bash
python osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json"
```

### Example with Random Seed

```bash
python osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json" -r 42
```

### Example with Custom Cache Directory

```bash
python osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json" -r 42 -c "/tmp"
```

## Input Scenario File Format

The input scenario file should be a JSON file with the following structure:

```json
{
    "id_prefix": "example",
    "place_names": ["London, UK"],
    "place_names_choose_one_of": [
        ["London, UK"],
        ["Paris, France"],
        ["Berlin, Germany"]
    ],
    "depot_tags": {
        "amenity": "warehouse"
    },
    "delivery_tags": {
        "shop": "supermarket"
    },
    "pickup_tags": {
        "shop": "convenience"
    },
    "servicing_tags": {
        "amenity": "service"
    },
    "break_locations": {
        "amenity": "restaurant"
    },
    "hub_tags": {
        "amenity": "hub"
    },
    "hub_delivery_tags": {
        "shop": "department_store"
    },
    "hub_pickup_tags": {
        "shop": "mall"
    },
    "target_min_depots": 2,
    "target_max_depots": 5,
    "target_min_vehicles_per_depot": 3,
    "target_max_vehicles_per_depot": 5,
    "target_min_break_at_location": 1,
    "target_max_break_at_location": 3
}
```

### Example Scenarios

1. **Basic Urban Delivery Scenario**:
```json
{
    "id_prefix": "urban_delivery",
    "place_names": ["New York, USA"],
    "depot_tags": {
        "amenity": "warehouse"
    },
    "delivery_tags": {
        "shop": "supermarket"
    },
    "target_min_depots": 2,
    "target_max_depots": 3,
    "target_min_vehicles_per_depot": 2,
    "target_max_vehicles_per_depot": 4
}
```

2. **Multi-City Pickup and Delivery**:
```json
{
    "id_prefix": "multi_city",
    "place_names_choose_one_of": [
        ["London, UK"],
        ["Paris, France"],
        ["Berlin, Germany"]
    ],
    "depot_tags": {
        "amenity": "warehouse"
    },
    "pickup_tags": {
        "shop": "convenience"
    },
    "delivery_tags": {
        "shop": "supermarket"
    },
    "target_min_depots": 3,
    "target_max_depots": 5,
    "target_min_vehicles_per_depot": 3,
    "target_max_vehicles_per_depot": 5
}
```

## Output Format

The script generates a JSON file containing the synthetic VRP problem with the following structure:

```json
{
    "data": {
        "jobs": [...],
        "vehicles": [...],
        "hubs": [...]
    },
    "_id": "example_42"
}
```

## Notes

- The script uses OSMnx to fetch data from OpenStreetMap, so an internet connection is required.
- The cache directory is used to store downloaded OSM data to avoid repeated downloads.
- The random seed can be used to reproduce the same problem instance.
- The script supports multiple place names and can randomly choose one from a list.
