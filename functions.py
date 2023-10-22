
#return object associated to a specific name
    def GetObject(list, fieldName, value):
        object = []
        for count, element in enumerate(list):
            if element[fieldName] == value:
                object = list[count]
        return object
              
#return first element (minimax or mini)
    def GetFirstElement(statJson):
        return next(iter(statJson))   

#return true if date format is correct
    def CheckDateFormat(date):
        format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        match = re.match(format, date)
        assert (match != None)  
    

                        
#return value associated to a specific name from config file        
    def GetConfigValue(config_data, name):
        start_index = config_data.find(name)
        if start_index == -1:
            return None
        start_index += len(name) + 1
        end_index = config_data.find("\n", start_index)
        return config_data[start_index+1:end_index].strip() 


    def JsonToList(json_branch, parent_key=''):
        stats_list = {}

        if isinstance(json_branch, dict):
            for name, value in json_branch.items():
                new_key = parent_key + '_' + name if parent_key else name
                stats_list.update(EnvTestLib.JsonToList(value, new_key))
        elif isinstance(json_branch, list):
            for i, item in enumerate(json_branch):
                if isinstance(item, dict) and 'name' in item:
                    component_name = item['name']
                    new_key = parent_key + '_' + component_name if parent_key else component_name
                    stats_list.update(EnvTestLib.JsonToList(item, new_key))
                elif isinstance(item, dict) and 'loc' in item:
                    loc_value = item['loc']
                    prefix = 'body' if loc_value == 'mini' else 'camera'
                    for field, value in item.items():
                        if field != 'loc':
                            new_field = f"{parent_key}_{prefix}_{field}" if parent_key else f"{prefix}_{field}"
                            stats_list[new_field] = value
                else:
                    new_key = parent_key + '_' + str(i) if parent_key else str(i)
                    stats_list.update(EnvTestLib.JsonToList(item, new_key))
        elif isinstance(json_branch, (str, int)):
            stats_list[parent_key] = str(json_branch).lower()

        return stats_list
    
    def GetStatsList(statJson):
        stats_list = []
        stats_dict = EnvTestLib.JsonToList(statJson)
        for object in stats_dict:
            substring_object = str(object[8:]).lower()#supprimer jusqu'au tiret
            stats_list.append([substring_object, stats_dict[object]])
        return stats_list
    
                  
    def GetConfigList(config):
        config_table = []
        for config_field in config['validation']:
            field_name = str(config_field).lower()
            field_value = str(config['validation'][config_field]).lower()
            config_table.append([field_name, field_value])
        return config_table
    
#compare the fields from config file to stats file    
    def CompareConfigToStats(statJson, config):         
        stats_table = EnvTestLib.GetStatsList(statJson)
        config_table = EnvTestLib.GetConfigList(config)
        for config_object in config_table:
            config_object_name = config_object[0]
            config_object_value = config_object[1]
            for stats_object in stats_table:
                stats_object_name = stats_object[0]
                stats_object_value = stats_object[1]
                if (config_object_name == stats_object_name):
                    if (str(config_object_value).lower() != str(stats_object_value).lower()):
                        print(stats_object_name + " non conforme")
                    assert(str(config_object_value).lower() == str(stats_object_value).lower())  
                    break
