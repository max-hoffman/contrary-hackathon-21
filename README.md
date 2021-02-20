# contrary-hackathon-21

## Summary

[NBA Topshot](https://www.nbatopshot.com/marketplace) price correctness classifier.

## TODO:

- [ ] Web scrape 10 pieces of data ([format](#data-format))
- [ ] Get data formatting fn to work for train + eval time
- [ ] Run training step w/ simple [tree model](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html) or [xboost](https://xgboost.readthedocs.io/en/latest/get_started.html)
- [ ] Make sure model is doing what we want it to do before complexifying/adding more data
- [ ] CLI to run evaluation given URL
- [ ] [Flask](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)/[FastAPI](https://fastapi.tiangolo.com) site for visualizing eval
- [ ] Deploy on AWS


## Dependencies

[poetry](https://python-poetry.org/docs/#installation)
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
```

[terraform (click link)](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## Data Format:

1. Cards should have a minimum age (1 month?)

2. Collect fields from html nodes
```
player stats:
MIN	PTS	FGM	FGA	FG%	3PM	3PA	3P%	FTM	FTA	FT%	OREB	DREB	REB	AST	TOV	STL	BLK	PF	+/-

final scores:
player_score opp_score

other:
card_age
target price (not an input feature)
```

3. Formalize feature names:
```python3
name_map = dict(
    MIN="minutes",
    PTS="points",
    FGM="",
    FGA="field_goal_attempts",
    FG%="",
    3PM="",
    3PA="",
    3P%="",
    FTM="",
    FTA="",
    FT%="",
    OREB="",
    DREB="",
    REB="",
    AST="",
    TOV="",
    STL="",
    BLK="",
    PF="",
    "+/-"="plus_minus",
)
```

4. Cleaning:
  - Convert percentages to 0.0-1.0
  - Convert minutes to seconds
  - Remove duplicates
  - Remove rows will nulls

5. Train/test splits -- does card age affect?
