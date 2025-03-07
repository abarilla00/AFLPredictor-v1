import csv
from scipy.stats import uniform, triang
import random

class Team:
    """
    Description: Contains all relevant data for each of the teams in the AFL.
    
    Attributes
    ----------
    Name : str [The name of the team]
    TrueAbility : int [A value between 1 (Bad) and 10 (Excellent) that indicates a team's raw skill before calculations]
    3yrWins : int [The team's number of wins over the previous 3 years]
    3yrMatches : int [The team's number of overall matches over the previous 3 years]
    VSRecord : dict [The team's overall record against each of the other teams]
    stadiumAdvantage : dict [The team's overall record at specific venues]
    """

    def __init__(self, name: str, trueAbility: int) -> None:
        self.__name = name
        self.__trueAbility = trueAbility
        self.__3yrWins = 0
        self.__3yrMatches = 0
        self.__VSRecord = dict()
        self.__stadiumAdvantage = dict()

    def updateVSRecord(self, data: list) -> None:
        """
        Description: Updates the VSRecord dictionary for a team when given a list containing the data from a specific match

        Args
        ----
        data : list [A list containing the data from a specific match (Home Team, Away Team, Venue, Scoreline)]
        """

        #Determines if the team in question is the home or away team for a given matchup
        home = True
        if data[0] == self.__name:
            pass
        else:
            home = False

        #Checks if the opposing team has previously been added to the VSRecord dicitonary
        if home:
            opposition = data[1]
            if opposition not in self.__VSRecord:
                self.__VSRecord[opposition] = [0, 0, 0, 0, 0]
        else:
            opposition = data[0]
            if opposition not in self.__VSRecord:
                self.__VSRecord[opposition] = [0, 0, 0, 0, 0]
        
        #Obtains the resulting scoreline from the matchup, the home team's score will always appear first with the away team second regardless of who wins
        result = data[3]
        scores = result.split("-")

        #Determines if the team won, lost, or drew the matchup and adds the result to the VSRecord dictionary
        if home:
            result = int(scores[0]) - int(scores[1])
        else:
            result = int(scores[1]) - int(scores[0])

        #Win
        if result > 0:
            overall = self.__VSRecord[opposition]
            overall[0] = overall[0] + 1
            self.__VSRecord[opposition] = overall
            self.__3yrWins += 1
        
        #Lose
        elif result < 0:
            overall = self.__VSRecord[opposition]
            overall[2] = overall[2] + 1
            self.__VSRecord[opposition] = overall

        #Draw
        else:
            overall = self.__VSRecord[opposition]
            overall[1] = overall[1] + 1
            self.__VSRecord[opposition] = overall
        
        #Updates the win/loss ratio of the team against the opponent and overall +/- result tally
        overall = self.__VSRecord[opposition]
        overall[3] = overall[0] / (overall[0] + overall[1] + overall[2])
        overall[4] = (overall[0] - overall[2])
        self.__VSRecord[opposition] = overall
        self.__3yrMatches += 1  

    def updateStadiumAdvantage(self, data: list) -> None:
        """
        Description: Updates the stadiumAdvantage dictionary for a team when given a list containing the data from a specific match

        Args
        ----
        data : list [A list containing the data from a specific match (Home Team, Away Team, Venue, Scoreline)]
        """
        
        #Determines if the team in question is the home or away team for a given matchup
        home = True
        if data[0] == self.__name:
            pass
        else:
            home = False

        #Checks if the venue has previously been added to the stadiumAdvantage dicitonary
        stadium = data[2]

        if stadium not in self.__stadiumAdvantage:
            self.addStadium(stadium)
        
        #Obtains the resulting scoreline from the matchup, the home team's score will always appear first with the away team second regardless of who wins
        result = data[3]
        scores = result.split("-")

        #Determines if the team won, lost, or drew the matchup and adds the result to the VSRecord dictionary
        if home:
            result = int(scores[0]) - int(scores[1])
        else:
            result = int(scores[1]) - int(scores[0])

        #Win
        if result > 0:
            overall = self.__stadiumAdvantage[stadium]
            overall[0] = overall[0] + 1
            self.__stadiumAdvantage[stadium] = overall
        
        #Lose
        elif result < 0:
            overall = self.__stadiumAdvantage[stadium]
            overall[2] = overall[2] + 1
            self.__stadiumAdvantage[stadium] = overall
        
        #Draw
        else:
            overall = self.__stadiumAdvantage[stadium]
            overall[1] = overall[1] + 1
            self.__stadiumAdvantage[stadium] = overall
        
        #Updates the win/loss ratio of the team at the venue and the overall +/- result tally
        overall = self.__stadiumAdvantage[stadium]
        overall[3] = overall[0] / (overall[0] + overall[1] + overall[2])
        overall[4] = (overall[0] - overall[2])
        self.__stadiumAdvantage[stadium] = overall           
    
    def addStadium(self, stadium: str) -> None:
        """
        Description: Adds a stadium to a team's stadiumAdvantage dictionary

        Args
        ----
        stadium : str [The name of the stadium]
        """

        self.__stadiumAdvantage[stadium] = [0,0,0,0,0]

    def getVSRecord(self) -> dict:
        """
        Description: Returns a team's VSRecord

        """
        return self.__VSRecord
    
    def getTrueAbility(self) -> int:
        """
        Description: Returns a team's trueAbility

        """
        return self.__trueAbility
    
    def getName(self) -> str:
        """
        Description: Returns a team's name

        """
        return self.__name
    
    def getStadiumAdvantage(self) -> dict:
        """
        Description: Returns a team's stadiumAdvantage dictionary

        """
        return self.__stadiumAdvantage
    
    def getWinRate(self) -> float:
        """
        Description: Returns a team's winrate

        """
        return self.__3yrWins / self.__3yrMatches
    
###########################
###########################
###########################

class Match:
    """
    Description: Contains all relevant data for a simulated match
    
    Attributes
    ----------
    homeTeam : str [The name of the home team]
    homeScore : float [The home team's score (Not match score), this value is determined by looking at the the team's ability, record against the opponenet, record at the venue, and form]
    homeRandom : float [The home team's score after randomisation to allow for upsets]
    awayTeam : str [The name of the away team]
    awayScore : float [The away team's score (Not match score), this value is determined by looking at the the team's ability, record against the opponenet, record at the venue, and form]
    awayRandom : float [The away team's score after randomisation to allow for upsets]
    stadium: str [The name of the stadium]
    winner: Team [The winning team]
    upset: bool [Whether the result of the match is an upset]

    """
    def __init__(self, homeTeam: Team, awayTeam: Team, stadium: str) -> None:
        self.__homeTeam = homeTeam
        self.__homeScore = 0
        self.__homeRandom = 0
        self.__awayTeam = awayTeam
        self.__awayScore = 0
        self.__awayRandom = 0
        self.__stadium = stadium
        self.__winner = ""
        self.__upset = False
        
    def calculateWinner(self) -> Team:
        """
        Description: Determines a predicted winner for the matchup and alters their existing records to account for this match

        Return
        ------
        Team [The winning team]

        """

        #Calculates a score for each team based on a team's abilities
        homeScore = self.__homeTeam.getTrueAbility()
        
        stadiumRecord = 0
        
        if self.__stadium in self.__homeTeam.getStadiumAdvantage().keys():
            stadiumRecord = self.__homeTeam.getStadiumAdvantage()[self.__stadium][3]
        
        VSRecord = self.__homeTeam.getVSRecord()[self.__awayTeam.getName()][3]
        winRate = self.__homeTeam.getWinRate()
        homeScore = homeScore + stadiumRecord * 1.2 + VSRecord * 1 + winRate * 0.2
        self.__homeScore = homeScore

        awayScore = self.__awayTeam.getTrueAbility()

        stadiumRecord = 0
        
        if self.__stadium == "ENGIE Stadium" and self.__awayTeam.getName() == "West Coast Eagles":
            pass

        if self.__stadium in self.__awayTeam.getStadiumAdvantage().keys():
            stadiumRecord = self.__awayTeam.getStadiumAdvantage()[self.__stadium][3]

        VSRecord = self.__awayTeam.getVSRecord()[self.__homeTeam.getName()][3]
        winRate = self.__awayTeam.getWinRate()
        awayScore = awayScore + stadiumRecord * 0.8 + VSRecord * 1 + winRate * 0.2
        self.__awayScore = awayScore


        #Determines the winner for the match before randomising scores. This is used to determine if the match was an upset
        winnerPreRandomisation = ""

        if homeScore >= awayScore:
             winnerPreRandomisation = self.__homeTeam
        else:
            winnerPreRandomisation = self.__awayTeam
        
        #Randomising the scores - Needs Improvement
        RandomnessX = random.uniform(-3, 3)
        RandomnessY = random.uniform(-3, 3)

        homeScore = homeScore + RandomnessX + RandomnessY

        RandomnessX = random.uniform(-3, 3)
        RandomnessY = random.uniform(-3, 3)

        awayScore = awayScore + RandomnessX + RandomnessY

        #Overrides the existing scores with the slightly randomised new scores
        self.__homeRandom = homeScore
        self.__awayRandom = awayScore

        #Determining the winner and if the result is an upset
        if(homeScore >= awayScore) and winnerPreRandomisation == self.__homeTeam:
            self.__winner = self.__homeTeam
            self.__upset = False
        elif(homeScore >= awayScore) and winnerPreRandomisation == self.__awayTeam:
            self.__winner = self.__homeTeam
            self.__upset = True
        elif(homeScore < awayScore) and winnerPreRandomisation == self.__homeTeam:
            self.__winner = self.__awayTeam
            self.__upset = True
        else:
            self.__winner = self.__awayTeam
            self.__upset = False

        #Updating records to account for the match in future calculations and returning the resulting teams in order of (winner, loser). The final part of each update (the part the looks like "1 - 0" or "0 - 1") is used as a dummy score for future calculations.
        if(self.__winner == self.__homeTeam):
            self.__homeTeam.updateStadiumAdvantage([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "1 - 0"])
            self.__homeTeam.updateVSRecord([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "1 - 0"])

            self.__awayTeam.updateStadiumAdvantage([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "1 - 0"])
            self.__awayTeam.updateVSRecord([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "1 - 0"])
            return self.__homeTeam, self.__awayTeam
            
        else:
            self.__homeTeam.updateStadiumAdvantage([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "0 - 1"])
            self.__homeTeam.updateVSRecord([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "0 - 1"])

            self.__awayTeam.updateStadiumAdvantage([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "0 - 1"])
            self.__awayTeam.updateVSRecord([self.__homeTeam.getName(), self.__awayTeam.getName(), self.__stadium, "0 - 1"])
            return self.__awayTeam, self.__homeTeam
        
    def getHomeTeam(self) -> Team:
        """
        Description: Returns the home team of a match

        """
        return self.__homeTeam
    
    def getAwayTeam(self) -> Team:
        """
        Description: Returns the away team of a match

        """
        return self.__awayTeam
    
    def getStadium(self) -> str:
        """
        Description: Returns the stadium of a match

        """
        return self.__stadium
    
    def getUpset(self) -> bool:
        """
        Description: Returns if the match was an upset

        """
        return self.__upset
    
    def display(self) -> None:
        """
        Description: Displays the resulting prediction of the match with pre-randomised and post-randomised scores shown

        """
        print(self.__homeTeam.getName(), " VS ", self.__awayTeam.getName(), " @ ", self.__stadium, " WINNER: ", self.__winner.getName(), "|| PRE-RANDOMISATION: ", round(self.__homeScore, 3) ,"-", round(self.__awayScore, 3), "|| POST-RANDOMISATION: ", round(self.__homeRandom, 3) ,"-", round(self.__awayRandom, 3))

###########################
###########################
###########################

class Round:
    """
    Description: Contains all relevant data for a simulated round
    
    Attributes
    ----------
    round : int [The incrementing number of each round]
    matches : list [A list of matches to be played]
    winners : list [The winning teams]
    losers: list [The losing teams]

    """
    def __init__(self, round: int) -> None:
        self.__round = round
        self.__matches = []
        self.__winners = []
        self.__losers = []
        
    def calculateResults(self) -> list:
        """
        Description: Determines a predicted winner for each matchup of a round

        Return
        ------
        list [Contains the list containing the winners, losers and number of upsets from a round]

        """

        upsets = 0

        #Individual match simulations
        for match in self.__matches:
            winner, loser = match.calculateWinner()

            self.__winners.append(winner)
            self.__losers.append(loser)

            if match.getUpset():
                upsets += 1
        
        return self.__winners, self.__losers, upsets

    def generateMatches(self, matches:list, teams:list) -> None:
        """
        Description: Generates the matches for the round based on the fixture
        
        Args
        ----
        matches : list [Contains all the matches to be simulated for a round]
        teams : list [Contains all the teams in a competition]

        """

        homeTeam, awayTeam, stadium = 0, 0, 0


        for match in matches:

            #Checks which teams are fixtured for the match and allocates them as home or away
            for team in teams:
                if team.getName() == match[1]:
                    homeTeam = team
                if team.getName() == match[2]:
                    awayTeam = team
            stadium = match[3]

            #Generates the match
            self.__matches.append(Match(homeTeam, awayTeam, stadium))

    def getRound(self) -> int:
        """
        Description: Returns the round number

        """
        return self.__round
    
    def display(self) -> None:
        """
        Description: Displayes the matches of each round

        """

        for match in self.__matches:
            match.display()
    
###########################
###########################
###########################

class Ladder:
    """
    Description: Stores a team's progress through the season in ladder format
    
    Attributes
    ----------
    ladder : dict [Contains the team name as a key and a tuple containing the team's wins and losses]

    """
    def __init__(self) -> None:
        
        self.__ladder = dict()
    
    def sort(self) -> None:
        """
        Description: Sorts the ladder primarily on win count, and secondarily by alphabetical order

        """

        self.__ladder = dict(sorted(self.__ladder.items(), key=lambda item: (-item[1][0], item[0])))

    def formatLadder(self) -> str:
        """
        Description: Formats the ladder into a string

        Return
        ------
        str [Formatted ladder]

        """
        
        output = ""

        for key in self.__ladder:
            output += key + " " + str(self.__ladder[key][0]) + " " + str(self.__ladder[key][1]) + "\n"

        return output

    def updateLadder(self, winners: list, losers: list) -> None:
        """
        Description: Updates the ladder after a round and sorts it using the sort() function

        Args
        ----
        winners : list [The winning teams from a round]
        losers : list [The losing teams from a round]

        """
        for winner in winners:
            winner = winner.getName()
            self.__ladder[winner] = (self.__ladder[winner][0]+1, self.__ladder[winner][1])
        
        for loser in losers:
            loser = loser.getName()
            self.__ladder[loser] = (self.__ladder[loser][0], self.__ladder[loser][1]+1)
        
        self.sort()

    def initLadder(self, teams: list) -> None:
        """
        Description: Initialises the ladder with each team

        Args
        ----
        teams : list [All teams in the competition]

        """
        for team in teams:
            self.__ladder[team.getName()] = (0,0)
    

###########################
###########################
###########################

class Controller:
    """
    Description: Controls the functionality of the everall system
    
    Attributes
    ----------
    matches : list [Contains all the matches to be predicted for the season]
    teams : list [All teams in the league]
    ladder : Ladder [The season's ladder]

    """
    def __init__(self) -> None:
        self.__matches = self.readCSV('afl-2025-UTC.csv')
        self.__teams = self.generateTeams()
        self.__ladder = Ladder()
    
    def generateTeams(self) -> list:
        """
        Description: generates default team objects for every team in the league

        Return
        ------
        list [Generated teams]

        """

        teamInputs = {"Adelaide Crows" : 6,
                      "Brisbane Lions" : 9,
                      "Carlton" : 6,
                      "Collingwood" : 7,
                      "Essendon" : 4,
                      "Fremantle" : 8,
                      "Geelong Cats" : 8,
                      "Gold Coast Suns" : 5,
                      "GWS Giants" : 7,
                      "Hawthorn" : 8,
                      "Melbourne" : 5,
                      "North Melbourne" : 3,
                      "Port Adelaide" : 6,
                      "Richmond" : 1,
                      "St Kilda" : 3,
                      "Sydney Swans" : 8,
                      "West Coast Eagles" : 3,
                      "Western Bulldogs" : 5}
        teams = []

        #Adds each team and their ability to the controller's teams list
        for teamName, ability in teamInputs.items():
            teams.append(Team(teamName, ability))
        
        return teams
    
    def setParams(self) -> None:
        """
        Description: Sets a team's parameters using data from the previous 3 years
        
        """
        
        #Concatonates all the matches played over the previous 3 years into a single list of matches
        yr2024 = self.readCSV('afl-2024-UTC.csv')
        yr2023 = self.readCSV('afl-2023-UTC.csv')
        yr2022 = self.readCSV('afl-2022-UTC.csv')
        stadiumNameCheck = self.readCSV('stadium-name-changes.csv')

        last3years = yr2024 + yr2023 + yr2022
        
        for match in last3years:
            homeTeam = match[0]
            awayTeam = match[1]

            #updates the team's parameters after each match
            for team in self.__teams:
                if team.getName() != homeTeam and team.getName() != awayTeam:
                    continue
                
                #Ensures the program only uses the most current name of a stadium
                currentStadiumName = self.checkStadiumName(match[2], stadiumNameCheck)
                match[2] = currentStadiumName

                team.updateVSRecord(match)
                team.updateStadiumAdvantage(match)
                
        
        #Debug Code for viewing team parameters
        for team in self.__teams:
           print(team.getName(), " ", team.getStadiumAdvantage())
           print(team.getName(), " ", team.getVSRecord())
           print()
    
    def initLadder(self) -> None:
        """
        Description: Initialises the season's ladder
        
        """

        self.__ladder.initLadder(self.__teams)
    
    def predict(self) -> None:
        """
        Description: Peforms predictions for each match in the season
        
        """

        roundNum = 0

        #Loops through the season's remaining matches
        while self.__matches:

            roundMatches = []
            round = Round(roundNum)

            for match in self.__matches:

                #Checks if the matches belong in the same round
                if int(match[0]) == roundNum:
                    roundMatches.append(match)
                else:
                    break
            
            #Removes the matches in the current round from the existing season matches list
            for match in roundMatches:
                self.__matches.remove(match)

            #Match generation, prediction, and ladder updates for the round
            round.generateMatches(roundMatches, self.__teams)
            roundWinners, roundLosers, upsets = round.calculateResults()
            self.__ladder.updateLadder(roundWinners, roundLosers)

            #Round displaying
            print("\n-=-Round " + str(roundNum) + "-=-\n")
            round.display()
            print("\nRound Upsets: ", upsets)
            print("\nPost-Round Ladder\n\n" + self.__ladder.formatLadder())
            
            roundNum += 1


    def readCSV(self, fileName: str) -> list:
        """
        Description: Imports csv files

        Args
        ----
        filename : str [The filename of the csv file]

        Return
        ------
        list [List of matches (rows) from the csv file]
        
        """

        file = open(fileName)
        rows = []
        csvreader = csv.reader(file)

        for row in csvreader:
            rows.append(row)
        
        return rows
    
    def checkStadiumName(self, stadium: str, stadiumNamesList: list) -> str:
        """
        Description: Converts old stadium names from previous years to the current name of the stadium if necassary.

        Args
        ----
        stadium : str [The name of the stadium being checked]
        stadiumNamesList : list [A list containing sub-lists with historical stadium names]

        Return
        ------
        str [The current name of the stadium in question]
        
        """

        for stadiumNames in stadiumNamesList:
            if stadium in stadiumNames:

                #the first index of the sub-list will always be the current stadium name
                return stadiumNames[0]
        

#Program Start
if __name__ == '__main__':
    controller = Controller()
    controller.setParams()
    controller.initLadder()
    controller.predict()