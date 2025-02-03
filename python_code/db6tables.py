from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Date, Numeric, DateTime
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Dictionary to standardize column definitions
def create_columns():
    return {
        "Id": Column(Integer, primary_key=True),
        "int": Column(Integer),
        "string": Column(String(length=100)),
        "date": Column(Date),
        "decimal": Column(Numeric(10, 2)),
        "timestamp": Column(DateTime, default=datetime.utcnow),
    }

columns_dict = create_columns()

class CoachMetric(Base):
    __tablename__ = "coach_metrics"

    metric_id = Column(Integer, primary_key=True)
    coach_id = Column(Integer, ForeignKey("head_coach.coach_id"))
    rating = Column(Numeric(10, 2))
    tactical_style = Column(String(length=100))
    rating_change_12m = Column(Numeric(10, 2))
    suitability = Column(Numeric(10, 2))
    team_rating_impact = Column(Numeric(10, 2))
    trust_in_youth = Column(Numeric(10, 2))
    preferred_formation = Column(String(length=100))
    squad_rotation = Column(Numeric(10, 2))
    avg_transfer_spend = Column(Numeric(10, 2))

    coach = relationship("HeadCoach", back_populates="metrics")

    def __repr__(self):
        return f"CoachMetric(metric_id={self.metric_id}, rating={self.rating})"

class HeadCoach(Base):
    __tablename__ = "head_coach"

    coach_id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    birth_date = Column(Date)
    nationality1 = Column(String(length=100))
    nationality2 = Column(String(length=100), nullable=True)
    current_team_id = Column(Integer, ForeignKey("teams.team_id"))
    current_role = Column(String(length=100))
    contract_expiry = Column(Date)
    agency_id = Column(Integer, ForeignKey("agencies.agency_id"), nullable=True)

    metrics = relationship("CoachMetric", back_populates="coach")

    def __repr__(self):
        return f"HeadCoach(coach_id={self.coach_id}, name={self.name})"

class Players(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    birth_date = Column(Date)
    first_position = Column(String(length=100))
    nationality1 = Column(String(length=100))
    nationality2 = Column(String(length=100), nullable=True)
    current_team_id = Column(Integer, ForeignKey("teams.team_id"))
    parent_team = Column(String(length=100), nullable=True)
    competition_id = Column(Integer, ForeignKey("competition.competition_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))

    def __repr__(self):
        return f"Player(player_id={self.player_id}, name={self.name})"

class PlayersCompetition(Base):
    __tablename__ = "players_competition"

    player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)
    competition_id = Column(Integer, ForeignKey("competition.competition_id"), primary_key=True)
    division_level = Column(Integer)

    def __repr__(self):
        return f"PlayersCompetition(player_id={self.player_id}, competition_id={self.competition_id})"

class TeamHistory(Base):
    __tablename__ = "team_history"

    team_history_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    entity_type = Column(String(length=100))

    def __repr__(self):
        return f"TeamHistory(team_history_id={self.team_history_id}, player_id={self.player_id})"

class PlayerMetrics(Base):
    __tablename__ = "player_metrics"

    metrics_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.player_id"))
    salary = Column(Numeric(10, 2))
    contract_expiry = Column(Date)
    playing_style = Column(String(length=100))
    xtv = Column(Numeric(10, 2))
    player_rating = Column(Numeric(10, 2))
    player_potential = Column(Numeric(10, 2))
    gbe_status = Column(String(length=100))
    minutes_played = Column(Numeric(10, 2))

    def __repr__(self):
        return f"PlayerMetrics(metrics_id={self.metrics_id}, player_id={self.player_id})"
