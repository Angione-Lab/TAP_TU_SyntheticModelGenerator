#!/usr/bin/python3

"""
Author: Ross Conroy

Generates a model problem file by sampling from OSM data

Example CLI commands:
    osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json"
    osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json -r 42"
    osm_synthesiser.py -s "input_scenario.json" -o "output_problem.json -r 42"" -c "/tmp"
            
Required libraries (pip install <lib>):
    osmnx
    pandas
"""


"""
Command line options
"""

import getopt, sys, json, osmnx as ox, pandas as pd, random, copy, time

    
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "s:o:r:c:h"
long_options = ["scenario_file=", "output=", "random_seed=", "cache_directory=", "help"]

def print_help():
    print("Required command line options")
    print("\t\t-s ,--scenario_file scenario json definition file")
    print("\t\t-o ,--output json file")
    print("\t\t-r ,--random_seed seed random with value")
    print("\t\t-c ,--cache_directory osmnx cache directory")
    print("\t\t-h ,--help print this help")
    sys.exit()
    
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    # Output error, and return with an error code
    print("Error", str(err))
    print_help()

scenario_file = None
output_json_file = None
random_seed = None
osmnx_cache_directory = 'C:\\tmp\\osmnxcache'
for current_argument, current_value in arguments:
    if current_argument in ("-s", "--scenario_file"):
        scenario_file = current_value
    elif current_argument in ("-o", "--output"):
        output_json_file = current_value
    elif current_argument in ("-r", "--random_seed"):
        random_seed = int(current_value)
    elif current_argument in ("-c", "--cache_directory"):
        osmnx_cache_directory = current_value
    elif current_argument in ("-h", "--help"):
        print_help()

if scenario_file is None or output_json_file is None:
    print_help()


"""
Load scenario file
"""
scenario = None
with open(scenario_file) as jsonFile:
    scenario = json.load(jsonFile)
    
    
"""
Seed random
"""
if random_seed is None:
    random_seed = int(time.time())
random.seed(random_seed)


"""
If multi place names configured, choose one
"""
if 'place_names_choose_one_of' in scenario:
    scenario['place_names'] = random.choice(scenario['place_names_choose_one_of'])
    print("Selected Place Names: " + str (scenario['place_names']))


"""
Setup cache directory
"""
ox.config(use_cache=True, cache_folder=osmnx_cache_directory)

"""
OSM data extraction
"""
depots_dfs = []
deliveries_dfs = []
pickups_dfs = []
servicing_dfs = []
breaks_dfs = []
hubs_dfs = []
hubs_pickups_dfs = []
hubs_deliveries_dfs = []
hubs_pickups_dfs = []

for place_name in scenario['place_names']:
    print("Extracting depot locations for location: " + str(place_name))
    depot_tags = {}
    if 'depot_tags' in scenario:
        depot_tags = scenario['depot_tags']
    depots_df = ox.geometries_from_place(place_name, depot_tags)
    depots_df["place_name"] = place_name
    depots_dfs.append(depots_df)
    
    print("Extracting delivery locations for location: " + str(place_name))    
    delivery_tags = {}
    if 'delivery_tags' in scenario:
        delivery_tags = scenario['delivery_tags']
    deliveries_df = ox.geometries_from_place(place_name, delivery_tags)
    deliveries_df["place_name"] = place_name
    deliveries_dfs.append(deliveries_df)
    
    print("Extracting pickup locations for location: " + str(place_name))
    pickup_tags = {}
    if 'pickup_tags' in scenario:
        pickup_tags = scenario['pickup_tags']
    pickups_df = ox.geometries_from_place(place_name, pickup_tags)
    pickups_df["place_name"] = place_name
    pickups_dfs.append(pickups_df)
    
    print("Extracting servicing locations for location: " + str(place_name))    
    servicing_tags = {}
    if 'servicing_tags' in scenario:
        servicing_tags = scenario['servicing_tags']
    servicing_df = ox.geometries_from_place(place_name, servicing_tags)
    servicing_df["place_name"] = place_name
    servicing_dfs.append(servicing_df)
    
    print("Extracting break locations for location: " + str(place_name))
    break_locations = {}
    if 'break_locations' in scenario:
        break_locations = scenario['break_locations']
    breaks_df = ox.geometries_from_place(place_name, break_locations)
    breaks_df["place_name"] = place_name
    breaks_dfs.append(breaks_df)
    
    print("Extracting hub locations for location: " + str(place_name))
    hub_locations = {}
    if 'hub_tags' in scenario:
        hub_locations = scenario['hub_tags']
    hubs_df = ox.geometries_from_place(place_name, hub_locations)
    hubs_df["place_name"] = place_name
    hubs_dfs.append(hubs_df)
    
    print("Extracting hub delivery locations for location: " + str(place_name))
    hub_delivery_locations = {}
    if 'hub_delivery_tags' in scenario:
        hub_delivery_locations = scenario['hub_delivery_tags']
    hubs_deliveries_df = ox.geometries_from_place(place_name, hub_delivery_locations)
    hubs_deliveries_df["place_name"] = place_name
    hubs_deliveries_dfs.append(hubs_deliveries_df)
    
    print("Extracting hub pickup locations for location: " + str(place_name))
    hub_pickup_locations = {}
    if 'hub_pickup_tags' in scenario:
        hub_pickup_locations = scenario['hub_pickup_tags']
    hubs_pickups_df = ox.geometries_from_place(place_name, hub_pickup_locations)
    hubs_pickups_df["place_name"] = place_name
    hubs_pickups_dfs.append(hubs_pickups_df)

depots_df = pd.concat(depots_dfs)
deliveries_df = pd.concat(deliveries_dfs)
pickups_df = pd.concat(pickups_dfs)
servicing_df = pd.concat(servicing_dfs)
breaks_df = pd.concat(breaks_dfs)
hubs_df = pd.concat(hubs_dfs)
hubs_deliveries_df = pd.concat(hubs_deliveries_dfs)
hubs_pickups_df = pd.concat(hubs_pickups_dfs)

print ("Candidate depot loactions: " + str(len(depots_df)))
print ("Candidate delivery loactions: " + str(len(deliveries_df)))
print ("Candidate pickup loactions: " + str(len(pickups_df)))
print ("Candidate servicing loactions: " + str(len(servicing_df)))
print ("Candidate break loactions: " + str(len(breaks_df)))
print ("Candidate hub loactions: " + str(len(hubs_df)))
print ("Candidate hub delivery loactions: " + str(len(hubs_deliveries_df)))
print ("Candidate hub pickup loactions: " + str(len(hubs_pickups_df)))

"""
initial empty problem definition
"""
problem = {
    "data" : {
        "jobs" : [],
        "vehicles" : [],
        "hubs" : []
        },
    "_id" : scenario["id_prefix"] + "_" + str(random_seed)
    }


"""
Select break locations
"""
selected_break_locations = []
if 'target_min_break_at_location' in scenario and 'target_max_break_at_location' in scenario:
    num_break_locations = scenario["target_min_break_at_location"]
    if scenario["target_min_break_at_location"] != scenario["target_max_break_at_location"]:
        num_depots = random.randint(scenario["target_min_break_at_location"], scenario["target_max_break_at_location"])

    if num_break_locations > len(breaks_df.index):
        num_break_locations = len(breaks_df.index)
        
        
        
    selected_break_locations = random.sample(breaks_df.to_dict('records'), num_break_locations)


print ("Selected break loactions: " + str(len(selected_break_locations)))

"""
Select depots & create vehicles
"""
selected_depots = []
if 'target_min_depots' in scenario and 'target_max_depots' in scenario:
    num_depots = scenario["target_min_depots"]
    if scenario["target_min_depots"] != scenario["target_max_depots"]:
        num_depots = random.randint(scenario["target_min_depots"], scenario["target_max_depots"])
    
    if num_depots > len(depots_df.index):
        num_depots = len(depots_df.index)
    selected_depots = random.sample(depots_df.to_dict('records'), num_depots)

print ("Selected depot loactions: " + str(len(selected_depots)))

for selected_depot in selected_depots:
    
    # Set depot name, use a hash if no name available
    depot_name = str(selected_depot['name'])
    if depot_name == "nan":
        depot_name = str(abs(hash(str(selected_depot))))      
        
    # Set depot location
    depot_point = selected_depot['geometry'].representative_point()
    
    num_depot_vehicles = scenario["target_min_vehicles_per_depot"]
    if scenario["target_min_vehicles_per_depot"] != scenario["target_max_vehicles_per_depot"]:
        num_depot_vehicles = random.randint(scenario["target_min_vehicles_per_depot"], scenario["target_max_vehicles_per_depot"])
        
    for v in range(num_depot_vehicles):
                        
        new_vehicle = copy.deepcopy(random.sample(scenario["vehicle_templates"], 1)[0])
        
        if "vehicle_weights" in scenario:
            weighted_choice = random.choices(
                population = scenario["vehicle_templates"], 
                weights = scenario["vehicle_weights"],
                k = 1)[0]            
            new_vehicle = copy.deepcopy(weighted_choice)
            
        
        
        # Set vehicle ID
        vehicle_id = depot_name + "_" + str(v)
        
        if new_vehicle["_id"] is not None:
            vehicle_id = new_vehicle["_id"] + "_" + vehicle_id  
        
        new_vehicle["_id"] = vehicle_id
        
        # Set vehicle start and stop locations        
        new_vehicle["definition"]["start"]["_id"] = vehicle_id + "_start"
        new_vehicle["definition"]["end"]["_id"] = vehicle_id + "_end"
        
        if new_vehicle["definition"]["start"]["coordinate"] is None :         
            new_vehicle["definition"]["start"]["coordinate"] = {
                    "latitude" : depot_point.y,
                    "longitude" : depot_point.x        
                }
            
        if new_vehicle["definition"]["end"]["coordinate"] is None :
            new_vehicle["definition"]["end"]["coordinate"] = {
                    "latitude" : depot_point.y,
                    "longitude" : depot_point.x        
                }
        
        
        #Templated preloaded stops
        if "breaksTemplates" in new_vehicle["definition"]:
            for b in range(len(new_vehicle["definition"]["breaksTemplates"])):            
                for l in range(len(selected_break_locations)):
                    new_break = copy.deepcopy(new_vehicle["definition"]["breaksTemplates"][b])
                    break_point = selected_break_locations[l]['geometry'].representative_point()
                    new_break['coordinate'] = {
                            "latitude" : break_point.y,
                            "longitude" : break_point.x
                        }
                    
                    break_name = str(selected_break_locations[l]['name'])
                    if break_name == "nan":
                        break_name = str(abs(hash(str(selected_break_locations[l]))))
                        
                    new_break_id = break_name
                    
                    if new_break["_id"] is not None:
                        new_break_id = new_break["_id"] + "_" + new_break_id  
                        
                    new_break["_id"] = new_break_id
                    
                    new_vehicle["definition"]["preloadedStops"].append(new_break)
            new_vehicle["definition"].pop("breaksTemplates")        
        
        
        #Update ID of each preloaded stop
        for i in range(len(new_vehicle["definition"]["preloadedStops"])):
            
            stop_id = vehicle_id + "_" + new_vehicle["definition"]["preloadedStops"][i]["type"] + "_" + str(i)
            
            if new_vehicle["definition"]["preloadedStops"][i]["_id"] is not None:
                stop_id = vehicle_id + "_" + new_vehicle["definition"]["preloadedStops"][i]["_id"]                
                
            new_vehicle["definition"]["preloadedStops"][i]["_id"] = stop_id        
        
        problem["data"]["vehicles"].append(new_vehicle)
    


"""
Select delivery locations & create jobs
"""
selected_deliveries = []
if 'target_min_deliveries' in scenario and 'target_max_deliveries' in scenario:
    num_deliveries = scenario["target_min_deliveries"]
    if scenario["target_min_deliveries"] != scenario["target_max_deliveries"]:
        num_deliveries = random.randint(scenario["target_min_deliveries"], scenario["target_max_deliveries"])
        
    if num_deliveries > len(deliveries_df.index):
        num_deliveries = len(deliveries_df.index)
        
    selected_deliveries = []
    if num_deliveries > 0:    
        selected_deliveries = random.sample(deliveries_df.to_dict('records'), num_deliveries)
    
print ("Selected delivery loactions: " + str(len(selected_deliveries)))

delivery_num = 0
for selected_delivery in selected_deliveries:
    
    delivery_num += 1
    
    new_delivery = copy.deepcopy(random.sample(scenario["deliveries_templates"], 1)[0])
    
    # Set delivery name, use a hash if no name available
    delivery_name = str(selected_delivery['name'])
    if delivery_name == "nan":
        delivery_name = str(abs(hash(str(selected_delivery))))
        
    delivery_name = "delivery_" + str(delivery_num) + "_" + delivery_name
        
    # Set delivery ID
    new_delivery_id = delivery_name
    
    if new_delivery["_id"] is not None:
        new_delivery_id = new_delivery["_id"] + "_" + new_delivery_id  
    
    new_delivery["_id"] = new_delivery_id;
    new_delivery["stops"][0]["_id"] = new_delivery_id
    new_delivery["stops"][0]["_id"] = delivery_name
        
    # Set delivery location
    delivery_point = selected_delivery['geometry'].representative_point()
    
    new_delivery["stops"][0]["coordinate"] = {
            "latitude" : delivery_point.y,
            "longitude" : delivery_point.x        
        }
    
    problem["data"]["jobs"].append(new_delivery)
    

"""
Select pickup locations & create jobs
"""
selected_pickups = []
if 'target_min_pickups' in scenario and 'target_max_pickups' in scenario:
    num_pickups = scenario["target_min_pickups"]
    if scenario["target_min_pickups"] != scenario["target_max_pickups"]:
        num_pickups = random.randint(scenario["target_min_pickups"], scenario["target_max_pickups"])
        
    if num_pickups > len(pickups_df.index):
        num_pickups = len(pickups_df.index)
    
    selected_pickups = []
    if num_pickups > 0:    
        selected_pickups = random.sample(pickups_df.to_dict('records'), num_pickups)
    
print ("Selected pickup loactions: " + str(len(selected_pickups)))

pickup_num = 0
for selected_pickup in selected_pickups:
    
    pickup_num += 1
    
    new_pickup = copy.deepcopy(random.sample(scenario["pickups_templates"], 1)[0])
    
    # Set pickup name, use a hash if no name available
    pickup_name = str(selected_pickup['name'])
    if pickup_name == "nan":
        pickup_name = str(abs(hash(str(selected_pickup))))
        
    pickup_name = "pickup_" + str(pickup_num) + "_" + pickup_name
        
    
    # Set pickup ID
    new_pickup_id = pickup_name
    
    if new_pickup["_id"] is not None:
        new_pickup_id = new_pickup["_id"] + "_" + new_pickup_id  
    
    new_pickup["_id"] = new_pickup_id;
    new_pickup["stops"][0]["_id"] = new_pickup_id
    new_pickup["stops"][0]["_id"] = pickup_name
        
    # Set pickup location
    pickup_point = selected_pickup['geometry'].representative_point()
    
    new_pickup["stops"][0]["coordinate"] = {
            "latitude" : pickup_point.y,
            "longitude" : pickup_point.x        
        }
    
    problem["data"]["jobs"].append(new_pickup)



"""
Select servicing locations & create jobs
"""
selected_servicing = []
if 'target_min_servicing' in scenario and 'target_max_servicing' in scenario:
    num_servicing = scenario["target_min_servicing"]
    if scenario["target_min_servicing"] != scenario["target_max_servicing"]:
        num_servicing = random.randint(scenario["target_min_servicing"], scenario["target_max_servicing"])
        
    if num_servicing > len(servicing_df.index):
        num_servicing = len(servicing_df.index)
    
    selected_servicing = []
    if num_servicing > 0:    
        selected_servicing = random.sample(servicing_df.to_dict('records'), num_servicing)
    
print ("Selected servicing loactions: " + str(len(selected_servicing)))

servicing_num = 0
for selected_servicing_loc in selected_servicing:
    
    servicing_num += 1
    
    new_servicing = copy.deepcopy(random.sample(scenario["servicing_templates"], 1)[0])
    
    if "servicing_weights" in scenario:
        weighted_choice = random.choices(
            population = scenario["servicing_templates"], 
            weights = scenario["servicing_weights"],
            k = 1)[0]
        
        new_servicing = copy.deepcopy(weighted_choice)
    
    
    
    # Set pickup name, use a hash if no name available
    servicing_name = str(selected_servicing_loc['name'])
    if servicing_name == "nan":
        servicing_name = str(abs(hash(str(selected_servicing_loc))))
        
    servicing_name = "servicing_" + str(servicing_num) + "_" + servicing_name
        
    
    # Set pickup ID
    new_servicing_id = servicing_name
    
    if new_servicing["_id"] is not None:
        new_servicing_id = new_servicing["_id"] + "_" + new_servicing_id  
    
    new_servicing["_id"] = new_servicing_id;
    new_servicing["stops"][0]["_id"] = new_servicing_id
    new_servicing["stops"][0]["_id"] = servicing_name
        
    # Set pickup location
    servicing_point = selected_servicing_loc['geometry'].representative_point()
    
    new_servicing["stops"][0]["coordinate"] = {
            "latitude" : servicing_point.y,
            "longitude" : servicing_point.x        
        }
    
    problem["data"]["jobs"].append(new_servicing)


"""
Generate shipments from pickups and deliveries
"""
selected_pickups = []
selected_deliveries = []
num_shipments = 0
if 'target_min_shipments' in scenario and 'target_max_shipments' in scenario:
    num_shipments = scenario["target_min_shipments"]
    if scenario["target_min_shipments"] != scenario["target_max_shipments"]:
        num_shipments = random.randint(scenario["target_min_shipments"], scenario["target_max_shipments"])
        
    num_shipment_pickups = scenario["target_min_shipments"]
    if scenario["target_min_shipments"] != scenario["target_max_shipments"]:
        num_shipment_pickups = random.randint(scenario["target_min_shipments"], scenario["target_max_shipments"])
    
    if num_shipment_pickups > len(pickups_df.index):
        num_shipment_pickups = len(pickups_df.index)
    
    num_shipment_deliveries = scenario["target_min_shipments"]
    if scenario["target_min_shipments"] != scenario["target_max_shipments"]:
        num_shipment_deliveries = random.randint(scenario["target_min_shipments"], scenario["target_max_shipments"])
    
    if num_shipment_deliveries > len(deliveries_df.index):
        num_shipment_deliveries = len(deliveries_df.index)
    
    selected_pickups = []
    if num_shipment_pickups > 0:    
        selected_pickups = random.sample(pickups_df.to_dict('records'), num_shipment_pickups)
        
    selected_deliveries = []
    if num_shipment_deliveries > 0:    
        selected_deliveries = random.sample(deliveries_df.to_dict('records'), num_shipment_deliveries)
    
print ("Selected shipments: " + str(num_shipments))
shipment_num = 0
for i in range (num_shipments):
    
    shipment_num += 1
    
    selected_pickup = selected_pickups[0]
    selected_delivery = selected_deliveries[0]

    if i != 0:
        selected_pickup = selected_pickups[i % len (selected_pickups)]
        selected_delivery = selected_deliveries[i % len (selected_deliveries)]
    
    
    new_shipment = copy.deepcopy(random.sample(scenario["shipments_templates"], 1)[0])
    
    if "shipments_weights" in scenario:
        weighted_choice = random.choices(
            population = scenario["shipments_templates"], 
            weights = scenario["shipments_weights"],
            k = 1)[0]
        
        new_shipment = copy.deepcopy(weighted_choice)
        
    
    pickup_name = ""
    
    if new_shipment["stops"][0]['name'] is not None:
        pickup_name = new_shipment["stops"][0]['name'] + "_" + str(shipment_num)
    else:
        # Set pickup name, use a hash if no name available    
        pickup_name = str(selected_pickup['name'])
        if pickup_name == "nan":
            pickup_name = str(abs(hash(str(selected_pickup))))  
            
        pickup_name = "shipment_pickup_" + str(shipment_num) + "_" + pickup_name
        
    
    delivery_name = ""
    
    if new_shipment["stops"][1]['name'] is not None:
        delivery_name = new_shipment["stops"][1]['name'] + "_" + str(shipment_num)
    else:
        # Set pickup name, use a hash if no name available    
        delivery_name = str(selected_delivery['name'])
        if delivery_name == "nan":
            delivery_name = str(abs(hash(str(selected_delivery))))  
            
        delivery_name = "shipment_pickup_" + str(shipment_num) + "_" + delivery_name

      
    
    # Set stops details    
    if new_shipment["stops"][0]["_id"] is None:
        new_shipment["stops"][0]["_id"] = ""
    else:
        new_shipment["stops"][0]["_id"] = new_shipment["stops"][0]["_id"] + "_"
    
    if new_shipment["stops"][1]["_id"] is None:
        new_shipment["stops"][1]["_id"] = ""
    else:
        new_shipment["stops"][1]["_id"] = new_shipment["stops"][1]["_id"] + "_"
    
    new_shipment["stops"][0]["_id"] = new_shipment["stops"][0]["_id"] + pickup_name
    new_shipment["stops"][1]["_id"] = new_shipment["stops"][1]["_id"] + delivery_name
        
    # Set points
    if new_shipment["stops"][0]['coordinate'] is None:
        
        # Set pickup location
        pickup_point = selected_pickup['geometry'].representative_point()  
        new_shipment["stops"][0]["coordinate"] = {
                "latitude" : pickup_point.y,
                "longitude" : pickup_point.x        
        }
    
    if new_shipment["stops"][1]['coordinate'] is None:
        
        # Set delivery location
        delivery_point = selected_delivery['geometry'].representative_point()    
        new_shipment["stops"][1]["coordinate"] = {
                "latitude" : delivery_point.y,
                "longitude" : delivery_point.x        
            }
    
    # Add to problem
    if new_shipment["_id"] is None:
        new_shipment["_id"] = "shipment_" + str(i)
    else:
        new_shipment["_id"] = new_shipment["_id"] + "_" + str(i)
        
    problem["data"]["jobs"].append(new_shipment)
    
 
"""
Generate hubs
"""
selected_hubs = []
if 'target_min_hubs' in scenario and 'target_max_hubs' in scenario:
    num_hubs = scenario["target_min_hubs"]
    if scenario["target_min_hubs"] != scenario["target_max_hubs"]:
        num_hubs = random.randint(scenario["target_min_hubs"], scenario["target_max_hubs"])
    
    if num_hubs > len(hubs_df.index):
        num_hubs = len(hubs_df.index)
    selected_hubs = random.sample(hubs_df.to_dict('records'), num_hubs)

print ("Selected hubs: " + str(len(selected_hubs)))


hub_num = 0
for selected_hub in selected_hubs:
    
    hub_num += 1
    
    new_hub = copy.deepcopy(random.sample(scenario["hubs_templates"], 1)[0])
    
    # Set pickup name, use a hash if no name available
    hub_name = str(selected_hub['name'])
    if hub_name == "nan":
        hub_name = str(abs(hash(str(selected_hub))))
        
    hub_name = "hub_" + str(hub_num) + "_" + hub_name
    new_hub['name'] =  hub_name   
    
    # Set pickup ID
    new_hub_id = hub_name
    
    if new_hub["_id"] is not None:
        new_hub_id = new_hub["_id"] + "_" + new_hub_id  
    
    new_hub["_id"] = new_hub_id;
        
    # Set pickup location
    hub_point = selected_hub['geometry'].representative_point()
    
    new_hub["coordinate"] = {
            "latitude" : hub_point.y,
            "longitude" : hub_point.x        
        }
    
    problem["data"]["hubs"].append(new_hub)

    
"""
Generate via hubs jobs: deliveries
Using nearest hub to last mile dropoff assignment method
nearest depot to hub for backhaul
"""

selected_hubs_deliveries = []
if 'target_min_hub_deliveries' in scenario and 'target_max_hub_deliveries' in scenario:
    num_hubs_del = scenario["target_min_hub_deliveries"]
    if scenario["target_min_hub_deliveries"] != scenario["target_max_hub_deliveries"]:
        num_hubs_del = random.randint(scenario["target_min_hub_deliveries"], scenario["target_max_hub_deliveries"])
    
    if num_hubs_del > len(hubs_deliveries_df.index):
        num_hubs_del = len(hubs_deliveries_df.index)
    selected_hubs_deliveries = random.sample(hubs_deliveries_df.to_dict('records'), num_hubs_del)
    
    
print ("Selected hubs deliveries: " + str(len(selected_hubs_deliveries)))

import math
delivery_num = 0
for selected_hub_delivery in selected_hubs_deliveries:
    
    delivery_num += 1
    
    new_hub_jobs = copy.deepcopy(random.sample(scenario["hub_deliveries_templates"], 1)[0])
    
    new_backhaul = new_hub_jobs[0]
    new_last_mile = new_hub_jobs[1]
    
    # Select nearest hub to last mile (using pythagoras between lat/lng)    
    nearest_hub = None
    nearest_hub_distance = 1000000.0
    
    delivery_point = selected_hub_delivery['geometry'].representative_point()
    
    for hub in problem["data"]["hubs"]:
        
        dx = delivery_point.x - hub["coordinate"]["longitude"]
        dy = 2 * (delivery_point.y - hub["coordinate"]["latitude"])
        
        distance = math.sqrt((dx * dx) + (dy * dy))
        
        if distance < nearest_hub_distance:
            nearest_hub_distance = distance
            nearest_hub = hub
            
    # Set hub location on both parts of job
    new_backhaul["stops"][1]["coordinate"] = nearest_hub["coordinate"]
    new_last_mile["stops"][0]["coordinate"] = nearest_hub["coordinate"]
    
    
    # Select nearest depot to the hub
    nearest_depot = None
    nearest_depot_distance = 100000000.0
    
    for depot in selected_depots:
        depot_point = depot['geometry'].representative_point()
        
        dx = depot_point.x - nearest_hub["coordinate"]["longitude"]
        dy = 2 * (depot_point.y - nearest_hub["coordinate"]["latitude"])
        
        distance = math.sqrt((dx * dx) + (dy * dy))
        
        if distance < nearest_depot_distance:
            nearest_depot_distance = distance
            nearest_depot = depot
    
    nearest_depot_point = nearest_depot['geometry'].representative_point()
    
    new_backhaul["stops"][0]["coordinate"] = {
            "latitude" : nearest_depot_point.y,
            "longitude" : nearest_depot_point.x        
        }
    
    # Fill in delivery location coordinates
    new_last_mile["stops"][1]["coordinate"] = {
            "latitude" : delivery_point.y,
            "longitude" : delivery_point.x        
        }
    
    
    # Generate ID's
    # Set delivery name, use a hash if no name available
    delivery_name = str(selected_hub_delivery['name'])
    if delivery_name == "nan":
        delivery_name = str(abs(hash(str(selected_hub_delivery))))
        
    delivery_name = "hub_delivery_" + str(delivery_num) + "_" + delivery_name
        
    # Set ID's and names
    new_delivery_id = delivery_name
    
    
    if new_backhaul["_id"] is not None:
        new_backhaul["_id"] = new_backhaul["_id"] + "_" + new_delivery_id
    else:
        new_backhaul["_id"] = new_delivery_id
        
    if new_backhaul['stops'][0]["_id"] is not None:
        new_backhaul['stops'][0]["_id"] = new_backhaul['stops'][0]["_id"] + "_" + new_delivery_id
    else:
        new_backhaul['stops'][0]["_id"] = "backhaul-pickup_" + new_delivery_id
        
    if new_backhaul['stops'][1]["_id"] is not None:
        new_backhaul['stops'][1]["_id"] = new_backhaul['stops'][1]["_id"] + "_" + new_delivery_id
    else:
        new_backhaul['stops'][1]["_id"] = "backhaul-delivery_" + new_delivery_id
    
        
    if new_last_mile["_id"] is not None:
        new_last_mile["_id"] = new_last_mile["_id"] + "_" + new_delivery_id
    else:
        new_last_mile["_id"] = new_delivery_id
        
    if new_last_mile['stops'][0]["_id"] is not None:
        new_last_mile['stops'][0]["_id"] = new_last_mile['stops'][0]["_id"] + "_" + new_delivery_id
    else:
        new_backhaul['stops'][0]["_id"] = "last-mile-pickup_" + new_delivery_id
        
    if new_last_mile['stops'][1]["_id"] is not None:
        new_last_mile['stops'][1]["_id"] = new_last_mile['stops'][1]["_id"] + "_" + new_delivery_id
    else:
        new_backhaul['stops'][1]["_id"] = "last-mile-delivery_" + new_delivery_id
    
    
    problem["data"]["jobs"].append(new_backhaul)
    problem["data"]["jobs"].append(new_last_mile)


"""
Generate via hubs jobs: pickups
"""
selected_hubs_pickups = []
if 'target_min_hub_pickups' in scenario and 'target_max_hub_pickups' in scenario:
    
    num_hubs_pic = scenario["target_min_hub_pickups"]
    if scenario["target_min_hub_pickups"] != scenario["target_max_hub_pickups"]:
        num_hubs_pic = random.randint(scenario["target_min_hub_pickups"], scenario["target_max_hub_pickups"])
    
    if num_hubs_pic > len(hubs_pickups_df.index):
        num_hubs_pic = len(hubs_pickups_df.index)
    selected_hubs_pickups = random.sample(hubs_pickups_df.to_dict('records'), num_hubs_pic)
print ("Selected hubs pickups: " + str(len(selected_hubs_pickups)))

import math
pickup_num = 0
for selected_hub_pickup in selected_hubs_pickups:
    
    pickup_num += 1
    
    new_hub_jobs = copy.deepcopy(random.sample(scenario["hub_pickups_templates"], 1)[0])
    
    new_backhaul = new_hub_jobs[1]
    new_last_mile = new_hub_jobs[0]
    
    # Select nearest hub to last mile (using pythagoras between lat/lng)    
    nearest_hub = None
    nearest_hub_distance = 1000000.0
    
    pickup_point = selected_hub_pickup['geometry'].representative_point()
    
    for hub in problem["data"]["hubs"]:
        
        dx = pickup_point.x - hub["coordinate"]["longitude"]
        dy = 2 * (pickup_point.y - hub["coordinate"]["latitude"])
        
        distance = math.sqrt((dx * dx) + (dy * dy))
        
        if distance < nearest_hub_distance:
            nearest_hub_distance = distance
            nearest_hub = hub
            
    # Set hub location on both parts of job
    new_backhaul["stops"][0]["coordinate"] = nearest_hub["coordinate"]
    new_last_mile["stops"][1]["coordinate"] = nearest_hub["coordinate"]
    
    
    # Select nearest depot to the hub
    nearest_depot = None
    nearest_depot_distance = 100000000.0
    
    for depot in selected_depots:
        depot_point = depot['geometry'].representative_point()
        
        dx = depot_point.x - nearest_hub["coordinate"]["longitude"]
        dy = 2 * (depot_point.y - nearest_hub["coordinate"]["latitude"])
        
        distance = math.sqrt((dx * dx) + (dy * dy))
        
        if distance < nearest_depot_distance:
            nearest_depot_distance = distance
            nearest_depot = depot
    
    nearest_depot_point = nearest_depot['geometry'].representative_point()
    
    new_backhaul["stops"][1]["coordinate"] = {
            "latitude" : nearest_depot_point.y,
            "longitude" : nearest_depot_point.x        
        }
    
    # Fill in delivery location coordinates
    new_last_mile["stops"][0]["coordinate"] = {
            "latitude" : pickup_point.y,
            "longitude" : pickup_point.x        
        }
    
    
    # Generate ID's
    # Set delivery name, use a hash if no name available
    pickup_name = str(selected_hub_pickup['name'])
    if pickup_name == "nan":
        pickup_name = str(abs(hash(str(selected_hub_pickup))))
        
    pickup_name = "hub_pickup_" + str(pickup_num) + "_" + pickup_name
        
    # Set ID's and names
    new_pickup_id = pickup_name
    
    
    if new_backhaul["_id"] is not None:
        new_backhaul["_id"] = new_backhaul["_id"] + "_" + new_pickup_id
    else:
        new_backhaul["_id"] = new_pickup_id
        
    if new_backhaul['stops'][0]["_id"] is not None:
        new_backhaul['stops'][0]["_id"] = new_backhaul['stops'][0]["_id"] + "_" + new_pickup_id
    else:
        new_backhaul['stops'][0]["_id"] = "backhaul-pickup_" + new_pickup_id
        
    if new_backhaul['stops'][1]["_id"] is not None:
        new_backhaul['stops'][1]["_id"] = new_backhaul['stops'][1]["_id"] + "_" + new_pickup_id
    else:
        new_backhaul['stops'][1]["_id"] = "backhaul-delivery_" + new_pickup_id
    
        
    if new_last_mile["_id"] is not None:
        new_last_mile["_id"] = new_last_mile["_id"] + "_" + new_pickup_id
    else:
        new_last_mile["_id"] = new_pickup_id
        
    if new_last_mile['stops'][0]["_id"] is not None:
        new_last_mile['stops'][0]["_id"] = new_last_mile['stops'][0]["_id"] + "_" + new_pickup_id
    else:
        new_backhaul['stops'][0]["_id"] = "last-mile-pickup_" + new_pickup_id
        
    if new_last_mile['stops'][1]["_id"] is not None:
        new_last_mile['stops'][1]["_id"] = new_last_mile['stops'][1]["_id"] + "_" + new_pickup_id
    else:
        new_backhaul['stops'][1]["_id"] = "last-mile-delivery_" + new_pickup_id
    
    
    problem["data"]["jobs"].append(new_backhaul)
    problem["data"]["jobs"].append(new_last_mile)




"""
Save to output file
"""
with open(output_json_file, 'w', encoding='utf-8') as f:
    json.dump(problem, f, ensure_ascii=False, indent=4)
    
print("Done")
    
    