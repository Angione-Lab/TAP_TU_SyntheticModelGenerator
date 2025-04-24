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

### Place Names Configuration

The script supports two ways to specify place names:

1. **Single or Multiple Fixed Places**:
   - Use the `place_names` field to specify one or more places
   - Example: `"place_names": ["London, UK", "Manchester, UK"]`
   - The script will generate a problem that includes locations from all specified places
   - This is useful when you want to create a problem spanning multiple cities or regions

2. **Random Selection from Multiple Options**:
   - Use the `place_names_choose_one_of` field to specify multiple sets of places
   - Example: 
     ```json
     "place_names_choose_one_of": [
         ["London, UK"],
         ["Paris, France"],
         ["Berlin, Germany"]
     ]
     ```
   - The script will randomly select one set of places from the list
   - This is useful for generating different problem instances in different locations
   - The selection is deterministic when using the same random seed

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
    "place_names": ["London, UK", "Manchester, UK"],
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

3. **Random City Selection**:
```json
{
    "id_prefix": "random_city",
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
    "target_min_depots": 2,
    "target_max_depots": 3,
    "target_min_vehicles_per_depot": 2,
    "target_max_vehicles_per_depot": 4
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
- When using `place_names_choose_one_of`, the script will print the selected place names during execution.
- Multiple place names in `place_names` will create a problem that spans across all specified locations.
- The script will fetch data for each place name separately and combine them into a single problem instance.
