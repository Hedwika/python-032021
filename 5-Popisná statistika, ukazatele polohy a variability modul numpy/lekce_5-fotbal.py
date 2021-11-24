import itertools


team_list = ["FK Bohemia Kaznějov", "TJ Sokol Kozolupy", "TJ Sokol Plasy", "Tatran Třemošná", "TJ Sokol Plasy", "TJ Nečtiny"]
print(itertools.permutations(team_list, 3))
print(list(itertools.permutations(team_list, 3)))