# pip install boardgamegeek2

from boardgamegeek import BGGClient
from boardgamegeek import CacheBackendSqlite

bgg = BGGClient()
bgg_sqlite_cache = BGGClient(cache=CacheBackendSqlite(path="./cache.db", ttl=3600))

year = 2019
player_name = 'mortenjohs'

user = bgg.user(player_name)
# temp_collection = bgg.collection(player_name)

# collection 

plays = bgg.plays(player_name)

games = {}
mechanics = {}
categories = {}

for p in plays:
	is_new = False
	if p.date.year == year:
		for pl in p.players:
			if pl.username == player_name:
				if pl.new == "1":
					games[p.game_id] = bgg_sqlite_cache.game(game_id=p.game_id)
					
games = {k: v for k, v in sorted(games.items(), key=lambda item: item[1].name)}

for g in games.values():
	for m in g.mechanics:
		mechanics.setdefault(m, 0)
		mechanics[m] += 1
	for c in g.categories:
		categories.setdefault(c, 0)
		categories[c] += 1
		
mechanics = { k: v for k, v in sorted(mechanics.items(), key=lambda item: -item[1]) }
categories = { k: v for k, v in sorted(categories.items(), key=lambda item: -item[1]) }

print("name,id,year,rank,rating_avg,weight")

for k, v in games.items():
	print(
	v.name + "," +
	str(k) + "," +
	str(v.year) + "," +
	str(v.bgg_rank) + "," +
	str(v.rating_average) + "," +
	str(v.rating_average_weight)
	)

