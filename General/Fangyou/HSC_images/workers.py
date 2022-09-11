import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import simple_norm
import photutils
import time
import statmorph
import scipy.ndimage as ndi
from astropy.convolution import convolve
from astropy.table import Table
from astropy.table import Column
from astropy.stats import SigmaClip
from photutils.background import Background2D, MedianBackground
from photutils.segmentation import SourceCatalog

gain = 3

# Generating psf
size = 20  # on each side from the center
sigma_psf = 3.7 #FWHM KiDS is 0.77 arcsec
y, x = np.mgrid[-size:size+1, -size:size+1]
psf = np.exp(-(x**2 + y**2)/(2.0*sigma_psf**2))
psf /= np.sum(psf)


directory = './downloaded_data/'

def worker(name):
    try:
        fits_input = fits.open(directory+name)
        #fits_input.info()
        data=fits_input[1].data
        hdr=fits_input[1].header

        # Background estimator
        sigma_clip = SigmaClip(sigma=3.)
        bkg_estimator = MedianBackground()
        bkg = Background2D(data, (25,25), filter_size=(3,3),
                        sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

        # Subtracting background
        data = data-bkg.background

        # Creating segmentation map
        threshold = photutils.detect_threshold(data, 1.5)
        npixels = 5
        segm = photutils.detect_sources(data, threshold, npixels)

        # Making a tabel
        cat = SourceCatalog(data, segm)
        tbl = cat.to_table()

        # Finding central centroid
        x, y = tbl['xcentroid'], tbl['ycentroid']
        new_tbl = tbl[(x<40.)&(x>20.) & (y>20.)&(y<40.)]

        # If multiple, pick the biggest centroid
        index = np.argmax(new_tbl['area'])
        label = new_tbl['label'][index]
        segmap = segm.data == label
        
        # Smoothing the segmap
        segmap_float = ndi.uniform_filter(np.float64(segmap), size=10)
        segmap = segmap_float > 0.5

        #     except:
        #         print('I skip this galaxy: ', name, '\n')
        #         continue

        #     try:
        source_morphs = statmorph.source_morphology(
            data, segmap.astype(int), gain=gain,psf=psf)


        morph = source_morphs[0]
        new_row = [name, morph.xc_centroid, morph.yc_centroid, morph.ellipticity_centroid, morph.elongation_centroid,
               morph.orientation_centroid, morph.xc_asymmetry, morph.yc_asymmetry, morph.ellipticity_asymmetry, 
               morph.elongation_asymmetry, morph.orientation_asymmetry, morph.r20,morph.r50,morph.r80,
               morph.rhalf_circ, morph.rhalf_ellip, morph.rmax_circ, morph.rmax_ellip, morph.rpetro_circ,
               morph.rpetro_ellip, morph.concentration, morph.asymmetry, morph.smoothness, morph.m20, morph.gini,
               morph.gini_m20_bulge, morph.gini_m20_merger, morph.deviation, morph.shape_asymmetry, 
               morph.outer_asymmetry, morph.multimode, morph.sn_per_pixel, morph.flux_circ, morph.flux_ellip,
               morph.intensity, morph.sersic_xc, morph.sersic_yc, morph.sersic_amplitude, morph.sersic_ellip,
               morph.sersic_n, morph.sersic_rhalf, morph.sersic_theta, morph.sky_mean, morph.sky_median, 
               morph.sky_sigma, morph.nx_stamp, morph.ny_stamp, morph.xmax_stamp, morph.xmin_stamp,
               morph.ymax_stamp, morph.ymin_stamp, morph.flag, morph.flag_sersic
              ]
        return new_row
    except:
        return f'Problem with {name}'