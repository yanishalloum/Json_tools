def GetConfigValue(data, field):
    start_index = data.find(field)
    if start_index == -1:
        return None

    start_index += len(field) + 1
    end_index = data.find("\n", start_index)
    return data[start_index:end_index].strip()
