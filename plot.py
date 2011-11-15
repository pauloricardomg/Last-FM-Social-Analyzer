import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.patches import Polygon

def get_dists(users_list, attr):
    population_size = len(users_list)
    total_weight = 0.0
    
    dict_weight = dict()
    dict_attr = dict()

    for user in users_list:
        chosen_attr = int(getattr(user,attr))
        degree = int(user.friends)
	weight = 1.0/degree
	if chosen_attr in dict_attr:
            dict_attr[chosen_attr] += 1
            dict_weight[chosen_attr] += weight
	else:
            dict_attr[chosen_attr] = 1
            dict_weight[chosen_attr] = weight
        total_weight += weight 

    keys = dict_attr.keys()
    keys.sort()
    
    prob_RW = []
    prob_RWRW = []
    
    for key in keys:
        prob_RW.append(float(dict_attr[key]) / float(population_size))
        prob_RWRW.append(dict_weight[key] / total_weight)

    return (prob_RW, prob_RWRW, keys)

def plot_degree_distribution(users_list):
    probs = get_dists(users_list, "friends")
    prob_RW = probs[0]
    prob_RWRW = probs[1]
    keys = probs[2]

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, prob_RW, color="blue")
    plt.loglog(keys, prob_RWRW, color="red")
    ax.set_xlabel('Number of Friends')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Number of Friends (RW vs RWRW)')
    plt.show()

def plot_age_distribution(users_list):
    probs = get_dists(users_list, "age")
    prob_RW = probs[0]
    prob_RWRW = probs[1]
    keys = probs[2]

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.plot(keys, prob_RW, color="blue")
    plt.plot(keys, prob_RWRW, color="red")
    ax.set_xlabel('Age')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Age (RW vs RWRW)')
    plt.show()
    
def plot_playcount_distribution(users_list):
    probs = get_dists(users_list, "playcount")
    prob_RW = probs[0]
    prob_RWRW = probs[1]
    keys = probs[2]

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, prob_RWRW, color="red")
    plt.loglog(keys, prob_RW, color="blue")
    ax.set_xlabel('Playcount')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Playcount (RW vs RWRW)')
    plt.show()

def plot_playlists_distribution(users_list):
    probs = get_dists(users_list, "playlists")
    prob_RW = probs[0]
    prob_RWRW = probs[1]
    keys = probs[2]

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.loglog(keys, prob_RWRW, color="red")
    plt.loglog(keys, prob_RW, color="blue")
    ax.set_xlabel('Playlists')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Playlists (RW vs RWRW)')
    plt.show()
    
def plot_id_distribution(users_list):
    probs = get_dists(users_list, "id")
    prob_RW = probs[0]
    prob_RWRW = probs[1]
    keys = probs[2]

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.semilogy(keys, prob_RWRW, 'o', color="red")
    plt.semilogy(keys, prob_RW, 'o', color="blue")
    ax.set_xlabel('Id')
    ax.set_ylabel('Probability')
    plt.figtext(0.80, 0.80, 'RW', backgroundcolor="blue",
                color='white', weight='roman', size='small')
    plt.figtext(0.80, 0.77, 'RWRW', backgroundcolor="red",
                color='white', weight='roman', size='small')
    plt.grid(True)
    plt.title('Distribution of Id (RW vs RWRW)')
    plt.show()


def plot_visittimes_vs_degree(users_list):
    population_size = len(users_list)
    total_weight = 0.0
    
    dict_visittimes = dict()
    dict_ids = dict()

    for user in users_list:
        degree = int(user.friends)
        visitTimes = int(user.crawl_count)
	if degree in dict_visittimes:
            dict_visittimes[degree] += visitTimes
            dict_ids[degree].add(user.id)
	else:
            dict_visittimes[degree] = visitTimes
	    dict_ids[degree] = set()
            dict_ids[degree].add(user.id)

    keys = dict_visittimes.keys()
    keys.sort()
    times = []
    for key in keys:
        times.append(float(dict_visittimes[key]) / float(len(dict_ids[key])))

    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt.semilogx(keys, times, color="red")
    ax.set_xlabel('Degree')
    ax.set_ylabel('Average Visit Times')
    plt.grid(True)
    plt.title('Average Visit Times vs. Node Degree in Random Walk')
    plt.show()
    

def plot_meanage_vs_samplesize(ListListRW, ListListRWRW):
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

