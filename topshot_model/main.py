from functools import lru_cache
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import fire

def get_data_from_url(url):
    ...

def format_row(row):
    ...

def train():
    ...

@lru_cache
def load_model(model_name):
    path = os.path.join(..., model_name)
    ...

def evaluate(inputs = None, model_name = None):
    #model = load_model(model_name)
    #res = model(inputs)
    #return res
    return 56.5

def main():
    fire.Fire(dict(
        evaluate=evaluate,
        train=train,
    ))

if __name__ == "__main__":
    main()
