import categorization.functions as catFunc
from categorization.pdfGeneration import generatePdfsForDataset
import analysationrequest.request as request
from typing import List


def executeCategorization(requests: List[request.AnalysationRequest], drawResultsOnScreen=False) -> []:
    """ Execute the categorization for all csv files in the
        given source directory. """

    for data in requests:
        print("")
        data = catFunc.analyzeFrequency(data)
        data = catFunc.analyzeBalance(data)

    print("\nGenerating pdfs...")
    for dataset in requests:
        # Set the second parameter to True if you want to view the results
        # in a Matplotlib window.
        generatePdfsForDataset(dataset, drawResultsOnScreen)
    return requests
