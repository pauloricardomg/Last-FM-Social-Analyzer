import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.patches import Polygon
from resulttypes import RWResult, RWRWResult

def meanAgeVSsampleSize(ListListRW, ListListRWRW):
    num_ticks = len(ListListRW)
    ListListValues = []
    ListSampleSizes = []
    for i in range(num_ticks):
        ListRWValues = ListListRW.pop(0)
        ListRWAges = map(lambda x: x.age, ListRWValues)
        ListRWRWValues = ListListRWRW.pop(0)
        ListRWRWAges = map(lambda x: x.age, ListRWRWValues)
        ListListValues.append(ListRWAges)
        ListListValues.append(ListRWRWAges)
        ListSampleSizes.append(ListRWValues.pop().samplesize)
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pos = np.array(range(len(ListListValues)))+1
    bp = ax.boxplot( ListListValues, sym='+', vert=1, whis=1.5,
                     positions=pos, notch=0)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')
    text_transform= mtransforms.blended_transform_factory(ax.transData,
                                                         ax.transAxes)
    ax.set_xlabel('Sample Size')
    ax.set_ylabel('Age Means')
    ax.set_ylim(22, 26.5)
    fig.subplots_adjust(right=0.95, top=0.9, bottom=0.25)
    
    boxColors = ['darkkhaki','royalblue']
    numBoxes = len(ListListValues)
    medians = range(numBoxes)
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX,boxY)
        # Alternate between Dark Khaki and Royal Blue
        k = i % 2
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
            
    # Set the axes labels
    xtickNames = plt.setp(ax, xticklabels=np.repeat(ListSampleSizes, 2))
    plt.setp(xtickNames, rotation=45, fontsize=8)
    
    plt.figtext(0.80, 0.80, 'RW Means', backgroundcolor=boxColors[0], color='black', weight='roman',
           size='x-small')
    plt.figtext(0.80, 0.77, 'RWRW Means', backgroundcolor=boxColors[1],
               color='white', weight='roman', size='x-small')

    plt.show()