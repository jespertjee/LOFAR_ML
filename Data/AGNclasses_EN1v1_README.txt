This file contains the SF/AGN classifications for the Elais-N1 LOFAR Deep Field data, catalogue v1.0. It is based upon outputs of 5 SED fitting
algorithms, as has been described in various LOFAR telecons and will appear in more detail in Best et al (in prep).

The classification table provides also the output of numerous other classification schemes, or intermediate products, that the user can make
use of, as well as the final proposed classification.

Unless otherwise stated, -99 in a flag for no measurement.

For those just wanting final classifications, AGN_final and RadioAGN_final are the key columns:
AGN_final = flag for whether this is a radiative AGN (ie. optical/IR/X-ray SED evidence)
RadioAGN_final = flag for whether this is a radio-excess AGN

Thus:

AGN_final=0  &  RadioAGN_final=0     -> star-forming galaxy
AGN_final=1  &  RadioAGN_final=0     -> 'radio-quiet' AGN
AGN_final=0  &  RadioAGN_final=1     -> 'jet-mode' radio AGN / low-excitation radio galaxy
AGN_final=1  &  RadioAGN_final=1     -> quasar-like radio AGN / high-excitation radio galaxy 
AGN_final=-1 or RadioAGN_final=-1    -> no secure classification



========================

Column Descriptors

Source_name        The LOFAR source name

Radio_ID           The ID number in the SED fitting input file

Spitzer_SN         1 = above S/N=2 in all 4 Spitzer bands
                   2 = above S/N=3 in all bands; 
                   0 otherwise

Donley             1 = in Donley 2012 IRAC AGN region (and Spitzer_SN >=1, or limits sufficient)
                   0 = outside Donley AGN region (and Spitzer_SN >=1, or limits sufficient)
                  -1 = too low S/N in IRAC bands to tell.

Lacy               1 = in Lacy 2007 IRAC AGN region (and Spitzer_SN >=1, or limits sufficient)
                   0 = outside Lacy AGN region (and Spitzer_SN >=1, or limits sufficient)
                  -1 = too low S/N in IRAC bands to tell.
    
Stern              1 = in Stern 2005 IRAC AGN region (and Spitzer_SN >=1, or limits sufficient)
                   0 = outside Stern AGN region (and Spitzer_SN >=1, or limits sufficient)
                  -1 = too low S/N in IRAC bands to tell.
    
Messias            1 = in Messias 2012 IRAC/24mu AGN region (and Spitzer_SN >=1, and S/N_24mu>2 or limits sufficient)
                   0 = outside Messias AGN region (and Spitzer_SN >=1 and S/N_24mu>2, or limits sufficient)
                  -1 = too low S/N in IRAC/24mu bands to tell.
    
KI                 1 = at z<=1 and in K-IRAC AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                   0 = at z<=1 and not in K-IRAC AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                  -1 = at z<=1 but data not sufficient to classify on KI diagram
		 -99 = not at z<=1

Ch2_Ch4            1 = at 1<z<2.5 and in IRAC Ch2/Ch4 AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                   0 = at 1<z<2.5 and not in IRAC CH2/CH4 AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                  -1 = at 1<z<2.5 but data not sufficient to classify on Ch2/Ch4 diagram
		 -99 = not at 1<z<2.5


Ch4_24mu           1 = at z>2.5 and in 24mu/Ch4 AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                   0 = at z>2.5 and not in 24mu/Ch4 AGN region of Messias/Bonato (S/N>2, or limits sufficient)
                  -1 = at z>2.5 but data not sufficient to classify on Ch2/Ch4 diagram
		 -99 = not at z>2.5


X-ray             Flag for classified as X-ray AGN in Duncan et al table (1=AGN; 0=SFG)

Opt_spec          Flag for classified as optical spectroscopic AGN in Duncan et al table (1=AGN; 0=SFG)

AGNfrac_af        AGN fraction from AGNfitter, calculated as L_tor / (L_tor + L_ga + L_SF)

AGNfrac_af_16     1-sigma lower limit on AGNfitter AGN fraction

AGNfrac_cg_s      AGN fraction output from CIGALE, using Skirtor AGN model

AGNfrac_cg_s_16   1-sigma lower limit on CIGALE Skirtor AGN fraction

AGNfrac_cg_f_s    AGN fraction output from CIGALE, using Fritz AGN model

AGNfrac_cg_f_16   1-sigma lower limit on CIGALE Fritz AGN fraction

Chi_sq_mpbp       Lower chi-squared value from Magphys and Bagpipes SED fits
                 
Chi_sq_afcg       Lowest chi-squared value from AGNfitter and CIGALE SED fits

AGN_final         Proposed final flag for whether this is a radiative (optical/IR/X-ray) AGN
                  1 = Radiative AGN
		  0 = Not radiative AGN
		 -1 = No robust classification possible

Mass_conc         Concensus mass from different SED fits  (log, in solar masses)

SFR_conc          Concensus star formation rate from different SED fits (log, in solar masses/yr)

Radio_excess      Excess radio emission, in dex, over the SFR-radio prediction (using ridgeline)

Radio_excess_DJS  Excess radio emission, in dex, over the SFR-radio prediction including mass dependence (from Smith et al 2020)

Extended_radio    Flag for whether the radio source shows clear >80kpc-size extended emission (1=yes)

RadioAGN_final    Proposed final flag for whether this is a radio-selected AGN
                  1 = Radio AGN
		  0 = Not radio AGN
                 -1 = No robust classification possible
