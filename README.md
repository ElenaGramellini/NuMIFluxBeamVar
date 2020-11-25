# NuMIFluxBeamVar

If working on the UBooNE Servers,
Setup your environement as follows
> source setup.sh


If you're working on your local machine, you just need to setup the environmental variable

> export  BeamVarPath='<the correct path>'

to the location of the folder containing the beamline files.

NB: the code expects the FHC and RHC files to be stored separately in folders named "FHC" and "RHC" respectively.

Create simple flux plots

> cd SimpleFluxPlots

> python MakeFluxHisto.py

Create the ratio plots

> cd Systematics

> python CalculateRatioHistograms.py
