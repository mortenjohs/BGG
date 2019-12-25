## pip install boardgamegeek2

from boardgamegeek import BGGClient

bgg = BGGClient()

year        = 2019
player_name = 'mortenjohs'

plays = bgg.plays(player_name)

games = {}

for p in plays:
    is_new  = False
    if p.date.year == year:
        for pl in p.players:
            if pl.username == player_name:
                if pl.new == "1":
                    games[p.game_id] = bgg.game(game_id=p.game_id)

games = {k: v for k, v in sorted(games.items(), key=lambda item: item[1].name)}

print("name,id,year,rank,rating_avg")

for k, v in games.items():
    print(v.name + "," + str(k) + "," + str(v.year) + "," + str(v.bgg_rank) + "," + str(v.rating_average))