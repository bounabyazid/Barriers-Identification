import re
import os
import glob
import pickle

import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

def WritePickle(file,Data):
    with open(file+'.pkl', 'wb') as handle:
        pickle.dump(Data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def ReadPickle(file):
    with open(file+'.pkl', 'rb') as handle:
        Data = pickle.load(handle)
    return Data

def US_Forigen():
    files = glob.glob("US Forigen/US Barriers/*.txt")
    #print(files)

    US_Barriers = {}
    for i in range(2007,2020):
        j = [j for j in files if j.__contains__(str(i))]
        with open(j[0], 'r') as f:
             lines = []
             for line in f.readlines():
                 lines.append(line.strip())
             US_Barriers[i] = lines

    Barriers = [val for sublist in US_Barriers.values() for val in sublist]

    frequency = {}
    for barrier in sorted(list(set(Barriers))):
        frequency[barrier] = Barriers.count(barrier)
   
#    my_colors = {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'}
    xlabels_new = [re.sub("(.{46})", "\\1\n", label, 0, re.DOTALL) for label in frequency.keys()]

    plt.bar(frequency.keys(), frequency.values(), width=.5, color='g')
    plt.xticks(range(1,23), xlabels_new, rotation='vertical')

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
    return US_Barriers,list(set(Barriers)),frequency
def EU_Barriers():
    files = glob.glob("Scraping MADB/MADB/*.csv")
    #print(files)
    files = [os.path.basename(file) for file in files]
    #print(files)
    filenames = [os.path.splitext(file)[0] for file in files]
    #print(filenames)
    
    NonActiveSpsData = ReadPickle('Scraping MADB/MADB/'+filenames[0])
    ActiveSpsData = ReadPickle('Scraping MADB/MADB/'+filenames[1])
    
    Active_EU_Barriers = []
    Non_Active_EU_Barriers = []
    
    Russian_Federation = []
    
    for NASps in NonActiveSpsData:
        Data = {}
        for barrier in NASps['publicBarriers']:
            Data['title'] = barrier['title']
            Data['measures'] = []
            for measure in barrier['measures']:
                Data['measures'].append(measure['name'])
            Non_Active_EU_Barriers.append(Data)
            if barrier['country'] == 'Russian Federation':
               Data['ActiveSps'] = False
               Russian_Federation.append(Data)
    print('NonActiveSps Russia Federation',len(Russian_Federation))
    for ASps in ActiveSpsData:
        Data = {}
        for barrier in ASps['publicBarriers']:
            Data['title'] = barrier['title']
            Data['measures'] = []
            for measure in barrier['measures']:
                Data['measures'].append(measure['name'])
            Active_EU_Barriers.append(Data)
            if barrier['country'] == 'Russian Federation':
               Data['ActiveSps'] = True
               Russian_Federation.append(Data)
    
    measures_Active = [measure for barrier in Active_EU_Barriers for measure in barrier['measures']]
    frequency = {}
    for barrier in list(set(measures_Active)):
        frequency[barrier] = measures_Active.count(barrier)
    
    xlabels_new = [re.sub("(.{46})", "\\1\n", label, 0, re.DOTALL) for label in frequency.keys()]

    plt.bar(frequency.keys(), frequency.values(), width=.5, color='r')
    plt.xticks(range(1,13), xlabels_new, rotation='vertical')

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
    measures_NActive = [measure for barrier in Non_Active_EU_Barriers for measure in barrier['measures']]
    frequency = {}
    for barrier in list(set(measures_NActive)):
        frequency[barrier] = measures_NActive.count(barrier)
    
    xlabels_new = [re.sub("(.{46})", "\\1\n", label, 0, re.DOTALL) for label in frequency.keys()]

    plt.bar(frequency.keys(), frequency.values(), width=.5, color='b')
    plt.xticks(range(1,13), xlabels_new, rotation='vertical')

    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.show()

    #return NonActiveSpsData, ActiveSpsData, Active_EU_Barriers, Non_Active_EU_Barriers
    return measures_Active,measures_NActive,frequency,Russian_Federation

US_Barriers,Barriers,US_frequency = US_Forigen()
measures,measures_NActive,frequency,Russian_Federation = EU_Barriers()