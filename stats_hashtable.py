stats_table = []

for hardware in stats_data[model]['hardware']:
    for object in stats_data[model]['hardware'][hardware]:
        if type(object) == str:
            field_name = f"hardware_{hardware}_{object}"
            field_value = stats_data[model]['hardware'][hardware][object]
            stats_table.append([field_name, field_value])
        elif (hardware == 'board'):
            field_name = f"hardware_{hardware}_{object['name']}"
            field_value = object['id']
            stats_table.append([field_name, field_value])
        elif (hardware == 'sd'):
            for field in object:
                if type(field) == str:
                    field_name = field
                    field_value = f"hardware_{hardware}_{object[field]}"
                    stats_table.append([field_name, field_value])

pprint(stats_table)
