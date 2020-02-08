# pip install boardgamegeek2

from boardgamegeek import BGGClient
from boardgamegeek import CacheBackendSqlite
from boardgamegeek import exceptions
import time

bgg = BGGClient()
bgg_sqlite_cache = BGGClient(cache=CacheBackendSqlite(path="./cache.db", ttl=86400)) # ttl = 1 day (60 s * 60 m * 24 h) Does this even work?

year = 2019
user_name = 'mortenjohs'
other_player_names = ["Gab", "Nina", "Jean", "Pierrot", "Florent", "Clem", "Laure"]

user = bgg_sqlite_cache.user(user_name)
# temp_collection = bgg.collection(user_name)
# collection 

plays = bgg_sqlite_cache.plays(user_name)

games = {}
mechanics = {}
categories = {}

def get_game(id, bgg_client):
  try:
    return bgg_client.game(game_id=id)
  except boardgamegeek.exceptions.BGGApiError as e:
    print(e)
    print("\nBGG limit reached? -- Sleeping for 60 seconds")
    time.sleep(60) # sleep for one minute -- is that enough?

for p in plays:
  is_new = False
  if p.date.year == year:
    for pl in p.players:
      if pl.username == user_name:
        if pl.new == "1":
          print(".", end ="") 
          games[p.game_id] = get_game(p.game_id,bgg_sqlite_cache)

games_others = {}

for name in other_player_names:
  games_others[name] = {}
  for p in plays:
    is_new = False
    if p.date.year == year:
      for pl in p.players:
        if pl.name == name:
          if pl.new == "1":
            print(".", end ="")
            games_others[name][p.game_id] = get_game(p.game_id,bgg_sqlite_cache)
        
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

print("\nName,id,Year,Rank,Rating (avg),Weight")

for k, v in games.items():
  print(
  v.name + "," +
  str(k) + "," +
  str(v.year) + "," +
  str(v.bgg_rank) + "," +
  str(v.rating_average) + "," +
  str(v.rating_average_weight)
  )

for name in other_player_names:
  print("\n" + name + "("+ str(len(games_others[name].items())) + "): " + str([i.name for k,i in games_others[name].items()]))