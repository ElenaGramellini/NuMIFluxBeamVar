from ROOT import *


gStyle.SetOptStat(0)
def getHistograms(fileName,color,rebin=1):
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


    
    tmp0   .SetTitle("NuE; True Neutrino Energy [GeV];Relative Flux Diff: (CV - Var22) / CV ") 
    tmp1   .SetTitle("NuEBar; True Neutrino Energy [GeV];Relative Flux Diff: (CV - Var22) / CV ") 
    tmp2   .SetTitle("NuMu; True Neutrino Energy [GeV];Relative Flux Diff: (CV - Var22) / CV ") 
    tmp3   .SetTitle("NuMuBar; True Neutrino Energy [GeV];Relative Flux Diff: (CV - Var22) / CV ") 
    tmpAll .SetTitle("AllNu; True Neutrino Energy [GeV];Relative Flux Diff: (CV - Var22) / CV ") 
    
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
    tmp0.SetLineColor(color+1)
    tmp1.SetLineColor(color+2)
    tmp2.SetLineColor(color-1)
    tmp3.SetLineColor(color+3)
    tmpAll.SetLineColor(color)
    tmp0.SetLineWidth(2)
    tmp1.SetLineWidth(2)
    tmp2.SetLineWidth(2)
    tmp3.SetLineWidth(2)
    tmpAll.SetLineWidth(2)

    # Create total flux histogram
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
    execute()

     


def execute(VariationName = "run22", rebin = 2000 ):   
    fhc_histosVar = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/FHC/output_uboone_fhc_'+VariationName+'.root',kRed,rebin)
    rhc_histosVar = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/RHC/output_uboone_rhc_'+VariationName+'.root',kBlue,rebin)

    fhc_histosCV = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/FHC/output_uboone_fhc_run0_set1.root',kRed,rebin)
    rhc_histosCV = getHistograms('/Users/elenag/Desktop/NuMI/Flux/variationsFiles/RHC/output_uboone_rhc_run0_set1.root',kBlue,rebin)
    plotCV = False
    if plotCV :
        c = TCanvas("c","c",1800,600)
        c.cd()
        c.SetGrid()
        yrange = [0.001,0.001,0.1,0.1,0.1]
        for i in xrange(0,5):
            fhc_histosCV[i].GetXaxis().SetRangeUser(0.06,5.)
            fhc_histosCV[i].GetYaxis().SetRangeUser(0.,yrange[i])
            fhc_histosCV[i].Draw("histo")
            rhc_histosCV[i].Draw("histosame")
            legend = TLegend(0.5,0.2,0.8,0.4)
            legend.AddEntry(fhc_histosCV[i],"FHC")
            legend.AddEntry(rhc_histosCV[i],"RHC")
            legend.Draw("same")
            c.Update()
            c.SaveAs("BFieldVar22Covariance/"+fhc_histosCV[i].GetTitle()+"_CV.png")
            #raw_input()    
    
    diff_FHC = []
    diff_RHC = []

    for i in xrange(0,5):
        tempFHC = fhc_histosCV[i].Clone(fhc_histosCV[i].GetTitle()+"_FHC_Diff")
        tempFHC.SetDirectory(gROOT)
        tempFHC.Add(fhc_histosVar[i], -1)
        tempFHC.Divide(fhc_histosCV[i])
        diff_FHC.append(tempFHC)


        tempRHC = rhc_histosCV[i].Clone(rhc_histosCV[i].GetTitle()+"_RHC_Diff")
        tempRHC.SetDirectory(gROOT)
        tempRHC.Add(rhc_histosVar[i], -1)
        tempRHC.Divide(rhc_histosCV[i])
        diff_RHC.append(tempRHC)

        c1 = TCanvas("c1","c1",1800,600)
        c1.cd()
        c1.SetGrid()

        tempFHC.GetXaxis().SetRangeUser(0.0,5.)
        tempFHC.GetYaxis().SetRangeUser(-0.2,0.2)
        tempFHC.Draw("histo")
        tempRHC.Draw("histosame")
        legend1 = TLegend(0.15,0.15,0.25,0.35)
        legend1.AddEntry(tempFHC,"FHC")
        legend1.AddEntry(tempRHC,"RHC")
        legend1.Draw("same")
        c1.Update()
        #raw_input()
        c1.SaveAs("BFieldVar22Covariance/"+tempFHC.GetTitle()+"_"+VariationName+"_Diff.png")

    
        NuSpeciesName = diff_FHC[i].GetTitle()
        print NuSpeciesName,  diff_FHC[i].GetSize(),    diff_FHC[i].GetSize()
        f = open("BFieldVar22Covariance/"+NuSpeciesName+"_"+VariationName+"_NBins"+str(diff_FHC[i].GetSize()-2)+".csv", "w")
        f.write("energy FHC RHC\n")
        for j in xrange(1,diff_FHC[i].GetSize()-2):
            tupla = str(diff_FHC[i].GetBinCenter(j)) +" "+ str(diff_FHC[i].GetBinContent(j)) +" "+ str(diff_RHC[i].GetBinContent(j))+"\n"
            f.write(tupla)
        f.close()
__main__()
