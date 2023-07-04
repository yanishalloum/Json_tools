import json
from pprint import pprint

def JsonToList(json_branch):
        stats_list = {}
        if isinstance(json_branch, dict):
            for name, value in json_branch.items():
                local_stats_list = JsonToList(value)
                for stats_list_name, stats_list_value in local_stats_list.items():
                    stats_list[name+ "_" + stats_list_name] = str(stats_list_value).lower()
        elif isinstance(json_branch, list):
            for item in json_branch:
                JsonToList(item)
        elif isinstance(json_branch, (str, int)):
            stats_list[''] = str(json_branch).lower()  
                
        return stats_list



stats_list = []
with open("stats_example.json") as json_branch:
    json_data = json.load(json_branch)
    
    stats_dict = JsonToList(json_data)
    for object in stats_dict:
            substring_object = str(object[8:-1]).lower()
            stats_list.append([substring_object, stats_dict[object]])
    pprint(stats_list)

        
