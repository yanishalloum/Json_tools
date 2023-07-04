import json

def json_to_list(json_branch):
    branch_type = type(json_branch)
    stats_table = {}
    print (branch_type)
    if branch_type in [dict, list]:
        for name, element in json_branch.items():
            local_stats_table = json_to_list(element)
            for stats_table_name, stats_table_element in local_stats_table.items():
                stats_table[name+ "_" + stats_table_name] = stats_table_element
    elif branch_type in [str, int]:
        stats_table[''] = json_branch
    else:
        print ("toto")
    return stats_table



def JsonToList(json_branch):
        stats_table = {}
        if isinstance(json_branch, dict):
            for name, element in json_branch.items():
                local_stats_table = JsonToList(element)
                for stats_table_name, stats_table_element in local_stats_table.items():
                    stats_table[name+ "_" + stats_table_name] = stats_table_element
        elif isinstance(json_branch, list):
            for item in json_branch:
                JsonToList(item)
        elif isinstance(json_branch, (str, int)):
            stats_table[''] = json_branch.lower()        
        return stats_table




with open("stats_example.json") as json_branch:
    json_data = json.load(json_branch)
    
    stats_list = JsonToList(json_data)
    print (stats_list)
        
