#Bobby Crawford, CS 98 - Hackathing 1

#import all necessary modules
import datetime
import time
import os

from urllib.request import urlretrieve

#target url for rotogrinder nba player projections
url = 'https://rotogrinders.com/projected-stats/nba-player.csv?site=draftkings'
destination = 'rotogrinders_predictions.csv'

#scraping function for target url
def scrape_rotogrinders_predictions():
    urlretrieve(url, destination)
