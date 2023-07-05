import json

def JsonToList(json_branch, parent_key=''):
    stats_list = {}

    if isinstance(json_branch, dict):
        for name, value in json_branch.items():
            new_key = parent_key + '_' + name if parent_key else name
            stats_list.update(JsonToList(value, new_key))
    elif isinstance(json_branch, list):
        for i, item in enumerate(json_branch):
            if isinstance(item, dict) and 'name' in item:
                component_name = item['name']
                new_key = parent_key + '_' + component_name if parent_key else component_name
                stats_list.update(JsonToList(item, new_key))
            elif isinstance(item, dict) and 'loc' in item:
                loc_value = item['loc']
                prefix = 'body' if loc_value == 'mini' else 'camera'
                for field, value in item.items():
                    if field != 'loc':
                        new_field = f"{parent_key}_{prefix}_{field}" if parent_key else f"{prefix}_{field}"
                        stats_list[new_field] = value
            else:
                new_key = parent_key + '_' + str(i) if parent_key else str(i)
                stats_list.update(JsonToList(item, new_key))
    elif isinstance(json_branch, (str, int)):
        stats_list[parent_key] = str(json_branch).lower()

    return stats_list

# Exemple d'utilisation
with open("stats_example.json") as json_file:
    json_data = json.load(json_file)
    stats_dict = JsonToList(json_data)

print(stats_dict)
