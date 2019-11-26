class AnalysationRequest:
    """ A AnalysationRequest contains the data which should be analyzed. """

    def __init__(self, fileName):
        # The file name of the source
        self.fileName = fileName
        # The raw, unexpanded squences from the source
        self.rawSequences = []
        # The expanded sequences
        self.sequences = []
        # The calculated frequencies. The index is equal to the
        # index of source sequences
        self.frequencyResults = []
        # Contains the frequencies for the sub sequences
        self.subSequenceFrequencyResults = []
        # The calculated balances. The index is equal to the
        # index of source sequences
        self.balances = []
        # Contains the balances for the sub sequences
        self.subSequenceBalances = []
        # Contains the meta-data dictionaries. The index is equal to the
        # index of source sequences
        self.metadataDictionaries = []
