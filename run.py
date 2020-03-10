#Bobby Crawford - CS 98 Hackathing 1

#import all necessary modules
from generate_dk_csv import generate_csv
from scrape_rotogrinders_predictions import scrape_rotogrinders_predictions
from solver import solve

#generate final csv to be used for DraftKings
scrape_rotogrinders_predictions()
a = solve(5, 7, 'rotogrinders_predictions.csv', 'teams.csv')
generate_csv(a)
