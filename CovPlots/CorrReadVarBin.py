import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.signal import find_peaks
from scipy.stats  import pearsonr




def CalculateCorrelationCoeff(csvName = "All_run18.csv",plotMe=False):
    df    = pd.read_csv(csvName,delim_whitespace=True)
    df    = df.loc[ df['energy'] < 2., :]

    if plotMe:
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('RHC Diff')
        ax1.set_ylabel('FHC Diff')
        ax1.plot(df['RHC'], df['FHC'], marker="o",markersize=1,linestyle = 'None')
        plt.show()

    
    df['FHCIndex'] = np.argsort( df['FHC'])
    df['RHCIndex'] = np.argsort( df['RHC'])

    if plotMe:
        fig0, ax0 = plt.subplots()
        ax0.set_xlabel('RHC Diff Rank')
        ax0.set_ylabel('FHC Diff Rank')
        ax0.plot(df['energy'], df['RHC'], marker="o",markersize=1,linestyle = 'None')
        ax0.plot(df['energy'], df['FHC'], marker="o",markersize=1,linestyle = 'None')
        plt.show()
        input()

    #print(df['RHCIndex'])
    pearsonTest  = pearsonr(df['RHC'],df['FHC']) 
    spearmanTest = pearsonr(df['RHCIndex'],df['FHCIndex']) 
    #print (csvName, pearsonTest[0],spearmanTest[0])
    return pearsonTest[0],spearmanTest[0]


def __main__():
    from os import listdir
    from os.path import isfile, join
    onlyfiles  = [f for f in listdir("CovPlotsVarBin") if isfile(join("CovPlotsVarBin", f))]
    onlyfiles  = [f for f in onlyfiles if "csv" in f]
    labelNames = [x.replace('NBins18.csv', '').replace('', '') for x in onlyfiles]
    labelNames = [x.replace('NBins20.csv', '').replace('', '') for x in labelNames]
    labelNames = [x.replace('NuE_', '').replace('', '') for x in labelNames]
    labelNames = [x.replace('NuEBar_', '').replace('', '') for x in labelNames]
    labelNames = [x.replace('NuMu_', '').replace('', '') for x in labelNames]
    labelNames = [x.replace('NuMuBar_', '').replace('', '') for x in labelNames]
    labelNames = [x.replace('AllNu_', '').replace('', '') for x in labelNames]
    labelNames = sorted(set(labelNames))

    #df = pd.DataFrame(labelNames,columns=["variation"])
    #print (df)

    coeffDict = {}
    for name in onlyfiles:
        #print(name[:-4])
        coeff = CalculateCorrelationCoeff("CovPlotsVarBin/"+name)
        coeffDict[name] = coeff
    #print(coeffDict)

    neutrinoTypes = ["NuE_","NuEBar_","NuMu_","NuMuBar_","AllNu_"]
    nBins         = ["NBins20","NBins18"]
    columnNames   = ["variations"]
    tuplaName = []
    listOfLists = []
    for n in labelNames:
        tupla = [n[:-1]]
        columnNames = ["variations"]
        for t in neutrinoTypes:
            for b in nBins:
                for k in coeffDict.keys():
                    if (t in k) and (n in k) and (b in k):
                        #print (n, t, b, coeffDict[k][0],coeffDict[k][1])
                        tupla.append(coeffDict[k][0])
                        tupla.append(coeffDict[k][1])
                        columnNames.append(t+b+"_P")
                        columnNames.append(t+b+"_S")
        print(type(tupla))
        listOfLists.append(tupla)

    dfFinal = pd.DataFrame(listOfLists[1:], columns = columnNames)
    #dfFinal['newOrder']   = ((dfFinal['variations']).str.replace('run','',regex=True)).astype(int)
    dfFinal['variations'] = (dfFinal['variations']).str.replace('run','var',regex=True)
    dfFinal = dfFinal.sort_values('variations')


    fig2, ax2 = plt.subplots()
    plt.xticks(rotation=45)
    plt.title('Pearson And Spearman Correlation Coeff -- Nue')
    ax2.set_ylabel('Correlation coefficient CV Variation')
    #ax2.plot(dfFinal['variations'], dfFinal['NuE_NBins4000_P'], marker="o",linestyle = 'None',label='NuE_NBins4000_P')
    #ax2.plot(dfFinal['variations'], dfFinal['NuE_NBins4000_S'], marker="o",linestyle = 'None',label='NuE_NBins4000_S')
    ax2.plot(dfFinal['variations'], dfFinal['NuE_NBins18_P'], marker="o",linestyle = 'None',label='NuE Pearson Coeff')
    ax2.plot(dfFinal['variations'], dfFinal['NuE_NBins18_S'], marker="o",linestyle = 'None',label='NuE Spearman Coeff')
    plt.legend()

    fig3, ax3 = plt.subplots()
    plt.xticks(rotation=45)
    plt.title('Pearson And Spearman Correlation Coeff -- NueBar')
    ax3.set_ylabel('Correlation coefficient CV Variation')
    #ax3.plot(dfFinal['variations'], dfFinal['NuEBar_NBins4000_P'], marker="o",linestyle = 'None',label='NuEBar_NBins4000_P')
    #ax3.plot(dfFinal['variations'], dfFinal['NuEBar_NBins4000_S'], marker="o",linestyle = 'None',label='NuEBar_NBins4000_S')
    ax3.plot(dfFinal['variations'], dfFinal['NuEBar_NBins18_P'], marker="o",linestyle = 'None',label='NuEBar Pearson Coeff')
    ax3.plot(dfFinal['variations'], dfFinal['NuEBar_NBins18_S'], marker="o",linestyle = 'None',label='NuEBar Spearman Coeff')
    plt.legend()

    fig4, ax4 = plt.subplots()
    plt.xticks(rotation=45)
    plt.title('Pearson And Spearman Correlation Coeff -- NuMu')
    ax4.set_ylabel('Correlation coefficient CV Variation')
    #ax4.plot(dfFinal['variations'], dfFinal['NuMu_NBins4000_P'], marker="o",linestyle = 'None',label='NuMu_NBins4000_P')
    #ax4.plot(dfFinal['variations'], dfFinal['NuMu_NBins4000_S'], marker="o",linestyle = 'None',label='NuMu_NBins4000_S')
    ax4.plot(dfFinal['variations'], dfFinal['NuMu_NBins20_P'], marker="o",linestyle = 'None',label='NuMu Pearson Coeff')
    ax4.plot(dfFinal['variations'], dfFinal['NuMu_NBins20_S'], marker="o",linestyle = 'None',label='NuMu Spearman Coeff')
    plt.legend()

    fig5, ax5 = plt.subplots()
    plt.xticks(rotation=45)
    ax5.set_ylabel('Correlation coefficient CV Variation')
    plt.title('Pearson And Spearman Correlation Coeff -- NuMuBar')
    #ax5.plot(dfFinal['variations'], dfFinal['NuMuBar_NBins4000_P'], marker="o",linestyle = 'None',label='NuMuBar_NBins4000_P')
    #ax5.plot(dfFinal['variations'], dfFinal['NuMuBar_NBins4000_S'], marker="o",linestyle = 'None',label='NuMuBar_NBins4000_S')
    ax5.plot(dfFinal['variations'], dfFinal['NuMuBar_NBins20_P'], marker="o",linestyle = 'None',label='NuMuBar Pearson Coeff')
    ax5.plot(dfFinal['variations'], dfFinal['NuMuBar_NBins20_S'], marker="o",linestyle = 'None',label='NuMuBar Spearman Coeff')

    plt.legend()
    plt.show()
    print(dfFinal)
    


__main__()
