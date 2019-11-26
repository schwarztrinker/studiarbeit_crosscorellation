import math
import numpy as np
from analysationrequest.request import AnalysationRequest


def analyzeFrequency(data: AnalysationRequest) -> AnalysationRequest:
    """ Analyze the frequency for all given sequences. """
    data.frequencyResults = np.ndarray(len(data.sequences), float)
    data.subSequenceFrequencyResults = np.ndarray(len(data.sequences), object)
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating frequency for",
              data.fileName, "Sequence", sequenceIndex)
        data.frequencyResults[sequenceIndex] = \
            calculateFrequencyForSequence(sequence)
        data.subSequenceFrequencyResults[sequenceIndex] = \
            calculateFrequenciesForSubSequences(sequence)

    return data


def analyzeBalance(data: AnalysationRequest) -> AnalysationRequest:
    """ Analyze the balance for all given sequences. """
    data.balances = np.ndarray(len(data.sequences), float)
    data.subSequenceBalances = np.ndarray(len(data.sequences), object)
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Calculating balance for",
              data.fileName, "Sequence", sequenceIndex)
        data.balances[sequenceIndex] = calculateBalanceForSequence(sequence)
        data.subSequenceBalances[sequenceIndex] = \
            calculateBalancesForSubSequences(sequence)

    return data

def calculateBalancesForSubSequences(sequence) -> []:
    """ Calculate the balances for the sub sequences. """

    sequenceLength = len(sequence)
    resultDictionary = {}

    # Calculate for sub-sequences
    # The length of a subsequence is a mutiple of 10
    # e.g. 10, 1000, 1000
    # There must be at least 10 subsequences for each length.
    subSequenceDivisor = 10
    while (sequenceLength / subSequenceDivisor) >= 10:
        subSequenceSize = math.ceil(sequenceLength/subSequenceDivisor)
        splittedList = np.array_split(sequence, subSequenceSize)
        resultDictionary[subSequenceDivisor] = []
        for entry in splittedList:
            resultDictionary[subSequenceDivisor].append(
                calculateBalanceForSequence(entry))
        subSequenceDivisor *= 10

    return resultDictionary


def calculateFrequenciesForSubSequences(sequence) -> {}:
    """ Calculate the frequency for the sub sequences. """

    sequenceLength = len(sequence)
    resultDictionary = {}

    # Calculate for sub-sequences
    # The length of a subsequence is a mutiple of 10
    # e.g. 10, 1000, 1000
    # There must be at least 10 subsequences for each length.
    subSequenceDivisor = 10
    while (sequenceLength / subSequenceDivisor) >= 10:
        subSequenceSize = math.ceil(sequenceLength/subSequenceDivisor)
        splittedList = np.array_split(sequence, subSequenceSize)
        resultDictionary[subSequenceDivisor] = []
        for entry in splittedList:
            resultDictionary[subSequenceDivisor].append(
                calculateFrequencyForSequence(entry))
        subSequenceDivisor *= 10

    return resultDictionary


def calculateFrequencyForSequence(sequence) -> float:
    """ Calculate the frequency for a given sequence.
        Returns a value between 0 and 1. A value near 0 is a infrequent
        sequence, a value near 1 is highly frequent sequence. """
    oldValue = 0
    changeCounter = 0
    for index, value in enumerate(sequence):
        if index == 0:
            oldValue = value
            continue
        if oldValue != value:
            changeCounter += 1
            oldValue = value

    if changeCounter == 0 or len(sequence) == 0:
        return 0
    else:
        return np.round((changeCounter / len(sequence)), 2)


def calculateBalanceForSequence(sequence) -> float:
    """ Calculate the balance for a sequence.
        The balance is calculated with the following formula:+
        Count of occurences of 1 / length of sequence.
        A squence with a value around 0.5 is balanced, all others
        are unbalanced. """
    counter = 0
    if len(sequence) == 0:
        return 0
    for value in sequence:
        if value == 1:
            counter += 1
    return np.round((counter / len(sequence)), 2)
