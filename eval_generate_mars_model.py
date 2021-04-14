#IMPORTANT: ONLY works with Python 2.7!

import pandas as pd
import matplotlib.pyplot as plt
import pyearth
from pyearth import Earth
from pyearth import export
import numpy
import sympy
import sys
numpy.set_printoptions(threshold=sys.maxsize)

def plotMARS(csv, colorScatter, colorPlot, filePath, component):
    # Fit an Earth model
    sw = 1 + 1 / (csv['x'] + 1)
    model = Earth(minspan_alpha=5, endspan_alpha=5)
    model.fit(csv['x'], csv['y'], sample_weight=sw)

    # generate summary
    summary = model.summary() + "\n---------------\n" + str(pyearth.export.export_sympy(model))
    writeto = open(filePath + component + "_mars.txt", "w")
    writeto.write(summary)
    writeto.close()
    print(summary)

    # Plot
    s = numpy.linspace(1, 200, 100)
    y_pred = model.predict(s)
    plt.scatter(csv['x'], csv['y'], color=colorScatter, label='Measurement Samples')
    plt.plot(s, y_pred, color=colorPlot, label='MARS function')
    plt.legend()
    plt.xlabel('Concurrency')
    plt.ylabel('Response Time')
    plt.savefig(filePath + component + "_mars.pdf")
    plt.clf()
    # plt.show()

filenames = ["A", "B", "C"]
path = "logs/training/"
for file in filenames:
    print("Component: " + file)
    csv = pd.read_csv(path + file + "_trainingdata.csv", names=['y', 'x'], header=0)  # y=response time, x = concurrency
    plotMARS(csv, 'blue', 'black', path, file)
