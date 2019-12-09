import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import crosscorrelation.settings as crossSettings

RASTERIZE_PLOTS = True


def getXArray(seqA, seqB, secondsWindow):
    xArray = plt.xcorr(seqA.astype(float), seqB.astype(float), normed=True, usevlines=False, maxlags=secondsWindow,
                       markersize=0)[
        0]

    return xArray


def getYArray(seqA, seqB, secondsWindow):
    yArray = plt.xcorr(seqA.astype(float), seqB.astype(float), normed=True, usevlines=False, maxlags=secondsWindow,
                       markersize=0)[
        1]

    return yArray


# X VALUE
def getXValueOfMax(seqA, seqB, secondsWindow):
    xArray = getXArray(seqA, seqB, secondsWindow)
    yArray = getYArray(seqA, seqB, secondsWindow)

    destination: int = yArray.tolist().index(returnMaxResultValue(seqA, seqB, secondsWindow))

    xArray = xArray.tolist()

    return xArray[destination]


def leftHalfVal(left, secondsWindow, yar, ymax):
    i: int = left
    while i >= -secondsWindow:
        if yar[i] < (ymax*0.75):
            return i
        else:
            i -= 1

    return -secondsWindow


def rightHalfVal(right, secondsWindow, yar, ymax):
    while right <= secondsWindow:
        right: int
        if yar[right] < (ymax*0.75):
            return right
        else:
            right += 1
            continue

    return secondsWindow


def calcPeakScore(seqA, seqB, secondsWindow):
    # xar = getXArray(seqA, seqB)
    yar = getYArray(seqA, seqB, secondsWindow)

    ymax = returnMaxResultValue(seqA, seqB, secondsWindow)
    ymaxdest = getXValueOfMax(seqA, seqB, secondsWindow)

    left: int = ymaxdest
    lefty = leftHalfVal(left, secondsWindow, yar, ymax)

    right: int = ymaxdest
    righty = rightHalfVal(right, secondsWindow, yar, ymax)

    print(lefty, righty)


# NEUE FUNKTION UM DEN HÖCHSTEN WERT DES AUSGEGEBENEN ERGEBNISSES ZU ERFAHREN
def returnMaxResultValue(seqA, seqB, secondsWindow):
    ccarray = plt.xcorr(seqA.astype(float), seqB.astype(float), normed=True,
                        usevlines=False, maxlags=secondsWindow, markersize=0)[1]
    return max(ccarray)


def decidePdfPrint(seqA, seqB, value: float, secondsWindow):
    if returnMaxResultValue(seqA, seqB, secondsWindow) >= value:
        print("Max value bigger" + str(value) + " - > OK ...printing")
        return True
    else:
        print("Max value smaller " + str(value) + " - > NO")
        return False


def normalized(a, axis=-1, order=2):
    # See:
    # https://stackoverflow.com/questions/21030391/how-to-normalize-an-array-in-numpy
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)


def plotRawCorrelations(figure, gridSystem, plotRow, seqA, seqB):
    """ Takes a figure, the grid system in the figure, the row to plot to
        and two sequences to calculate and plot the correlations in all
        three ways ('valid', 'same', 'full). """

    # Calculate the correlations:
    valid = np.correlate(seqA, seqB, 'valid')
    same = np.correlate(seqA, seqB, 'same')
    full = np.correlate(seqA, seqB, 'full')

    # Plot the correlations:
    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(valid, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation: Valid')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(same, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation: Same')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(full, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation: Full')
    plotRow += 1

    return plotRow


def plotNormalizedCorrelations(figure, gridSystem,
                               plotRow,
                               seqANorm, seqBNorm):
    """ Takes a figure, the grid system in the figure, the row to plot to and
        two normalized sequences
        to calculate and plot the correlations in
        all three ways ('valid', 'same', 'full). """

    validNormalized = np.correlate(seqANorm, seqBNorm, 'valid')
    sameNormalized = np.correlate(seqANorm, seqBNorm, 'same')
    fullNormalized = np.correlate(seqANorm, seqBNorm, 'full')

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(validNormalized, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation Normalized: Valid')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(sameNormalized, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation Normalized: Same')
    plotRow += 1

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.plot(fullNormalized, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title('Correlation Normalized: Full')
    plotRow += 1
    return plotRow


def plotCorrelationResults(figure, gridSystem, plotRow, seqA, seqB):
    """ Takes a figure, the grid system in the figure, the row to plot to and
        two sequences to execute the correlation calculation
        and to plot the result. """

    ax = figure.add_subplot(gridSystem[plotRow, :])
    ax.set_title('Correlation results')
    # Calculate the correlation, using the xcorr method from the plot librar
    # The function uses numpy.correlate() to calculate the results, see:
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xcorr.html
    ax.xcorr(seqA.astype(float), seqB.astype(float), normed=False,
             usevlines=False, maxlags=1500, linestyle='-', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=1, zorder=1)
    plotRow += 1
    return plotRow


# DIESE FUNKTION WIRD AKTUELL ZUM PLOTTEN DER KREUZKORRALTION GENUTZT

def plotNormalizedCorrelationResults(figure, gridSystem, plotRow, seqA, seqB, secondsWindow):
    """ Takes a figure, the grid system in the figure, the row to plot to
        and two sequences to execute the correlation calculation and to
        plot the result. """
    ax = figure.add_subplot(gridSystem[plotRow, :])

    g = float("{0:.2f}".format(returnMaxResultValue(seqA, seqB, secondsWindow)))

    calcPeakScore(seqA, seqB, secondsWindow)

    ax.set_title(
        'Normalized Correlation results  -   Peak:' + str(g) + " at " + str(getXValueOfMax(seqA, seqB, secondsWindow)))
    # Calculate the correlation, using the xcorr method from
    # the plot library [Normalizing the data]:
    # The function uses numpy.correlate() to calculate the results, see:
    # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xcorr.html
    ax.xcorr(seqA.astype(float), seqB.astype(float), normed=True,
             usevlines=False, maxlags=secondsWindow, linestyle='-', rasterized=RASTERIZE_PLOTS, markersize=0.5, lw=1,
             markeredgecolor='blue')
    ax.grid(True)
    plotRow += 1
    return plotRow


def crossCorrelation(seqA: [], seqB: [], settings: crossSettings.Settings, seqAname, seqBname, secondsWindow,
                     autoTrashPdfs):
    global seqASubtracted, seqBSubtracted
    plt.close("all")
    """ Calculate the cross correlation between two sequences. """
    seqA = np.asarray(seqA)
    seqB = np.asarray(seqB)
    if len(seqA) != len(seqB):
        raise ValueError('Length of sequences must be equal'
                         'for cross correlation')
    seqA = seqA.astype(float)
    seqB = seqB.astype(float)
    numberOfRowsToPlot = 2
    currentPlotRow = 0

    # Normalize the data:
    seqANorm = normalized(seqA)[0]
    seqBNorm = normalized(seqB)[0]

    # The number of rows which need to be plotted, depend
    # on the settings. Calculate the needed number of rows:
    if settings.plotNormalizedData:
        numberOfRowsToPlot += 1
    if settings.plotCorrelations:
        numberOfRowsToPlot += 3
    if settings.plotCorrelations and settings.plotNormalizedData:
        numberOfRowsToPlot += 3
    if settings.plotNonNormalizedResults:
        numberOfRowsToPlot += 1
    if settings.plotNormalizedResults:
        numberOfRowsToPlot += 1

    # Plot the raw sequences:
    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(numberOfRowsToPlot, 2, figure=figure)
    ax = figure.add_subplot(gs[currentPlotRow, 0])
    ax.plot(seqA, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title(seqAname)
    ax = figure.add_subplot(gs[currentPlotRow, 1])
    ax.plot(seqB, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
    ax.set_title(seqBname)
    currentPlotRow += 1

    # Plotting the normalized data:
    if settings.plotNormalizedData:
        ax = figure.add_subplot(gs[currentPlotRow, 0])
        ax.plot(seqANorm, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
        ax.set_title('Normalized: Sequence A')
        ax = figure.add_subplot(gs[currentPlotRow, 1])
        ax.plot(seqBNorm, 'ro', rasterized=RASTERIZE_PLOTS, markersize=1)
        ax.set_title('Normalized: Sequence B')
        currentPlotRow += 1

    if settings.plotCorrelations:
        currentPlotRow = plotRawCorrelations(
            figure, gs, currentPlotRow, seqA, seqB)

    if settings.plotCorrelations and settings.plotNormalizedData:
        currentPlotRow = plotNormalizedCorrelations(
            figure, gs, currentPlotRow, seqANorm, seqBNorm)

    if settings.subtractMeanFromResult:
        seqAMean = np.mean(seqA)
        seqASubtracted = seqA
        seqASubtracted[:] = [x - seqAMean for x in seqASubtracted]
        seqBSubtracted = seqB
        seqBMean = np.mean(seqB)
        seqBSubtracted[:] = [x - seqBMean for x in seqBSubtracted]
        if settings.plotNonNormalizedResults:
            currentPlotRow = plotCorrelationResults(
                figure, gs, currentPlotRow, seqASubtracted, seqBSubtracted)
        if settings.plotNormalizedResults:
            currentPlotRow = plotNormalizedCorrelationResults(
                figure, gs, currentPlotRow, seqASubtracted, seqBSubtracted, secondsWindow)
    else:
        if settings.plotNonNormalizedResults:
            currentPlotRow = plotCorrelationResults(
                figure, gs, currentPlotRow, seqA, seqB)
        if settings.plotNormalizedResults:
            currentPlotRow = plotNormalizedCorrelationResults(
                figure, gs, currentPlotRow, seqA, seqB, secondsWindow)

    if settings.drawResults:
        figure.canvas.set_window_title(settings.exportFilePath)
        plt.draw()
        plt.show()
    if settings.exportToPdf:
        if settings.decidePdfPrinting:
            if decidePdfPrint(seqASubtracted, seqBSubtracted, autoTrashPdfs, secondsWindow):
                figure.savefig(settings.exportFilePath, bbox_inches='tight', dpi=1000)
                plt.close(figure)
        else:
            figure.savefig(settings.exportFilePath, bbox_inches='tight', dpi=1000)
            plt.close(figure)
