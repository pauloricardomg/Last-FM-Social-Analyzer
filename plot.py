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
    #ax.set_ylim(22, 26.5)
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
    
def distributionsDegree(ListLastFMUser):

    populationSize = len(ListLastFMUser)
    totalweight = 0.0
    
    DictWeight = dict()
    DictDegree = dict()

    for user in ListLastFMUser:
        degree = int(user.friends)
        weight = 1.0/degree
	if degree in DictDegree:
            DictDegree[degree] += 1
            DictWeight[degree] += weight
	else:
            DictDegree[degree] = 1
            DictWeight[degree] = weight
        totalweight += weight 

    keys = DictDegree.keys()
    keys.sort()
    probRW = []
    probRWRW = []
    
    for key in keys:
        probRW.append(float(DictDegree[key]) / float(populationSize))
        probRWRW.append(DictWeight[key] / totalweight)

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, probRW, color="blue")
    plt.loglog(keys, probRWRW, color="red")
    ax.set_xlabel('Number of Friends')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Number of Friends (RW vs RWRW)')
    plt.show()
    
def distributionsAge(ListLastFMUser):

    populationSize = len(ListLastFMUser)
    totalweight = 0.0
    
    DictWeight = dict()
    DictAge = dict()

    for user in ListLastFMUser:
	age = int(user.age)
        degree = int(user.friends)
        weight = 1.0/degree
	if age in DictAge:
            DictAge[age] += 1
            DictWeight[age] += weight
	else:
            DictAge[age] = 1
            DictWeight[age] = weight
        totalweight += weight 

    keys = DictAge.keys()
    keys.sort()
    probRW = []
    probRWRW = []
    
    for key in keys:
        probRW.append(float(DictAge[key]) / float(populationSize))
        probRWRW.append(DictWeight[key] / totalweight)

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.plot(keys, probRW, color="blue")
    plt.plot(keys, probRWRW, color="red")
    ax.set_xlabel('Age')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Age (RW vs RWRW)')
    plt.show()
    
def distributionsPlaycount(ListLastFMUser):

    populationSize = len(ListLastFMUser)
    totalweight = 0.0
    
    DictWeight = dict()
    DictPlaycount = dict()

    for user in ListLastFMUser:
	playcount = int(user.playcount)
        degree = int(user.friends)
        weight = 1.0/degree
	if playcount in DictPlaycount:
            DictPlaycount[playcount] += 1
            DictWeight[playcount] += weight
	else:
            DictPlaycount[playcount] = 1
            DictWeight[playcount] = weight
        totalweight += weight 

    keys = DictPlaycount.keys()
    keys.sort()
    probRW = []
    probRWRW = []
    
    for key in keys:
        probRW.append(float(DictPlaycount[key]) / float(populationSize))
        probRWRW.append(DictWeight[key] / totalweight)

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, probRWRW, color="red")
    plt.loglog(keys, probRW, color="blue")
    ax.set_xlabel('Playcount')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Playcount (RW vs RWRW)')
    plt.show()

def distributionsPlaylists(ListLastFMUser):

    populationSize = len(ListLastFMUser)
    totalweight = 0.0
    
    DictWeight = dict()
    DictPlaylists = dict()

    for user in ListLastFMUser:
	playlists = int(user.playlists)
        degree = int(user.friends)
        weight = 1.0/degree
	if playlists in DictPlaylists:
            DictPlaylists[playlists] += 1
            DictWeight[playlists] += weight
	else:
            DictPlaylists[playlists] = 1
            DictWeight[playlists] = weight
        totalweight += weight 

    keys = DictPlaylists.keys()
    keys.sort()
    probRW = []
    probRWRW = []
    
    for key in keys:
        probRW.append(float(DictPlaylists[key]) / float(populationSize))
        probRWRW.append(DictWeight[key] / totalweight)

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, probRWRW, color="red")
    plt.loglog(keys, probRW, color="blue")
    ax.set_xlabel('Playlists')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Playlists (RW vs RWRW)')
    plt.show()

def distributionsId(ListLastFMUser):

    populationSize = len(ListLastFMUser)
    totalweight = 0.0
    
    DictWeight = dict()
    DictId = dict()

    for user in ListLastFMUser:
	id = int(user.id)
        degree = int(user.friends)
        weight = 1.0/degree
	if id in DictId:
            DictId[id] += 1
            DictWeight[id] += weight
	else:
            DictId[id] = 1
            DictWeight[id] = weight
        totalweight += weight 

    keys = DictId.keys()
    keys.sort()
    probRW = []
    probRWRW = []
    
    for key in keys:
        probRW.append(float(DictId[key]) / float(populationSize))
        probRWRW.append(DictWeight[key] / totalweight)

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.semilogy(keys, probRWRW, 'o', color="red")
    plt.semilogy(keys, probRW, 'o', color="blue")
    ax.set_xlabel('Id')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Id (RW vs RWRW)')
    plt.show()

def distributionsRWRWdegree(ListLastFMUser):
    totalweight = 0.0
    DictWeight = dict()
    for user in ListLastFMUser:
        degree = int(user.friends)
        weight = 1.0/degree
        if degree in DictWeight:
            DictWeight[degree] += weight
        else:
            DictWeight[degree] = weight
        totalweight += weight 

    keys = DictWeight.keys()
    keys.sort()
    probability = []
    for key in keys:
        probability.append(DictWeight[key] / totalweight)
    fig = plt.figure()
    fig.add_subplot(111)
    plt.loglog(keys, probability)
    plt.grid(True)
    plt.title('distribution of degree by RWRW')
    plt.show()


def distributionsRWRWdegree(ListLastFMUser):
    for user in ListLastFMUser:
        degree = int(user.friends)
        weight = 1.0/degre
        if degree in DictWeight:
            DictWeight[degree] += weight
        else:
            DictWeight[degree] = weight
        totalweight += weight 
	
    keys = DictWeight.keys()
    keys.sort()
    probability = []
    for key in keys:
        probability.append(DictWeight[key] / totalweight)
    fig = plt.figure()
    fig.add_subplot(111)
    plt.loglog(keys, probability)
    plt.grid(True)
    plt.title('distribution of degree by RWRW')
    plt.show()


def distributionsRWid(ListLastFMUser):
    populationSize = len(ListLastFMUser)
    DictID = dict()
    for user in ListLastFMUser:
        id = int(user.id)
        if id in DictID:
            DictID[id] += 1
        else:
            DictID[id] = 1
    keys = DictID.keys()
    keys.sort()
    probability = []
    for key in keys:
        probability.append(float(DictID[key]) / float(populationSize))
    fig = plt.figure()
    fig.add_subplot(111)
    plt.loglog(keys, probability)
    plt.grid(True)
    plt.title('distribution of id by RW')
    plt.show()

    

    
if __name__ == "__main__":
            main()
