with open('stats_example.json', 'r') as stats_json:
            stats_data = json.load(stats_json)

stats_table = EnvTestLib.GetStatsTable(stats_data, 'minimax')
model = EnvTestLib.GetModel(stats_data)
#pprint(stats_table)

EnvTestLib.CompareConfigToStats(stats_data, config, model)
