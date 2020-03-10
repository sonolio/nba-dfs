# Hack A Thing 1: DraftKings Lineup Generator
## Paolo Takagi-Atilano and Bobby Crawford

**What we made:**

For our first Hack A Thing, we decided to create a program that would generate (optimized) lineups for DraftKings NBA Daily Fantasy games.  

**Points Projections:**

For starters, we needed to find a way to try to predict the number of points that a NBA player would score in the upcoming competition.  Since we were more focused on making a program that optimized lineups given projections, we decided to use the projections created by RotoGrinders, rather than create our own.  We were able to accomplish this using the `urlretrieve` function from the `urllib.request` module.  Luckily the downloaded data also included necessary information about each player such as their salary, position, team, and name (in addition to points projections).  Bobby wrote the scraping functionality.

**Constraint Satisfaction Problem:**

Now that we have predicitons about a players performance in the upcoming daily fantasy sports contest, we wanted to create a way to generate valid lineups optimized for projected points.  We decided to formulate this problem as a Constaint Satisfaction Problem (CSP), and use the `PuLP` library to do this task.  

First, Bobby wrote the `data_handling` module, which read the input from the scraped rotogrinders predictions into a pandas dataframe for use in the CSP solver.  The data was slightly refactored to enable integer programming to solve it.

Next, Paolo wrote the functionality to add constraints to the model that make sure that each lineup fit position constraints (i.e. one point guard, one shooting guard, etc.), as well as the logic to fit within the DraftKings budget, and to optimize for projected points.  Then Paolo also wrote the funcitonality to add an overlap constraint.  This was inspired from the Picking Winners Using Integer Programming (see sources).  The idea of an overlap constraint was without it, the model would return the exact same lineup (optimal with respect to the points projections) every time it was ran. But with an overlap constraint, there was a cap on the number of players that any two lineups could share, forcing the model to find novel lineups.  This allows for a diversification between players, so that we are more likely to have a scoring lineup at the end of the day.  

Then, Bobby wrote the `solver` module which actually included the `PuLP` model to solve for lineups.  It ran a parametrized number of times, first adding the feasability (positional) constraints, and then each subsequent time adding the newest overlap constraint to the model.  At the end of each iteration, it added the solution lineups (in the form of a pandas dataframe) to a list, which it finally returned.

**Generating DraftKings CSV file:**

Next, Paolo wrote the logic for generating the DraftKings csv file for uploading to the website (so that many lineups do not have to be hand-entered by the user).  It first had to associate each player with their correct position, which it did by performing a depth-first search.  Next, it used the a provided Draftkings document to convert each player's name to the corresponding id that DraftKings uses.  Here is where we discovered that there was a discrepancy between the names of players that DraftKings uses compared to Rotogrinders (i.e. "Bruce Brown" or "Bruce Brown Jr.").  In order to solve this, we wrote a prompt that displayed the rotogrinders name, and asked the user to input the correct DraftKings name of that user (and then verified the input).  An escape option was also included in the prompt (inputting `~~~~`), in which case the lineup was discarded.  The mapping from Rotogrinders player names to DraftKings player names was saved in a json file called `player_names.json`, for future use (current version is part of the git repo).  All of these was used to create a file called `dk_upload.csv` that is a list of lineups (by player ids), in the correct format mandated by DraftKings for uploading.

Finally, Bobby wrote the `run` module, which put all of the above methods and functionality into a single script that executed the entirety of the program, and Paolo wrote the `README.md`.

**What we learned**

We learned how to use the `urllib` library to scrape datasets from websites, how to use `PuLP` to solve constraint satisfaction problems, and how to use `pandas` to load and manipulate datasets.

**What didn't work:**

We tried to automate the process as much as possible, we found that scraping DraftKings was difficult, as well as not allowed by their terms and service (so best to be avoided anyways).  As such, there are two pieces of data that are needed to be collected manually before the program is ran.  First, the `teams.csv` file that indicates the teams from which you are alowed to use players on (different DraftKings competitions at different times use different teams, so without this its posisble that lineups would use players that aren't actually part of that particular competition and thus be invalid).  Second, the `dk_salaries.csv` file that maps DraftKings player names to their corresponding ids to upload.  In hindsight, we could have extracted the list of valid teams from the `dk_salaries.csv` file, thus making only one necessary item for manual download.  This could be a next step.  Other next steps would be finding a way to test how good our generator actually is, perhaps by building a backtesting suite.

We included an exmaple `teams.csv` and `dk_salaries.csv` in the git repo, so that one could see the format of these files.  Note that `teams.csv` needs to be manually entered and `dk_salaries.csv` need to be downloaded from DraftKings (for the corresponding competition), and then moved into the folder of the git repo, and renamed to `dk_salaries.csv`.  Also included in the git repo is a picture called `proof.png`, which is a screenshot of succesfully uploading 100 out of 100 DraftKings lineups from a csv file generated by our scripts.

**Sources:**

* http://www.mit.edu/~jvielma/publications/Picking-Winners.pdf
* http://benalexkeen.com/linear-programming-with-python-and-pulp-part-5/
