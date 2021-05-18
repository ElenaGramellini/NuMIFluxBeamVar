from ROOT import *


gStyle.SetOptStat(0)
def getHistograms(fileName,style,rebin=1):
    # Get Files
    file          = TFile(fileName,"r")  
    nueString     = "nue/Detsmear/nue_CV_AV_TPC_5MeV_bin"
    nueBarString  = "nuebar/Detsmear/nuebar_CV_AV_TPC_5MeV_bin"
    numuString    = "numu/Detsmear/numu_CV_AV_TPC_5MeV_bin"
    numuBarString = "numubar/Detsmear/numubar_CV_AV_TPC_5MeV_bin"

    bigBins = False
    if bigBins:
        nueString     = "nue/Detsmear/nue_CV_AV_TPC"
        nueBarString  = "nuebar/Detsmear/nuebar_CV_AV_TPC"
        numuString    = "numu/Detsmear/numu_CV_AV_TPC"
        numuBarString = "numubar/Detsmear/numubar_CV_AV_TPC"

    tmp0   = file.Get(nueString)
    tmp1   = file.Get(nueBarString)
    tmp2   = file.Get(numuString)
    tmp3   = file.Get(numuBarString)
    tmpAll = tmp0.Clone("allNu")

    tmp0   .Rebin(rebin) 
    tmp1   .Rebin(rebin) 
    tmp2   .Rebin(rebin) 
    tmp3   .Rebin(rebin) 
    tmpAll .Rebin(rebin) 

    
    tmp0   .SetTitle("NuE CV; True Neutrino Energy [GeV];POT Norm Flux [A.U.] ") 
    tmp1   .SetTitle("NuEBar CV; True Neutrino Energy [GeV];POT Norm Flux [A.U.] ") 
    tmp2   .SetTitle("NuMu CV; True Neutrino Energy [GeV];POT Norm Flux [A.U.] ") 
    tmp3   .SetTitle("NuMuBar CV; True Neutrino Energy [GeV];POT Norm Flux [A.U.] ") 
    tmpAll .SetTitle("AllNu CV; True Neutrino Energy [GeV];POT Norm Flux [A.U.] ") 
    
    # Get Simulated POT
    ttree  = file.Get("POT")
    POT    = float(ttree.GetEntries())

    # Set directory so root is happy
    tmp0.SetDirectory(gROOT)
    tmp1.SetDirectory(gROOT)
    tmp2.SetDirectory(gROOT)
    tmp3.SetDirectory(gROOT)
    tmpAll.SetDirectory(gROOT)

    # Cosmetic stuff
    tmp0.SetLineColor(kBlue)
    tmp1.SetLineColor(kRed)
    tmp2.SetLineColor(kBlue)
    tmp3.SetLineColor(kRed)
    tmpAll.SetLineColor(kBlack)

    tmp0.SetLineStyle(style)
    tmp1.SetLineStyle(style)
    tmp2.SetLineStyle(style)
    tmp3.SetLineStyle(style)
    tmpAll.SetLineStyle(style)

    tmp0.SetLineWidth(4)
    tmp1.SetLineWidth(4)
    tmp2.SetLineWidth(4)
    tmp3.SetLineWidth(4)
    tmpAll.SetLineWidth(4)

    # Create total flux histogram
    if not bigBins:
        tmpAll.Add(tmp1)
        tmpAll.Add(tmp2)
        tmpAll.Add(tmp3)

    # Normalize per simulated POT
    tmp0.Scale(1./POT)
    tmp1.Scale(1./POT)
    tmp2.Scale(1./POT)
    tmp3.Scale(1./POT)
    tmpAll.Scale(1./POT)

    return tmp0,tmp1,tmp2,tmp3,tmpAll



def __main__():
    rebin = 1 
    fhc_histosCV = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/FHC/output_uboone_fhc_run0_set1.root',1,rebin)
    rhc_histosCV = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/RHC/output_uboone_rhc_run0_set1.root',5,rebin)
    plotCV = True
    if plotCV :
        c = TCanvas("c","c",1800,600)
        c.cd()
        c.SetGrid()
        yrange = [0.001,0.001,0.1,0.1,0.1]

        fhc_histosCV[4].GetXaxis().SetRangeUser(0.,3.)
        fhc_histosCV[4].GetYaxis().SetRangeUser(0.,yrange[4])
        fhc_histosCV[4].Draw("histo")
        rhc_histosCV[4].Draw("histosame")
        legend = TLegend(0.5,0.5,0.8,0.7)
        legend.AddEntry(fhc_histosCV[4],"FHC")
        legend.AddEntry(rhc_histosCV[4],"RHC")
        legend.Draw("same")
        c.Update()
        c.SaveAs("CVPlots/"+fhc_histosCV[4].GetTitle()+"_CV.png")
            #raw_input()    
        puppa = [0,2]
        for i in puppa:    
            fhc_histosCV[i].GetXaxis().SetRangeUser(0.,1.)
            fhc_histosCV[i].GetYaxis().SetRangeUser(0.,0.05*fhc_histosCV[i].GetMaximum())
            fhc_histosCV[i].GetYaxis().SetRangeUser(0.,yrange[i])
            fhc_histosCV[i].Draw("histo")
            fhc_histosCV[i+1].Draw("histosame")
            rhc_histosCV[i].Draw("histosame")
            rhc_histosCV[i+1].Draw("histosame")
            legend = TLegend(0.5,0.5,0.8,0.7)
            legend.AddEntry(fhc_histosCV[i],"FHC Nu")
            legend.AddEntry(rhc_histosCV[i],"RHC Nu")
            legend.AddEntry(fhc_histosCV[i+1],"FHC Nu Bar")
            legend.AddEntry(rhc_histosCV[i+1],"RHC Nu Bar")
            legend.Draw("same")
            c.Update()
            c.SaveAs("CVPlots/"+fhc_histosCV[i].GetTitle()+"_CV.png")


__main__()
