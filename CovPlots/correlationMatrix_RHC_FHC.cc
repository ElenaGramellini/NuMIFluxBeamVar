#include <TFile.h>
#include <TH1D.h>

void CalcCovariance(std::vector<TH1D*> h_universe, TH1D *h_CV, TH2D *h_cov){

    for (unsigned int uni = 0; uni < h_universe.size(); uni++){
        
        // Loop over the rows
        for (int row = 1; row < h_CV->GetNbinsX()+1; row++){
            
            double uni_row = h_universe.at(uni)->GetBinContent(row);
            double cv_row  = h_CV->GetBinContent(row);

            // Loop over the columns
            for (int col = 1; col < h_CV->GetNbinsX()+1; col++){

                double uni_col = h_universe.at(uni)->GetBinContent(col);
                double cv_col  = h_CV->GetBinContent(col);
                
                double c = (uni_row - cv_row) * (uni_col - cv_col);

                if (uni != h_universe.size()-1)    h_cov->SetBinContent(row, col, h_cov->GetBinContent(row, col) + c ); // Fill with variance 
                else h_cov->SetBinContent(row, col, (h_cov->GetBinContent(row, col) + c) / h_universe.size());          // Fill with variance and divide by nuni
            
            } // end loop over columns

        } // end loop over rows
    
    } // end loop over universes

}

void CalcCorrelation(TH1D *h_CV, TH2D *h_cov, TH2D *h_cor){

    double cor_bini;
    
    // loop over rows
    for (int row = 1; row < h_CV->GetNbinsX()+1; row++) {
        
        double cii = h_cov->GetBinContent(row, row);

        // Loop over columns
        for (int col = 1; col < h_CV->GetNbinsX()+1; col++) {
            
            double cjj = h_cov->GetBinContent(col, col);
            
            double n = sqrt(cii * cjj);

            // Catch Zeros, set to arbitary 1.0
            if (n == 0) cor_bini = 0;
            else cor_bini = h_cov->GetBinContent(row, col) / n;

            h_cor->SetBinContent(row, col, cor_bini );
        
        } // end loop over rows

    } // end loop over columns

}

void CalcCFracCovariance(TH1D *h_CV, TH2D *h_frac_cov){

    // ** Requires the input frac cov to be a cloned version of the covariance matrix **

    double setbin;
   
    // loop over rows
    for (int row = 1; row < h_CV->GetNbinsX()+1; row++) {
       
       double cii = h_CV->GetBinContent(row);

        // Loop over columns
        for (int col = 1; col < h_CV->GetNbinsX()+1; col++) {
            double cjj = h_CV->GetBinContent(col);
            double n = cii * cjj;

            // Catch Zeros, set to arbitary 0
            if (n == 0) setbin = 0;
            else setbin = h_frac_cov->GetBinContent(row, col) / n;

            h_frac_cov->SetBinContent(row, col, setbin );
        
        } // end loop over the columns
    
    } // end loop over the rows

}

void correlationMatrix_RHC_FHC(){

    // ---------------------
    // --- input information
    // ---------------------

    std::string fhcFileName = "../files/output_uboone_fhc_run0_merged.root";
    std::string rhcFileName = "../files/output_uboone_rhc_run0_merged.root";
    int run_period = 1;                      // run number used for printing a watermark on the plot
    std::string hd_mode = "UBPPFX";          // hadron production mode 
    int nuniverses = 600;                    // number of universes

    // ----------------
    // --- import files
    // ----------------

    std::cout << "\nImporting files" << std::endl;
    std::cout << "   FHC: " << fhcFileName << std::endl;
    std::cout << "   RHC: " << rhcFileName << std::endl;

    TFile *fhc_run0 = TFile::Open(fhcFileName.c_str(),"READ");
    TFile *rhc_run0 = TFile::Open(rhcFileName.c_str(),"READ");

    // ----------------------------------------------------------
    // --- enum for the models we want the correlation matrix for
    // ----------------------------------------------------------

    enum enum_flav { k_numu, k_numubar, k_nue, k_nuebar, k_FLAV_MAX};
    std::vector<std::string> flav = {"numu", "numubar", "nue", "nuebar"}; // name should match to the histogram in the root file

    // --------------------------------------------
    // --- importing histograms for FHC, RHC and CV
    // --------------------------------------------

    std::vector<TH1D*> hist_unwrap_CV_fhc;
    hist_unwrap_CV_fhc.resize(k_FLAV_MAX);
    std::vector<std::vector<TH1D*>> hist_unwrap_fhc;
    hist_unwrap_fhc.resize(k_FLAV_MAX);

    std::vector<TH1D*> hist_unwrap_CV_rhc;
    hist_unwrap_CV_rhc.resize(k_FLAV_MAX);
    std::vector<std::vector<TH1D*>> hist_unwrap_rhc;
    hist_unwrap_rhc.resize(k_FLAV_MAX);

    std::cout << "\nImporting histograms (universes & CV)" << std::endl;
    for(unsigned int flavor=0; flavor<hist_unwrap_fhc.size(); flavor++) { 
        
        hist_unwrap_fhc.at(flavor).resize(nuniverses); // create one histogram per universe for FHC
        hist_unwrap_rhc.at(flavor).resize(nuniverses); // create one histogram per universe for RHC

        // loop over universes and get the histograms for FHC and RHC
        for(unsigned int uni=0; uni<hist_unwrap_fhc.at(flavor).size(); uni++){

            // FHC
            fhc_run0->cd();
            hist_unwrap_fhc.at(flavor).at(uni) = (TH1D*)fhc_run0->Get(Form("%s/Multisims/%s_ppfx_ms_%s_Uni_%d_AV_TPC", flav.at(flavor).c_str(), flav.at(flavor).c_str(), hd_mode.c_str(), uni));

            // RHC
            rhc_run0->cd();
            hist_unwrap_rhc.at(flavor).at(uni) = (TH1D*)rhc_run0->Get(Form("%s/Multisims/%s_ppfx_ms_%s_Uni_%d_AV_TPC", flav.at(flavor).c_str(), flav.at(flavor).c_str(), hd_mode.c_str(), uni));

        }

        // get CV histograms
        fhc_run0->cd();
        hist_unwrap_CV_fhc.at(flavor) = (TH1D*)fhc_run0->Get(Form("%s/Detsmear/%s_CV_AV_TPC", flav.at(flavor).c_str(), flav.at(flavor).c_str()));

        rhc_run0->cd();
        hist_unwrap_CV_rhc.at(flavor) = (TH1D*)rhc_run0->Get(Form("%s/Detsmear/%s_CV_AV_TPC", flav.at(flavor).c_str(), flav.at(flavor).c_str()));
    }

    // ---------------------------------------------
    // --- stitching histograms together (UNIVERSES)
    // ---------------------------------------------

    std::cout << "\nStitching histograms together (universes)" << std::endl;

    std::vector<TH1D*> hist_unwrap_stitch;
    hist_unwrap_stitch.resize(nuniverses);

    for(unsigned int uni=0; uni<nuniverses; uni++){

        // create the stitched histogram
        // this is going to be a single histogram that is going to be equivalent to putting numu, numubar, nue, nuebar for FHC and RHC next to each other
        // so we need to find out the number of bins we need for this "stitched" histogram
        const int nBins_fhc = hist_unwrap_fhc.at(k_numu).at(0)->GetNbinsX() + hist_unwrap_fhc.at(k_numubar).at(0)->GetNbinsX() + hist_unwrap_fhc.at(k_nue).at(0)->GetNbinsX() + hist_unwrap_fhc.at(k_nuebar).at(0)->GetNbinsX();
        const int nBins_rhc = hist_unwrap_rhc.at(k_numu).at(0)->GetNbinsX() + hist_unwrap_rhc.at(k_numubar).at(0)->GetNbinsX() + hist_unwrap_rhc.at(k_nue).at(0)->GetNbinsX() + hist_unwrap_rhc.at(k_nuebar).at(0)->GetNbinsX();
        const int nBins = nBins_fhc + nBins_rhc;

        // now we create a vector that will contain the bin content for all the histograms attached next to each other
        std::vector<double> values;

        // FHC
        for(unsigned int flav=0; flav<k_FLAV_MAX; flav++){
            for(unsigned int bin=1; bin<hist_unwrap_fhc.at(flav).at(uni)->GetXaxis()->GetNbins()+1; bin++){
                values.push_back(hist_unwrap_fhc.at(flav).at(uni)->GetBinContent(bin));
            }
        }

        // RHC
        for(unsigned int flav=0; flav<k_FLAV_MAX; flav++){
            for(unsigned int bin=1; bin<hist_unwrap_rhc.at(flav).at(uni)->GetXaxis()->GetNbins()+1; bin++){
                values.push_back(hist_unwrap_rhc.at(flav).at(uni)->GetBinContent(bin));
            }
        }

        // stitching histograms together
        hist_unwrap_stitch.at(uni) = new TH1D("","",nBins,0,nBins);
        for(unsigned int bin=1; bin<values.size()+1; bin++){
            hist_unwrap_stitch.at(uni)->SetBinContent(bin,values.at(bin-1));
        }

    }

    // --------------------------------------
    // --- stitching histograms together (CV)
    // --------------------------------------

    std::cout << "\nStitching histograms together (CV)" << std::endl;

    const int nBins_fhc = hist_unwrap_CV_fhc.at(k_numu)->GetNbinsX() + hist_unwrap_CV_fhc.at(k_numubar)->GetNbinsX() + hist_unwrap_CV_fhc.at(k_nue)->GetNbinsX() + hist_unwrap_CV_fhc.at(k_nuebar)->GetNbinsX();
    const int nBins_rhc = hist_unwrap_CV_rhc.at(k_numu)->GetNbinsX() + hist_unwrap_CV_rhc.at(k_numubar)->GetNbinsX() + hist_unwrap_CV_rhc.at(k_nue)->GetNbinsX() + hist_unwrap_CV_rhc.at(k_nuebar)->GetNbinsX();
    const int nBins = nBins_fhc + nBins_rhc;
    TH1D* hist_unwrap_stitch_CV = new TH1D("","",nBins,0,nBins);

    std::vector<double> values;

    // FHC
    for(unsigned int flav=0; flav<k_FLAV_MAX; flav++){
        for(unsigned int bin=1; bin<hist_unwrap_CV_fhc.at(flav)->GetXaxis()->GetNbins()+1; bin++){
            values.push_back(hist_unwrap_CV_fhc.at(flav)->GetBinContent(bin));
        }
    }

    // RHC
    for(unsigned int flav=0; flav<k_FLAV_MAX; flav++){
        for(unsigned int bin=1; bin<hist_unwrap_CV_rhc.at(flav)->GetXaxis()->GetNbins()+1; bin++){
            values.push_back(hist_unwrap_CV_rhc.at(flav)->GetBinContent(bin));
        }
    }

    for(unsigned int bin=1; bin<values.size()+1; bin++){
        hist_unwrap_stitch_CV->SetBinContent(bin,values.at(bin-1));
    }

    // --------------------------------
    // --- create the covariance matrix
    // --------------------------------

    // draw vertical lines to help the eye
    int numu_bin_fhc    = hist_unwrap_CV_fhc.at(k_numu)->GetNbinsX() + 1;
    int numubar_bin_fhc = numu_bin_fhc + hist_unwrap_CV_fhc.at(k_numubar)->GetNbinsX();
    int nue_bin_fhc     = numubar_bin_fhc + hist_unwrap_CV_fhc.at(k_nue)->GetNbinsX();
    int nuebar_bin_fhc  = nue_bin_fhc + hist_unwrap_CV_fhc.at(k_nuebar)->GetNbinsX();
    int numu_bin_rhc    = nuebar_bin_fhc + hist_unwrap_CV_rhc.at(k_numu)->GetNbinsX();
    int numubar_bin_rhc = numu_bin_rhc + hist_unwrap_CV_rhc.at(k_numubar)->GetNbinsX();
    int nue_bin_rhc     = numubar_bin_rhc + hist_unwrap_CV_rhc.at(k_nue)->GetNbinsX();
    int nuebar_bin_rhc  = nue_bin_rhc + hist_unwrap_CV_rhc.at(k_nuebar)->GetNbinsX();

    std::vector<TLine*> line(14);
    line.at(0) = new TLine(numu_bin_fhc   , 1, numu_bin_fhc   , nuebar_bin_rhc);
    line.at(1) = new TLine(numubar_bin_fhc, 1, numubar_bin_fhc, nuebar_bin_rhc);
    line.at(2) = new TLine(nue_bin_fhc    , 1, nue_bin_fhc    , nuebar_bin_rhc);
    line.at(3) = new TLine(nuebar_bin_fhc , 1, nuebar_bin_fhc , nuebar_bin_rhc);
    line.at(4) = new TLine(numu_bin_rhc   , 1, numu_bin_rhc   , nuebar_bin_rhc);
    line.at(5) = new TLine(numubar_bin_rhc, 1, numubar_bin_rhc, nuebar_bin_rhc);
    line.at(6) = new TLine(nue_bin_rhc    , 1, nue_bin_rhc    , nuebar_bin_rhc);
    line.at(7) = new TLine(1, numu_bin_fhc   , nuebar_bin_rhc, numu_bin_fhc);
    line.at(8) = new TLine(1, numubar_bin_fhc, nuebar_bin_rhc, numubar_bin_fhc);
    line.at(9) = new TLine(1, nue_bin_fhc, nuebar_bin_rhc, nue_bin_fhc);
    line.at(10) = new TLine(1, nuebar_bin_fhc, nuebar_bin_rhc, nuebar_bin_fhc);
    line.at(11) = new TLine(1, numu_bin_rhc   , nuebar_bin_rhc, numu_bin_rhc);
    line.at(12) = new TLine(1, numubar_bin_rhc, nuebar_bin_rhc, numubar_bin_rhc);
    line.at(13) = new TLine(1, nue_bin_rhc, nuebar_bin_rhc, nue_bin_rhc);

    const int n_bins = hist_unwrap_stitch.at(0)->GetNbinsX();
    TH2D* h_cov = new TH2D("","Covariance Matrix; Bin i; Bin j", n_bins, 1, n_bins+1, n_bins, 1, n_bins+1);

    CalcCovariance(hist_unwrap_stitch, hist_unwrap_stitch_CV, h_cov);

    gStyle->SetOptStat(0);

    TH2D* h_cor = (TH2D*)h_cov->Clone();
    TH2D* h_frac_cov = (TH2D*)h_cov->Clone();
    CalcCorrelation(hist_unwrap_stitch_CV, h_cov, h_cor);
    CalcCFracCovariance(hist_unwrap_stitch_CV, h_frac_cov);

    TCanvas *c = new TCanvas("", "", 500, 500);
    h_cov->Draw("colz");
    for (unsigned int i = 0; i< line.size(); i++){
        line.at(i)->SetLineColor(kRed+2);
        line.at(i)->SetLineWidth(4);
        line.at(i)->Draw();
    }
    c->Print("covariance.pdf");

    TCanvas *c2 = new TCanvas("", "", 700, 700);
    gPad->SetLeftMargin(0.14);
    gPad->SetRightMargin(0.14);
    gPad->SetTopMargin(0.14);
    gPad->SetBottomMargin(0.14);
    h_cor->SetTitle("Correlation Matrix ;Bin i; Bin j");
    h_cor->GetZaxis()->SetRangeUser(-1,1);
    h_cor->Draw("colz");
    for (unsigned int i = 0; i< line.size(); i++){
        line.at(i)->SetLineColor(kRed+2);
        line.at(i)->SetLineWidth(4);
        line.at(i)->Draw();
    }

    c2->Print(Form("correlation_%s_run%d.pdf", hd_mode.c_str(), run_period));

}