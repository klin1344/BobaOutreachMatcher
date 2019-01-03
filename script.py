"""
An script to match teams with questions based on difficulty and category of questions and 
confidence of teams.  Takes a greedy approach.

Authors:

Kevin Lin
Titus Deng
"""

import csv
import numpy as np
import math

TEAM_DATA_CSV = 'Fall 2018 Team_Question Data - Team Data.csv'
QUESTION_DATA_CSV = 'Copy3 of Fall 2018 Questions - Responses.csv'
TOPICS = ['Bible',
          'Character of God',
          'Comparative Religion',
          'Central Tenets',
          'Church History',
          'Science & Faith',
          'Social Issues',
          'Spiritual Disciplines',
          'Trinity',
          'Personal Testimony']


class teamObject:
    def __init__(self, teammate1, teammate2, confidence):
        self.teammate1 = teammate1
        self.teammate2 = teammate2
        self.breadth = None
        self.confidence = confidence
        self.questions = []


class questionObject:
    def __init__(self, difficulty, category, question, name):
        self.difficulty = difficulty
        self.category = category
        self.question = question
        self.name = name
        self.info = None


def main():

    # Sorts the teamsList first by breadth, and then subsorts each breadth by confidence
    sortedTeamsList = sorted(
        sorted(populateTeamsList(TEAM_DATA_CSV), key=lambda x: x.confidence), key=lambda x: sum(x.breadth))

    # sorts questionsList first by category, then by difficulty
    sortedQuestionsList = sorted(
        sorted(populateQuestionsStructure(QUESTION_DATA_CSV), key=lambda x: x.difficulty), key=lambda x: x.category)

    # match questions to teams!
    matchedTeams, remainderQuestions = matchQuestionsToTeams(
        sortedTeamsList, sortedQuestionsList)

    for team in matchedTeams:
        print team.teammate1, team.teammate2
        print[q.question for q in team.questions]
        print ''
    print 'Remainder:', [q.question for q in remainderQuestions]


def populateTeamsList(sheet):
    teamsList = []
    with open(sheet) as team_csv:
        team_csv_reader = csv.reader(team_csv, delimiter=',')
        rowCounter = 0
        for row in team_csv_reader:
            if rowCounter == 0:
                rowCounter += 1
            else:
                # find full join of topics each member can answer questions about
                b1 = np.array(map(lambda x: 1 if x == 'Yes' else 0, row[1:11]))
                b2 = np.array(
                    map(lambda x: 1 if x == 'Yes' else 0, row[13:23]))
                breadth = np.sum([b1, b2], 0).clip(0, 1)

                # finds the maximum confidence
                confidence = max(int(row[24]), int(row[25]))
                # create object
                team = teamObject(row[0], row[12], confidence)
                # assign breadth
                team.breadth = breadth
                # add object to list
                teamsList.append(team)
                rowCounter += 1
    return teamsList


def populateQuestionsStructure(sheet):
    questionsList = []
    with open(sheet) as q_csv:
        q_csv_reader = csv.reader(q_csv, delimiter=',')
        row_counter = 0
        for row in q_csv_reader:
            if row_counter == 0:
                row_counter += 1
            else:
                row_counter += 1
                # create question object
                q = questionObject(
                    row[7], TOPICS.index(row[10]), row[6], row[3])
                # if row[7] == '1':
                #     onesQList.append(q)
                # else:
                #     questionList.append(q)
                questionsList.append(q)
    return questionsList


def matchQuestionsToTeams(teamsList, questionsList):

    # we floor here so we can make sure each team gets the same base number of q's
    numQuestionsPerTeam = int(math.floor(
        float(len(questionsList)) / len(teamsList)))

    # first pass.  we match numQuestionsPerTeam questions to teams using a greedy approach by iterating through the sorted order.
    # questions at the front of the list are 'easier', and teams at the front are 'less confident'
    for team in teamsList:
        questionCounter = 0
        for question in questionsList:
            if questionCounter == numQuestionsPerTeam:
                break
            if team.breadth[question.category] == 1:
                team.questions.append(question)
                questionCounter += 1
                questionsList.remove(question)
            else:
                continue

    # second pass.  we are guaranteed that there will be more teams than remaining questions, so we assign one question to each team
    # reverse teams list, so confident teams get more questions
    for team in reversed(teamsList):
        for question in questionsList:
            if team.breadth[question.category] == 1:
                team.questions.append(question)
                questionsList.remove(question)
                break
    return teamsList, questionsList
    # if there are still questions leftover, those questions are ones where a category match was not found
    # with the greedy approach.  manually assign these questions

    # for team in teamsList:

    #     potentialQuestions = filter(
    #         lambda x: x.category in np.nonzero(team.breadth)[0], questionList)

    #     difference = numQuestionsPerTeam
    #     if len(potentialQuestions) > numQuestionsPerTeam:
    #         for i in range(0, int(numQuestionsPerTeam)):
    #             team.questions.append(potentialQuestions[i])
    #             questionList.remove(potentialQuestions[i])
    #     for i in range(0, int(numQuestionsPerTeam)):
    #         team.questions.append(potentialQuestions[i])
    #         questionList.remove(potentialQuestions[i])
    #         difference -= 1

    # for j in range(0, numQuestionsPerTeam - )

    # for each team in tl:
    # make a list of all categories from breadth of team called List1
    # make a list of all questions that have attributes in List1 AND confidence attribute is less than team.confidence called List2
    # assign the first x questions to team
    #     if List2 is empty, assign (# of questions per team - # of current questions) of onesQlist questions
    #     else: do nothing (if there are no more easy/filler questsions)
    # pop the sepcific x questions from questionList


main()
