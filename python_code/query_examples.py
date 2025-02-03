#%%
from opta_models_functions import database_session
from opta_models import OptaMatch, OptaEvent, OptaQualifier, OptaEventPassOption
from sqlalchemy.orm import joinedload
from typing import List

#%%
session = database_session()

#example query

matches = session.query(OptaMatch).all()

print(len(matches))
#%%

#get events for a Vejle - Brøndby Match
MATCH_ID = 2769

match = session.query(OptaMatch).filter(OptaMatch.id == MATCH_ID).first()

match_events: List[OptaEvent] = match.events

event: OptaEvent = match_events[0]

for event in match.events:
    print(event.player.first_name)

#%%

#%%
# Get all events for a player

PLAYER_ID = 2619

for event in match.events:
    if event.player.id == PLAYER_ID:
        print(event.id)
# %%


eager_loaded_match = session.query(OptaMatch).options(
        joinedload(OptaMatch.events)
        ).filter(OptaMatch.id == match.id).first()

#%%

#Nuværende sæson
eager_loaded_match = session.query(OptaMatch).options(
        joinedload(OptaMatch.events)
        .joinedload(OptaEvent.qualifiers)
        .joinedload(OptaQualifier.qualifier_values),
        ).filter(OptaMatch.season_id == 21).all()

# %%



print(len(eager_loaded_match))
# %%

# 2023-2024 sæson
eager_loaded_match = session.query(OptaMatch).options(
        joinedload(OptaMatch.events)
        .joinedload(OptaEvent.qualifiers)
        .joinedload(OptaQualifier.qualifier_values),
        ).filter(OptaMatch.season_id == 22).all()

print(len(eager_loaded_match))

# %%

# 2022-2023 sæson
eager_loaded_match = session.query(OptaMatch).options(
        joinedload(OptaMatch.events)
        .joinedload(OptaEvent.qualifiers)
        .joinedload(OptaQualifier.qualifier_values),
        ).filter(OptaMatch.season_id == 23).all()

print(len(eager_loaded_match))

# %%