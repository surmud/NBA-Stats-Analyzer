from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt

import numpy as np

#given a player's age and their performance in certain categories, give a projection of their future stats
def projectFutureStats(name, age, category, seasons):

    #nba player's prime: roughly at age 27-31
    yearsInLeague = range( len(seasons))

    #if they are younger than 25, they probably haven't reached their peak yet so calculate linear regression
    if age < 27:
        mymodel = np.poly1d(np.polyfit(yearsInLeague, category, 1))

    #otherwise, most players fit a quadratic curve if they are past their peak
    else:
        mymodel = np.poly1d(np.polyfit(yearsInLeague, category, 2))


    myline = np.linspace(0, 30, len(seasons) + 5, False)
    
    plt.title(name+"'s projected stats for the future")
    plt.scatter(yearsInLeague, category, c = "r")
    plt.plot(myline, mymodel(myline), "--")
    plt.xlim(0, len(seasons) + 5)
    plt.ylim(0, 40)
    plt.xticks(range(0, len(seasons) + 5, 2))
    plt.xlabel("Number of Seasons in the League")
    plt.ylabel("Number of Points Scored")
    plt.show()


def main():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # These three lines are to stop the browser window from opening
    
    name = input("\nEnter the name of the player: ")
    nameCopy = name
    name = name.lower()
    name = name.split(" ") #split into first and last name

    #structure of a basketball reference url: https://www.basketball-reference.com/players/lastInitial/lastNameFirstTwolettersoffirstname01.html
    #the url is also structured so that up to the first 5 characters of the last name are used
    
    if(len(name) == 2):
        firstName = name[0]
        lastName = name[1]
    
    else:
        print("Invalid name entered.")
        return 0

    lastInitial = lastName[0]
    lastName = lastName[:5]
    firstName = firstName[0]+firstName[1]
    name = lastName+firstName

    url = "https://www.basketball-reference.com/players/"+lastInitial + "/" + name + "01.html"
    
    print("Loading player data...")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

    except:
        print("Couldn't find data for that player")
        main()

    table = driver.find_element_by_id("totals")
    table = table.text 
    driver.quit()
    table = table.split("\n")
    
    
    seasons = [] #index 0
    age = []     #index 1
    gamesPlayed = [] #5
    gamesStarted = [] #6
    minutesPlayed = [] #7
    fieldGoals = [] #8
    fieldGoalsAttempted = [] #9
    fieldGoalPercentage = [] #10 
    threePtrs = [] #11
    threePtrsAttempted = [] #12
    threePtrsPercentage = [] #13
    freeThrows = [] #18
    freeThrowPercentage = [] #20
    offensiveRebounds = [] #21
    defensiveRebounds = [] #22
    totalRebounds = [] #23
    assists = [] #24
    steals = [] #25
    blocks = [] #26
    turnovers = [] #27
    personalFouls = [] #28
    points = [] #29
    tripleDoubles= [] #30
    pointsPerGame = []
    assistsPerGame = []
    reboundsPerGame = []
    blocksPerGame = []
    stealsPerGame = []
    subtotals = []

    endReached = False
    endingRow = -1
    listCount = 0
    try:
        for i in range(len(table)):
            
            #split the list up by its whitespace
            table[i] = table[i].split(" ")

            #find the end of the list by looking for the current season, since it continues into a sub table
            if table[i][0] == "Career":
                endReached = True

            if i > 0 and endReached == False:

                table[i][0] = "'"+table[i][0][2:]
                seasons.append(table[i][0][0:3])
                age.append(int(table[i][1]))
                gamesPlayed.append(int(table[i][5]))
                gamesStarted.append(int(table[i][6]))
                minutesPlayed.append(int(table[i][7]))
                fieldGoals.append(int(table[i][8]))
                fieldGoalsAttempted.append(int(table[i][9]))
                fieldGoalPercentage.append(float(table[i][10]) * 100)
                threePtrs.append(int(table[i][11]))
                threePtrsAttempted.append(int(table[i][12]))
                threePtrsPercentage.append(float(table[i][13]))
                freeThrows.append(int(table[i][18]))
                freeThrowPercentage.append(float(table[i][20]))
                offensiveRebounds.append(int(table[i][21]))
                defensiveRebounds.append(int(table[i][22]))
                totalRebounds.append(int(table[i][23]))
                assists.append(int(table[i][24]))
                steals.append(int(table[i][25]))
                blocks.append(int(table[i][26]))
                turnovers.append(int(table[i][27]))
                personalFouls.append(int(table[i][28]))
                points.append(int(table[i][29]))
                #tripleDoubles.append(int(table[i][30]))
                pointsPerGame.append(points[listCount]/gamesPlayed[listCount])
                assistsPerGame.append(assists[listCount]/gamesPlayed[listCount])
                reboundsPerGame.append(totalRebounds[listCount]/gamesPlayed[listCount])
                stealsPerGame.append(steals[listCount]/gamesPlayed[listCount])
                blocksPerGame.append(blocks[listCount]/gamesPlayed[listCount])
                subtotals.append(pointsPerGame[listCount] + assistsPerGame[listCount] + reboundsPerGame[listCount] + blocksPerGame[listCount] + stealsPerGame[listCount])
                listCount += 1

    except:
        print(nameCopy +"/'s stats aren't complete on basketballreference.com for me to make a graph")
        main()
        return
   
    
    startSeason = seasons[0]
    startSeason = int(startSeason[1:3])
    if startSeason < 35:
        startSeason += 2000
    else:
        startSeason += 1900
        
    
    
    plt.ylim(0, 50)
    plt.plot(seasons, pointsPerGame, marker = ".")
    plt.plot(seasons, assistsPerGame, marker = ".")
    plt.plot(seasons, reboundsPerGame, marker = ".")
    plt.plot(seasons, stealsPerGame, marker = ".")
    plt.plot(seasons, blocksPerGame, marker = ".")
    

    plt.legend(["Points per game", "Assists per game", "Rebounds per game", "Steals per game", "Blocks per game"])
    plt.title(nameCopy+"'s career stats per game")
    plt.show()
    
    age = age[len(age) - 1]

    projectFutureStats(nameCopy, age, pointsPerGame, seasons)
    
    again = input("Do you want to enter in another player? (type y or n): ")
    if(again == "y"):
        main()


main()