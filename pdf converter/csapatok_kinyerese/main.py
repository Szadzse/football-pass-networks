def get_teams():
    with open('data.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    team_names = []
    for line in lines[1:]:
        data = line.strip().split('\t')
        team_name = data[1]
        team_names.append(team_name)

    print(team_names)
    return team_names
