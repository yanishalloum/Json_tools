    # Merge two dict together.
    def merge_two_dicts(dict1, dict2):
        merged_dict = {**dict1, **dict2}
        return merged_dict
 
    # Merge a variable number of dicts together.
    def merge_dicts(*args):
        final_merged_dict = {**args[0]}
        for dict in args[1:]:
            merged_dict = EnvTestLib.merge_two_dicts(final_merged_dict, dict)
            final_merged_dict = merged_dict
        return final_merged_dict

#Return the differences between two .json excluding some fields.  
    def GetDiffJson(new_firmware_stat_json, old_firmware_stat_json, fields_to_exclude: list):
        """When this code was written:
        feature "include_paths" did not work for nested .json.
        feature "exclude_paths" did not work when "ignore_order" == True."""
        diff = DeepDiff(new_firmware_stat_json, old_firmware_stat_json, exclude_paths=fields_to_exclude)
        return diff
 
    #Return .tasks parsed by lines
    def parse_tasks(tasks: str): 
        #"[:-1]" because last cronline is empty.
        parsed_tasks = tasks[:-1].split('\n') 
        return parsed_tasks 

    #Return (cron, command) from a .tasks line.
    def get_cron_and_command(task):
        #Find the first letter to appear in the word. 
        match = re.compile("[^\W\d]").search(task)
        #Strictly before that letter is the cron and after is the command.
        return [task[:match.start()], task[match.start():]] 
                        
    #Check if certain lines are present in a tasks file.
    def are_lines_in_tasks_file(task_lines, tasks):
        task_lines = EnvTestLib.parse_tasks(task_lines)
        for task in task_lines:
            if not (task in tasks):
                return False
        return True   

    #Return lines from tskerr file.
    def get_tskerr_lines(tskerr): 
        tskerr = EnvTestLib.parse_tasks(tskerr) 
        parsed_tskerr = [] 
        for tskerr_lines in tskerr: 
            index = tskerr_lines.find(":")  
            if index != -1: 
                parsed_tskerr.append(tskerr_lines[index+1:].strip())  
        return parsed_tskerr

    #More specific version of GetObject.                   
    def get_object_specific(json_branch, field_name1: str, value1, field_name2: str, value2):
            object = []
            for count, element in enumerate(json_branch):
                if (element[field_name1] == value1) and (element[field_name2] == value2):
                    object = json_branch[count]
                    break
            return object 

#Return object associated to a specific value.
    def GetObject(json_branch, field_name: str, value):
        object = []
        for count, element in enumerate(json_branch):
            if element[field_name] == value:
                object = json_branch[count]
                break
        return object
              
    #Return box form factor (minimax or mini).
    def GetBoxFormFactor(stat_json)-> str:
        #Return the very first field of the Json which is the box form factor: "minimax" or "mini".   
        return next(iter(stat_json))
