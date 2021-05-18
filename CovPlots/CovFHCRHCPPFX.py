import os
import uproot
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
from scipy.stats import chisquare


def calculateCov(fhc_list, rhc_list):
        print(type(fhc_list),type(fhc_list[0]), (fhc_list[0]).shape)
        fhc = np.concatenate(fhc_list,axis=0)
        rhc = np.concatenate(rhc_list,axis=0)

        debug = True
        if debug:
                fhc *= 1000000000
                rhc = fhc
                
        mean_fhc = fhc.mean(axis=0)
        mean_rhc = rhc.mean(axis=0)

        fhc = fhc - mean_fhc
        rhc = rhc - mean_rhc
        print(fhc.shape)
        fhc_std = fhc.std(axis=0,ddof=10)
        rhc_std = rhc.std(axis=0,ddof=10)
        den = (fhc_std.reshape(10,1))@(rhc_std.reshape(1,10))
        print(fhc_std.shape, den.shape,"STD")
        matrix = fhc.T @ rhc
        assert np.allclose(matrix,matrix.T)
        matrix_spearson = matrix/den
        #matrix = np.log(np.abs(matrix))
        print(matrix_spearson)
        fig, ax = plt.subplots()
        ax.imshow(matrix_spearson)
        plt.show()


def __main__():
    from os import listdir
    from os.path import isfile, join
    fhcFileName = "/Users/elenag/Desktop/PlotterLEE/NuMIFlux/variationsFiles/FHC/merged/output_uboone_fhc_run0_merged.root"
    rhcFileName = "/Users/elenag/Desktop/PlotterLEE/NuMIFlux/variationsFiles/RHC/merged/output_uboone_rhc_run0_merged.root"
    
    fhcHisto_nue     = uproot.open(fhcFileName)['nue/Multisims']
    rhcHisto_nue     = uproot.open(rhcFileName)['nue/Multisims']


    uniTemplate = ['nue_ppfx_mippk_PPFXMIPPKaon'         ,'nue_ppfx_mipppi_PPFXMIPPPion' ,'nue_ppfx_other_PPFXOther',
                   'nue_ppfx_targatt_PPFXTargAtten'      ,'nue_ppfx_think_PPFXThinKaon'  ,'nue_ppfx_thinmes_PPFXThinMeson',
                   'nue_ppfx_thinnpi_PPFXThinNeutronPion','nue_thinna_PPFXThinNucA'      ,'nue_thinn_PPFXThinNuc'         ,
                   'nue_ppfx_thinpi_PPFXThinPion'        ,'nue_ppfx_totabs_PPFXTotAbsorp','nue_ppfx_ms_UBPPFX']


    for name in uniTemplate :
        fhc_list = []
        rhc_list = []
        for i in range(600):
                fhc_tmp = (fhcHisto_nue[name+'_Uni_'+str(i)+'_AV_TPC']).allvalues
                rhc_tmp = (rhcHisto_nue[name+'_Uni_'+str(i)+'_AV_TPC']).allvalues
                index = [10,11,12,13,14,15,16,17,18,19]
                fhc_tmp = np.delete(fhc_tmp, index)
                rhc_tmp = np.delete(rhc_tmp, index)
                fhc_list.append(fhc_tmp.reshape(1,10))
                rhc_list.append(rhc_tmp.reshape(1,10))
        calculateCov(fhc_list,rhc_list)
        break



def testUnit():
        fhc_list = [np.array([1,2,3,4,5,6,7,8,9,10]).reshape(1,10), np.array([0,1,2,3,4,5,6,7,8,9]).reshape(1,10) ]
        rhc_list = [np.array([10,20,30,40,50,60,70,80,90,100]).reshape(1,10), np.array([0,10,20,30,40,50,60,70,80,90]).reshape(1,10) ]
        
        calculateCov(fhc_list,rhc_list)

__main__()
#testUnit()
