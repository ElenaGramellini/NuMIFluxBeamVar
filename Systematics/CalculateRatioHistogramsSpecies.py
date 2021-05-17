####################################
## This is a simple python script to 
## obtain the weight from the NuMI
## geometry beamline variations
## Just run as
## > python CalculateRatioHistograms.py
## output: the file w/ all variations ratio wrt to CV
## 
####################################


from ROOT import *
import os
gStyle.SetOptStat(0)

# Where are the inputFiles?
rootInputDir = os.environ['BeamVarPath']

# fetch the histograms and POT normalize them
def getHisto(fileName, histoName,name):
    file   = TFile(fileName,"r")
    ttree  = file.Get("POT")
    POT = 0
    for i in ttree:
        POT += ttree.POT
    c1 = TCanvas()
    tmp0   = file.Get(histoName)
    tmp0.SetDirectory(gROOT)
    tmp0.SetTitle(name)
    tmp0.Scale(1./POT)
    tmp0.Draw()
    c1.Update()
    input()
    file.Close()
    return tmp0


def DivideHistos(var, cv):
    var.SetDirectory(gROOT)
    var.Divide(cv)
    return var


'''
def saveToTxt(theHistogramFile):
    outTextFile = open("s.txt","w")
    ax_x = (theHistogramFile.GetXaxis())#->GetBinCenter(ix);
    ax_y = (theHistogramFile.GetYaxis())#->GetBinCenter(iy);
    nX   =  ax_x.GetNbins()
    nY   =  ax_y.GetNbins()
    for i in xrange(nX):
        for j in xrange(nY):
            outString = "%s %s %s %s %s\n" %  (i, j, ax_x.GetBinCenter(i), ax_y.GetBinCenter(j),theHistogramFile.GetBinContent(i,j))
            outTextFile.write(outString)
    outTextFile.close()
'''


def __main__():
    from os import listdir
    from os.path import isfile, join

    # We are going to plot all the possible variations: nue, nuebar, numu, numubar, RHC and FHC
    neutrinoTypes = ["nue","nuebar","numu","numubar"]
    currentType   = ["FHC","RHC"]

    # Take the central value for both RHC and FHC, all neutrino types
    CV_FileFHC  = rootInputDir+"/FHC/output_uboone_fhc_run0_set1.root"

    plotName  = "nue/Detsmear/nue_CV_AV_TPC"
    CV_FHC_Histos_Nue    =  getHisto(CV_FileFHC, plotName, "FHC_CV_nue_CV_AV_TPC")
    plotName  = "nuebar/Detsmear/nuebar_CV_AV_TPC"
    CV_FHC_Histos_NueBar =  getHisto(CV_FileFHC, plotName, "FHC_CV_nuebar_CV_AV_TPC")
                
    # Declare Variations Ouput
    outputFile = TFile("NuMI_NueNueBar.root","recreate")
    outputFile.cd()

    
    # Calculate the ratio plots
    tmp = CV_FHC_Histos_Nue.Clone("ratio_nueOverNuebar_CV_AV_TPC")
    tmp = DivideHistos(tmp, CV_FHC_Histos_NueBar)
    tmp.SetTitle(";Energy;nue/nuebar")
    outputFile.Add(tmp)
    outputFile.Write()
    outputFile.Close()
__main__()

