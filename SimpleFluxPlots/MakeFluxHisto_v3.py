####################################
## This is a simple python script to 
## plot the flux histograms
##
## Just run:
## > python MakeFluxHisto.py
## output: the file w/ the flux histograms
####################################

import os
import uproot
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from scipy.stats import chisquare

# Where are the inputFiles?
rootInputDir = os.environ['BeamVarPath']

fhcHisto = uproot.open(rootInputDir + "FHC/output_uboone_fhc_run0_merged.root")['nue/Detsmear/nue_CV_AV_TPC_5MeV_bin']
rhcHisto = uproot.open(rootInputDir + "RHC/output_uboone_rhc_run0_merged.root")['nue/Detsmear/nue_CV_AV_TPC_5MeV_bin']

binsRHC    = rhcHisto.bins
valueRHC   = rhcHisto.values
binsFHC    = fhcHisto.bins
valueFHC   = fhcHisto.values
ratio      = valueRHC/valueFHC

if np.allclose(binsRHC,binsFHC):
    print ("YAY")

b = binsFHC[:,0]
np.append(b, binsFHC[-1:,1])
np.set_printoptions(threshold=sys.maxsize)
#for i in range(1000):
#    print(valueRHC[i], valueFHC[i])
_ = plt.plot(b, ratio)
plt.ylim(.5,3.0)
plt.show()

'''

####### Let's fix the parameters here                                                                                                          
histoName      = "ratio_run"+str(1)+"_"+str(current)+"_"+str(neutrino)+"_CV_AV_TPC_2D"
thisHisto = thisFolder[histoName]
energy_v = (thisHisto.edges)[0]
angle_v  = (thisHisto.edges)[1]
self.energyEdges[neutrino] = energy_v
self.angleEdges[neutrino]  = angl
            


gStyle.SetOptStat(0)

def getHisto(fileName, histoName,  color,style,pol="FHC"):
    print fileName
    file = TFile(fileName,"r")
    # Calculate POT for this file
    ttree  = file.Get("POT")
    POT = 0
    for i in ttree:
        POT += ttree.POT
        
    tmp0 = file.Get(histoName)
    tmp0.SetDirectory(gROOT)
    #POT    *= 1.0e4 # add to convert to cm2
    # Convert to units and binning wanted: counts fro 50 MeV and 10^6 POTs
    tmp0.Scale(1000000./POT)
    #tmp0.Rebin(10)
    #Make it pretty
    tmp0.SetTitle(pol+"; Neutrino Energy [GeV]; N #nu/50MeV/m^{2}/10^{6}POT")
    tmp0.SetLineColor(color)
    tmp0.SetLineStyle(style)
    tmp0.SetLineWidth(4)
    #file.Close()
    return tmp0






def __main__():
    from os import listdir
    from os.path import isfile, join
    
    # FHC
    onlyfilesfhc   = rootInputDir+"/FHC/output_uboone_fhc_run0_set1.root"
    nueF      = getHisto(onlyfilesfhc,'nue/Detsmear/nue_CV_AV_TPC_5MeV_bin'        , kRed,1)
    antinueF  = getHisto(onlyfilesfhc,'nuebar/Detsmear/nuebar_CV_AV_TPC_5MeV_bin'  , kRed,3)
    numuF     = getHisto(onlyfilesfhc,'numu/Detsmear/numu_CV_AV_TPC_5MeV_bin'      , kBlue,1)
    antinumuF = getHisto(onlyfilesfhc,'numubar/Detsmear/numubar_CV_AV_TPC_5MeV_bin', kBlue,3)
    nNumuF    = 100.*numuF.Integral(26,-1)
    nAntiNumuF= 100.*antinumuF.Integral(26,-1)
    nNueF     = 100.*nueF.Integral(26,-1)
    nAntiNueF = 100.*antinueF.Integral(26,-1)
    nTotalF   = (nNumuF + nAntiNumuF + nNueF + nAntiNueF)/100.
    nNumuF    /= nTotalF
    nAntiNumuF/= nTotalF
    nNueF     /= nTotalF
    nAntiNueF /= nTotalF

    
    c1 = TCanvas("cFHC","cFHC",600,600)
    c1.cd()
    c1.SetLogy()
    numuF    .GetXaxis().SetRangeUser(0.,5.)
    antinumuF.GetXaxis().SetRangeUser(0.,5.)
    nueF     .GetXaxis().SetRangeUser(0.,5.)
    antinueF .GetXaxis().SetRangeUser(0.,5.)
    numuF    .Draw("histo")
    antinumuF.Draw("histosame")
    nueF     .Draw("histosame")
    antinueF .Draw("histosame")
    leg1 = TLegend(0.38,0.65,0.90,0.88)
    SetOwnership( leg1, 0 ) # 0 = release (not keep), 1 = kee
    leg1.AddEntry(numuF    ,str(round(nNumuF    ,2))+"% Nu Mu")
    leg1.AddEntry(antinumuF,str(round(nAntiNumuF,2))+"% AntiNu Mu")
    leg1.AddEntry(nueF     ,str(round(nNueF     ,2))+"% Nu E")
    leg1.AddEntry(antinueF ,str(round(nAntiNueF ,2))+"% AntiNu E")
    leg1.Draw("same")

    c1.Update()


    # RHC
    onlyfilesrhc = rootInputDir+"/RHC/output_uboone_rhc_run0_set1.root"
    nueR      = getHisto(onlyfilesrhc,'nue/Detsmear/nue_CV_AV_TPC_5MeV_bin'        , kRed ,1,"RHC")
    antinueR  = getHisto(onlyfilesrhc,'nuebar/Detsmear/nuebar_CV_AV_TPC_5MeV_bin'  , kRed ,3,"RHC")
    numuR     = getHisto(onlyfilesrhc,'numu/Detsmear/numu_CV_AV_TPC_5MeV_bin'      , kBlue,1,"RHC")
    antinumuR = getHisto(onlyfilesrhc,'numubar/Detsmear/numubar_CV_AV_TPC_5MeV_bin', kBlue,3,"RHC")
    nNumuR    = 100.*numuR.Integral()
    nAntiNumuR= 100.*antinumuR.Integral()
    nNueR     = 100.*nueR.Integral()
    nAntiNueR = 100.*antinueR.Integral()
    nTotalR   = (nNumuR + nAntiNumuR + nNueR + nAntiNueR)/100.
    nNumuR    /= nTotalR
    nAntiNumuR/= nTotalR
    nNueR     /= nTotalR
    nAntiNueR /= nTotalR
    
    c2 = TCanvas("cRHC","cRHC",600,600)
    c2.cd()
    c2.SetLogy()
    numuR    .GetXaxis().SetRangeUser(0.,5.)
    antinumuR.GetXaxis().SetRangeUser(0.,5.)
    nueR     .GetXaxis().SetRangeUser(0.,5.)
    antinueR .GetXaxis().SetRangeUser(0.,5.)
    numuR    .Draw("histo")
    antinumuR.Draw("histosame")
    nueR     .Draw("histosame")
    antinueR .Draw("histosame")
    leg2 = TLegend(0.38,0.65,0.90,0.88)
    SetOwnership( leg2, 0 ) # 0 = release (not keep), 1 = kee
    leg2.AddEntry(numuR    ,str(round(nNumuR    ,2))+"% Nu Mu")
    leg2.AddEntry(antinumuR,str(round(nAntiNumuR,2))+"% AntiNu Mu")
    leg2.AddEntry(nueR     ,str(round(nNueR     ,2))+"% Nu E")
    leg2.AddEntry(antinueR ,str(round(nAntiNueR ,2))+"% AntiNu E")
    leg2.Draw("same")
    c2.Update()    


    
__main__()
raw_input()
'''
