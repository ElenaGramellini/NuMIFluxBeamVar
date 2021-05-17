####################################
## This is a simple python script to 
## plot the flux histograms
##
## Just run:
## > python MakeFluxHisto.py
## output: the file w/ the flux histograms
####################################

from ROOT import *
import os
from ROOT import SetOwnership

# Where are the inputFiles?
rootInputDir = os.environ['BeamVarPath']

gStyle.SetOptStat(0)

def getHisto(fileName, histoName,  color,style,pol="FHC"):
    print(fileName)
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
    tmp0.SetTitle("Neutrino Predicted Flux; Neutrino Energy [GeV]; N #nu/50MeV/m^{2}/10^{6}POT")
    tmp0.GetYaxis().SetTitleOffset(1.5)
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
    
    # RHC
    onlyfilesrhc = rootInputDir+"/RHC/output_uboone_rhc_run0_set1.root"
    nueR      = getHisto(onlyfilesrhc,'nue/Detsmear/nue_CV_AV_TPC_5MeV_bin'        , kBlue ,1,"RHC")
    antinueR  = getHisto(onlyfilesrhc,'nuebar/Detsmear/nuebar_CV_AV_TPC_5MeV_bin'  , kBlue ,3,"RHC")
    
    c1 = TCanvas("cFHC","cFHC",600,600)
    c1.cd()
    c1.SetLogy()
    c1.SetGrid()
    nueF.SetTitleOffset(1.)
    nueF.SetTitle("Neutrino Predicted Flux; Neutrino Energy [GeV]; N #nu/50MeV/m^{2}/10^{6}POT")
    nueF     .GetXaxis().SetRangeUser(0.,2.5)
    nueF     .Draw("histo")
    nueR     .GetXaxis().SetRangeUser(0.,2.5)
    nueR     .Draw("histosame")
        
    leg1 = TLegend(0.38,0.65,0.80,0.78)
    SetOwnership( leg1, 0 ) # 0 = release (not keep), 1 = kee
    leg1.AddEntry(nueF     ,"FHC #nu_{e}")
    leg1.AddEntry(nueR     ,"RHC #nu_{e}")
    leg1.Draw("same")

    c1.SaveAs("ENeutrinoFluxes.pdf")
    c1.Update()

    
    c2 = TCanvas("cRHC","cRHC",600,600)
    c2.cd()
    c2.SetLogy()
    c2.SetGrid()
    antinueF.SetTitleOffset(1.)
    antinueF.SetTitle("AntiNeutrino Predicted Flux; Neutrino Energy [GeV]; N #nu/50MeV/m^{2}/10^{6}POT")
    antinueF .GetXaxis().SetRangeUser(0.,2.5)
    antinueF .Draw("histo")
    antinueR .GetXaxis().SetRangeUser(0.,2.5)
    antinueR .Draw("histosame")
    leg2 = TLegend(0.38,0.65,0.80,0.78)
    SetOwnership( leg2, 0 ) # 0 = release (not keep), 1 = kee
    leg2.AddEntry(antinueF ,"FHC #bar#nu_{e}")
    leg2.AddEntry(antinueR ,"RHC #bar#nu_{e}")
    leg2.Draw("same")
    c2.Update()    
    c2.SaveAs("EAntiNeutrinoFluxes.pdf")

    
__main__()
input()
