import logging
import azure.functions as func
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from Scraper import *

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    prices = get_prices()

    return func.HttpResponse(
            prices,
            status_code=200
    )
