import os
import sys
import errno
from categorization.automated_categorization import executeCategorization
from crosscorrelation.automated_crosscorrelation import (
    executeCrossCorrelationForDatasets)
import analysationrequest.functions as fileAccessFuntions


# You need the dependencies defined in "dependencies.txt" installed to run this
# script.


def main():
    # Check if a argument for a folder path is provided
    if len(sys.argv) > 1:
        folderPath = sys.argv[1]
        if os.path.exists(folderPath):
            # Folder path found:
            executedForFolderPath(folderPath)
            return
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(
                    errno.ENOENT), folderPath)

    # Folder path not provided or found. Use the default folder:

    # Get the directory path of where this script is executed:
    dirname = os.path.dirname(__file__)
    # Build the path for the source folder:
    directoryPath = os.path.join(dirname, 'sourceFiles')
    # Create the default folder if it does not exist:
    if not os.path.exists(directoryPath):
        os.makedirs(directoryPath)
    executedForFolderPath(directoryPath)


def executedForFolderPath(path):
    # Read the csv source files and expand them:
    filePathBatches = fileAccessFuntions.getFilePathBatches(path)

    batchcounter = 0
    for filePathBatch in filePathBatches:
        batchcounter += 1
        print("Executing batch", str(batchcounter), "of", str(len(filePathBatches)), "batches.")
        requests = fileAccessFuntions.readFilesForFilePathBatch(filePathBatch)
        # Execute the categorization: Calculating the balance, frequency:
        # Set the second parameter to True if you want to show the results in a
        # Matplotlib window:
        executeCategorization(requests, False)
        # This will calculate the cross correlation between sequences in the same
        # source file. Additionally, the sequences must have the same length.
        executeCrossCorrelationForDatasets(requests)


if __name__ == "__main__":
    main()
