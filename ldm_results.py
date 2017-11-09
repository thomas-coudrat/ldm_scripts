#!/usr/bin/env python

# ------------------------------------------------------------------------------
# This script extracts results of an LDM experiment, and stores them into
# a RESULTS/ directory, together with a .txt file containing the information
# about all LDM results.
# The results can be sorted either by ICM score (option=icm) or by a
# combination of ICM and OPUS score, both weighted equally (option=opus-icm)
#
# Thomas Coudrat, February 2014
# thomas.coudrat@gmail.com
# ------------------------------------------------------------------------------

import os
import shutil
import argparse
import sys


def main():
    """
    Execute this script
    """

    ldmDir, sort = parsing()

    # Get the the opus and icm scores
    # both lists are organized like this
    #   [(constantID, 'path/Of/LDMresult.pdb', score)]
    # Extremums are as such
    # [icmMax, icmMin, opusMax, opusMin]
    icmList, opusList, extremums = getLDMscores(ldmDir + "/RUN")

    # Check if score lists were loaded
    if len(icmList) == 0 or len(opusList) == 0:
        print("ICMlist and/or OPUSlist not found")
        sys.exit()
    else:
        icmListNew = makeSort(icmList, "ICM")
        opusListNew = makeSort(opusList, "OPUS")

    # Make the opus + icm normalized score and results extraction
    if sort == "opus-icm":
        results_dir = "/RESULTS_opus-icm"
        # Using the value '1' sorts the normalized lists based on the combined
        # score of OPUS + ICM
        combineList = getNormalizedScore(icmListNew, opusListNew,
                                         extremums, 1, "normalized OPUS-ICM")
        createDir(ldmDir, results_dir)
        transferResults(combineList, ldmDir, results_dir)

    # Make the ICM only scoring and results extraction
    elif sort == "icm":
        results_dir = "/RESULTS_icm"
        # Using the value 2 sorts the normalized list based on ICM score only
        icmList = getNormalizedScore(icmListNew, opusListNew,
                                     extremums, 2, "ICM")
        createDir(ldmDir, results_dir)
        transferResults(icmList, ldmDir, results_dir)

    # Make the OPUS only scoring and results extraction
    elif sort == "opus":
        results_dir = "/RESULTS_opus"
        opusList = getNormalizedScore(icmListNew, opusListNew,
                                      extremums, 3, "OPUS")
        createDir(ldmDir, results_dir)
        transferResults(opusList, ldmDir, results_dir)
    else:
        print("The sorting method must be either 'opus-icm' or 'icm'")


def parsing():
    """
    Defining the parsing, and parsing arguments
    """

    descr = "Tool to extract results of a LDM experiment, sorting them " \
            "on either normalized OPUS & ICM score, or just normalized " \
            "ICM score"
    help_ldmDir = "Input the LDM directory path"
    help_sort = "Input the sorting method, options are 'opus-icm', " \
                "'icm' or 'opus'"

    # Argument parsing
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("ldmDir", help=help_ldmDir)
    parser.add_argument("sort", help=help_sort)

    args = parser.parse_args()

    ldmDir = args.ldmDir
    sort = args.sort

    return ldmDir, sort


def getLDMscores(runDir):
    """
    This loops over all the directories in the given runDir, and for each
    directory that is a number, looks for the score files (ICM and OPUS).
    Then is stores the scoring for all receptors of that LDM experiment, and
    also keeps the highest and lowest values of ICM and OPUS scores (for future
    normalization).
    Each receptor gets a constant ID, which represents it wether we are
    checking an ICM or an OPUS score.
    """

    # List storing scores
    icmList = []
    opusList = []
    constantID = 0
    icmMax = -9999999999999.99
    icmMin = 9999999999999.99
    opusMax = -9999999999999.99
    opusMin = 9999999999999.99

    # Looping over items in the directory
    for entry in os.listdir(runDir):
        if entry.isdigit():
            dirNum = entry.strip()
            recSolutionPath = runDir + "/" + dirNum + "/filtered/"

            icmFile = open(runDir + "/" + dirNum + '/icm-running-best', 'r')
            icmLines = icmFile.readlines()
            icmFile.close()
            opusFile = open(runDir + "/" + dirNum + '/opus-running-best', 'r')
            opusLines = opusFile.readlines()
            opusFile.close()

            for icm, opus in zip(icmLines, opusLines):
                icm = icm.split()
                opus = opus.split()
                # Verify that there is a value for the ICM and OPUS lines:
                # often the LDM will crash during a replicate run, and no
                # further receptors are obtained for this particular replicate
                if len(icm) > 1 and len(opus) > 1:
                    receptPath = recSolutionPath + icm[0]
                    icmScore = float(icm[1].strip())
                    # Keep ICM biggest and smallest score
                    if icmScore > icmMax:
                        icmMax = icmScore
                    if icmScore < icmMin:
                        icmMin = icmScore
                    # Store ICM score information
                    icmList.append((constantID, receptPath, icmScore))

                    receptPath = recSolutionPath + opus[0]
                    opusScore = float(opus[1].strip())
                    # Keep OPUS biggest and smallest score
                    if opusScore > opusMax:
                        opusMax = opusScore
                    if opusScore < opusMin:
                        opusMin = opusScore
                    # Store OPUS score information
                    opusList.append((constantID, receptPath, opusScore))

                constantID += 1
    """
    print('PRINTING ICM')
    for item in icmList:
        print(item)

    print('PRINTING OPUS')
    for item in opusList:
        print(item)
    """

    return icmList, opusList, [icmMax, icmMin, opusMax, opusMin]


def getNormalizedScore(icmListNew, opusListNew, extremums, val, message):
    """
    Normalize both ICM and OPUS scores on 1, and combine them
    Then write a text file with the ordered results, also as the #1 solution
    The best ICM and OPUS score is 0 (highest value), and the worst (lowest
    value) is 1.
    Combining them, one has to select the smallest sum to get the best scoring
    complex
    The argument 'val' defines the value that will be used in the
    normalizedList to be sorted. This can be the combined normalized list, or
    ICM score, or OPUS score only
    """

    print("Make a " + message + "sorted list")

    [icmMax, icmMin, opusMax, opusMin] = extremums

    normalizedList = []

    # Loop over the the items in the list
    for icm, opus in zip(icmListNew, opusListNew):
        # print(icm[1], ',', opus[1], '=', icm[3], '+',opus[3])
        receptPath = icm[1]
        icmScore = icm[2]
        # icmScoreID = icm[3]
        opusScore = opus[2]
        # opusScoreID = opus[3]
        icmNorm = abs((abs(icmScore) - abs(icmMin)) /
                      (abs(icmMax) - abs(icmMin)))
        opusNorm = abs((abs(opusScore) - abs(opusMin)) /
                       (abs(opusMax) - abs(opusMin)))

        normalizedList.append((receptPath,
                               icmNorm + opusNorm,
                               icmScore,
                               opusScore))

    normalizedList = sorted(normalizedList, key=lambda score: score[val])
    # bestNormScore = normalizedList[0]

    """
    print("NORMALIZED SCORE LIST")
    for item in normalizedList:
        print(item)

    print("icmMax", icmMax)
    print("icmMin", icmMin)
    print("opusMax", opusMax)
    print("opusMin", opusMin)
    """

    return normalizedList


def createDir(ldm_dir, results_dir):
    """
    Check if this directory exists, if it does delete it and its content, then
    create a new empty one
    """

    print("Create " + results_dir + " directory")

    resDirPath = ldm_dir + results_dir

    if os.path.isdir(resDirPath):
        shutil.rmtree(resDirPath)
    os.mkdir(resDirPath)


def makeSort(scoreList, message):
    """
    Sorting both lists based on score, adding the index of each score to the
    info, and sorting of the new list based on directory.
    The list is of the form:
        [[consantID, receptorPath, scoreValue, scoreID]]
    """

    print("Sort the results based on " + message + " scores")

    scoreList = sorted(scoreList, key=lambda score: score[2])

    scoreListNew = []
    scoreID = 1
    for score in scoreList:
        constantID = score[0]
        receptPath = score[1]
        scoreVal = score[2]
        scoreListNew.append((constantID, receptPath, scoreVal, scoreID))
        scoreID += 1
    scoreListNew = sorted(scoreListNew, key=lambda score: score[0])

    """
    print('PRINTING ICM new')
    for item in icmListNew:
        print(item)
    """

    return scoreListNew


def transferResults(normalizedList, ldm_dir, results_dir):
    """
    Copy the results from the RUN folder, onto the RESULTS folder
    Get the LDM scoring info, call the copyReceptor function
    """

    print("Transfer all LDM results to " + results_dir)

    resultsDirectory = ldm_dir + results_dir

    resultFile = open(resultsDirectory + "/LDMresult.txt", "w")
    resultFile.write("Conf \t"
                     "Replica \t"
                     "Round \t"
                     "NormScore \t"
                     "ICMscore \t"
                     "OPUSscore \n")

    # Setup to figure out the number of '0' to add in front of the identifier
    # of the .pdb results
    total = len(normalizedList)
    totLen = len(str(total))

    # Loop over the results orderd by the normalized score
    for i, item in enumerate(normalizedList):
        recOriginPath = item[0]
        print(i, recOriginPath)

        #
        # Values associated with that LDM result:
        #

        # Receptor number
        diff = totLen - len(str(i))
        recNum = str(i)
        for zero in range(diff):
            recNum = "0" + recNum

        # Figure out at which round this .pdb result was obtained
        recOriginName = os.path.basename(recOriginPath)
        roundNum = recOriginName.split("-")[1].replace(".pdb", "")

        # Replica number
        replicaPath = os.path.dirname(os.path.dirname(recOriginPath))
        replica = replicaPath.split("/RUN/")[1]

        # Normalized score
        normScore = str(item[1])

        # ICM score
        icmScore = str(item[2])

        # OPUS score
        opusScore = str(item[3])

        # Copy the best scored model in the root directory
        shutil.copyfile(recOriginPath,
                        resultsDirectory + "/ldm_" + recNum + ".pdb")
        # And add that receptor to the log file
        resultFile.write(recNum + ".pdb\t" +
                         replica + "\t" +
                         roundNum + "\t" +
                         normScore + "\t" +
                         icmScore + "\t" +
                         opusScore + "\n")

    resultFile.close()


if __name__ == "__main__":
    main()
