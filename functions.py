    def GetModel(statJson):
        return next(iter(statJson))   

#return true if date format is correct
    def CheckDateFormat(date):
        format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        match = re.match(format, date)
        assert (match != None)  

#return table containing all (key, value) from stats.json
    def GetStatsTable(statJson, model):
        possible_box_name = ['mini']#à remplir
        stats_table = []
        stats_table.append(['boxType'.lower(), statJson[model]['boxType']])
        stats_table.append(['coreVersion'.lower(), statJson[model]['coreVersion']])   
        for hardware in statJson[model]['hardware']:
            for object in statJson[model]['hardware'][hardware]:
                if type(object) == str:
                    field_name = f"hardware_{hardware}_{object}".lower()
                    field_value = statJson[model]['hardware'][hardware][object]
                    stats_table.append([field_name, field_value])
                elif (hardware == 'board'):
                    field_name = f"hardware_{hardware}_{object['name']}".lower()
                    field_value = object['id']
                    stats_table.append([field_name, field_value])
                elif (hardware == 'sd'):
                    for field in object:
                            if (object['loc'] in possible_box_name):
                                field_name = f"hardware_{hardware}_box_{field}".lower() 
                            else:
                                field_name = f"hardware_{hardware}_camera_{field}".lower()
                            field_value = object[field]
                            stats_table.append([field_name, field_value])    


        for software in statJson[model]['software']['release']:
            for field in software:
                if field != 'name':
                    field_name = f"software_{software['name']}_{field}".lower()
                    field_value = software[field].lower()
                    stats_table.append([field_name, field_value])
        return stats_table
              

#compare the fields from config file to stats file    
    def CompareConfigToStats(statJson, config, model):         
        stats_table = EnvTestLib.GetStatsTable(statJson, model)
        config_table = []
        for config_field in config['validation']:
            field_name = config_field.lower()
            field_value = config['validation'][config_field]
            config_table.append([field_name, field_value])
        for i, config_object in enumerate(config_table):
            config_object_name = config_object[0]
            config_object_value = config_object[1]
            for j, stats_object in enumerate(stats_table):
                stats_object_name = stats_object[0]
                stats_object_value = stats_object[1]
                if (config_object_name == stats_object_name):
                    if (str(config_object_value).lower() != str(stats_object_value).lower()):
                        print(stats_object_name + " non conforme")
                    assert(str(config_object_value).lower() == str(stats_object_value).lower())  
                    config_table.pop(i)
                    stats_table.pop(j) 
                    break
                        
#return value associated to a specific name from config file        
    def GetConfigValue(config_data, name):
        start_index = config_data.find(name)
        if start_index == -1:
            return None
        start_index += len(name) + 1
        end_index = config_data.find("\n", start_index)
        return config_data[start_index+1:end_index].strip() 
