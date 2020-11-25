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

    tmp0   = file.Get(histoName)
    tmp0.SetDirectory(gROOT)
    tmp0.SetTitle(name)
    tmp0.Scale(1./POT)
    file.Close()
    return tmp0


def DivideHistos(var, cv):
    neutrinoTypes = ["nue_","nuebar_","numu_","numubar_"]
    check = 0
    for n in neutrinoTypes:
        if n in var.GetTitle() and n in cv.GetTitle():
            check += 1
    if check != 1:
        print "Wrong Check ", var.GetTitle(), cv.GetTitle()
    #tmp1 = var.Clone("ratio"+var.GetTitle())
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
    # fetch the variation giles
    onlyfilesfhc = [f for f in listdir(rootInputDir+"/FHC") if isfile(join(rootInputDir+"/FHC", f))]
    onlyfilesrhc = [f for f in listdir(rootInputDir+"/RHC") if isfile(join(rootInputDir+"/RHC", f))]
    onlyfilesfhc = [x.replace('output_uboone_fhc_', '').replace('', '') for x in onlyfilesfhc]
    onlyfilesrhc = [x.replace('output_uboone_rhc_', '').replace('', '') for x in onlyfilesrhc]
    onlyfilesfhc = [x.replace('.root', '').replace('', '') for x in onlyfilesfhc]
    onlyfilesrhc = [x.replace('.root', '').replace('', '') for x in onlyfilesrhc]

    #This are the runs currently available to you
    overlap = list(set(onlyfilesfhc) & set(onlyfilesrhc))
    overlap = [ x for x in overlap if ("run0" not in x) and ("run21" not in x) and ("run22" not in x) and ("run23" not in x)]

    # We are going to plot all the possible variations: nue, nuebar, numu, numubar, RHC and FHC
    neutrinoTypes = ["nue","nuebar","numu","numubar"]
    currentType   = ["FHC","RHC"]

    # Take the central value for both RHC and FHC, all neutrino types
    CV_FileFHC  = rootInputDir+"/FHC/output_uboone_fhc_run0_set1.root"
    CV_FileRHC  = rootInputDir+"/RHC/output_uboone_rhc_run0_set1.root"
    CV_FHC_HistosVarB = []
    CV_RHC_HistosVarB = []
    CV_FHC_Histos   = []
    CV_RHC_Histos   = []
    CV_FHC_HistosTh = []
    CV_RHC_HistosTh = []
    CV_FHC_Histos2D = []
    CV_RHC_Histos2D = []
    for neutrino in neutrinoTypes:
        plotName  = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC"
        CV_FHC_HistosVarB  .append( getHisto(CV_FileFHC, plotName, "FHC_CV_"+neutrino+"_CV_AV_TPC") )
        CV_RHC_HistosVarB  .append( getHisto(CV_FileRHC, plotName, "RHC_CV_"+neutrino+"_CV_AV_TPC") )
        plotName  = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC_5MeV_bin"
        CV_FHC_Histos  .append( getHisto(CV_FileFHC, plotName, "FHC_CV_"+neutrino+"_CV_AV_TPC_5MeV_bin") )
        CV_RHC_Histos  .append( getHisto(CV_FileRHC, plotName, "RHC_CV_"+neutrino+"_CV_AV_TPC_5MeV_bin") )
        plotName  = neutrino+"/Detsmear/Th_"+neutrino+"_CV_TPC"
        CV_FHC_HistosTh.append( getHisto(CV_FileFHC, plotName, "FHC_CV_"+neutrino+"_CV_TPC_Th") )
        CV_RHC_HistosTh.append( getHisto(CV_FileRHC, plotName, "RHC_CV_"+neutrino+"_CV_TPC_Th") )
        plotName  = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC_2D"
        CV_FHC_Histos2D.append( getHisto(CV_FileFHC, plotName, "FHC_CV_"+neutrino+"_CV_AV_TPC_2D") )
        CV_RHC_Histos2D.append( getHisto(CV_FileRHC, plotName, "RHC_CV_"+neutrino+"_CV_AV_TPC_2D") )
            
    # Declare Variations Ouput
    outputFile = TFile("NuMI_Beamline_Variations_to_CV_Ratios.root","recreate")
    outputFile.cd()
    subSubD3 = outputFile.mkdir("EnergyVarBin")
    subSubD2 = outputFile.mkdir("Energy")
    subSubD1 = outputFile.mkdir("Theta")
    subSubD0 = outputFile.mkdir("EnergyTheta2D")
    
    for c in currentType:
        for b in overlap:
            fileName = rootInputDir+'/'+c+'/output_uboone_'+c.lower()+'_'+b+'.root'
            # Loop on the neutrino types
            for i, neutrino in enumerate(neutrinoTypes):
                # Ratios of the Energy Histograms at Variable Bin Width
                plotName = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC"
                subSubD2.cd()
                # Loop on the variations
                thisVarHistos = getHisto(fileName, plotName,"ratio"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC")
                # Calculate the ratio plots
                tmp = thisVarHistos.Clone("ratio_"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC")
                if "FHC" in c:
                    tmp = DivideHistos(tmp, CV_FHC_HistosVarB[i])
                else:
                    tmp = DivideHistos(tmp, CV_RHC_HistosVarB[i])
                subSubD3.Add(tmp)

                
                # Ratios of the Energy Histograms
                plotName = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC_5MeV_bin"
                subSubD2.cd()
                # Loop on the variations
                thisVarHistos = getHisto(fileName, plotName,"ratio"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC_5MeV_bin")
                # Calculate the ratio plots
                tmp = thisVarHistos.Clone("ratio_"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC_5MeV_bin")
                if "FHC" in c:
                    tmp = DivideHistos(tmp, CV_FHC_Histos[i])
                else:
                    tmp = DivideHistos(tmp, CV_RHC_Histos[i])
                subSubD2.Add(tmp)

                
                # Ratios of the Theta Histograms
                plotName = neutrino+"/Detsmear/Th_"+neutrino+"_CV_TPC"
                subSubD1.cd()
                # Loop on the variations
                thisVarHistos = getHisto(fileName, plotName,"ratio_Th_"+b+"_"+c+"_"+neutrino+"_CV_TPC")
                # Calculate the ratio plots
                tmp = thisVarHistos.Clone("ratio_Th_"+b+"_"+c+"_"+neutrino+"_CV_TPC")
                if "FHC" in c:
                    tmp = DivideHistos(tmp, CV_FHC_HistosTh[i])
                else:
                    tmp = DivideHistos(tmp, CV_RHC_HistosTh[i])
                subSubD1.Add(tmp)

                # Ratios of the 2D Histograms
                plotName = neutrino+"/Detsmear/"+neutrino+"_CV_AV_TPC_2D"
                subSubD0.cd()
                # Loop on the variations
                thisVarHistos = getHisto(fileName, plotName,"ratio"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC_2D")
                # Calculate the ratio plots
                tmp = thisVarHistos.Clone("ratio_"+b+"_"+c+"_"+neutrino+"_CV_AV_TPC_2D")
                if "FHC" in c:
                    tmp = DivideHistos(tmp, CV_FHC_Histos2D[i])
                else:
                    tmp = DivideHistos(tmp, CV_RHC_Histos2D[i])
                subSubD0.Add(tmp)
    
    outputFile.Write()
    outputFile.Close()
__main__()

