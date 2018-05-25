#!/usr/bin/env python

import os

import gippy
from gips.parsers import GIPSParser
from gips.inventory import ProjectInventory
from gips.utils import Colors, VerboseOut, basename
from gips import utils

from pdb import set_trace


__version__ = '0.1.0'

def main():
    title = Colors.BOLD + 'GIPS Project Raster Splitter (v%s)' % __version__ + Colors.OFF

    parser = GIPSParser(datasources=False, description=title)
    parser.add_projdir_parser()
    
    group = parser.add_argument_group('splitting options')
    group.add_argument('--prodname', help='Pattern of the target images')

    #group.add_argument('--filemask', help='Mask all files with this static mask', default=None)
    #group.add_argument('--pmask', help='Mask files with this corresponding product', nargs='*', default=[])
    #h = 'Write mask to original image instead of creating new image'
    #group.add_argument('--original', help=h, default=False, action='store_true')
    #h = 'Overwrite existing files when creating new'
    #group.add_argument('--overwrite', help=h, default=False, action='store_true')
    #h = 'Suffix to apply to masked file (not compatible with --original)'
    #group.add_argument('--suffix', help=h, default='-masked')
    args = parser.parse_args()

    # TODO - check that at least 1 of filemask or pmask is supplied

    utils.gips_script_setup(None, args.stop_on_error)

    with utils.error_handler('Splitting error'):

        VerboseOut(title)
        for projdir in args.projdir:
    
            #if args.filemask is not None:
            #    mask_file = gippy.GeoImage(args.filemask)

            inv = ProjectInventory(projdir, args.products)
            for date in inv.dates:
                VerboseOut('Splitting files from %s' % date)
                
                #if args.filemask is None and args.pmask == []:
                #    available_masks = inv[date].masks()
                #else:
                #    available_masks = inv[date].masks(args.pmask)

                for p in inv.products(date):

                    VerboseOut(p)
                    
                    img = inv[date].open(p)
                    fname = img.Filename()

                    if not fname.endswith("{}.tif".format(args.prodname)):
                        continue
                    
                    bnames = img.BandNames()
                    
                    for i,bname in enumerate(bnames):

                        fnameout = "{}_{}.tif".format(
                            os.path.splitext(fname)[0], bname)

                        data = img[i].Read()
                        
                        imgout = gippy.GeoImage(fnameout, img, gippy.GDT_Int16, 1)
                        imgout.SetNoData(-32768)
                        imgout.SetOffset(0.0)
                        imgout.SetGain(0.0001)
                        imgout[0].Write(data)
                        imgout.SetBandName(bname, 1)
                        imgout = None
                        
                    img = None
    
                    #if args.filemask is not None:
                    #    img.AddMask(mask_file[0])
                    #    meta = basename(args.filemask) + ' '
                    #for mask in available_masks:
                    #    img.AddMask(inv[date].open(mask)[0])
                    #    meta = meta + basename(inv[date][mask]) + ' '
                    #if meta != '':
                    #    if args.original:
                    #        VerboseOut('  %s' % (img.Basename()), 2)
                    #        img.Process()
                    #        img.SetMeta('MASKS', meta)
                    #    else:
                    #        fout = os.path.splitext(img.Filename())[0] + args.suffix + '.tif'
                    #        if not os.path.exists(fout) or args.overwrite:
                    #            VerboseOut('  %s -> %s' % (img.Basename(), basename(fout)), 2)
                    #            imgout = img.Process(fout)
                    #            imgout.SetMeta('MASKS', meta)
                    #            imgout = None
                    #img = None
            #mask_file = None

    utils.gips_exit()


if __name__ == "__main__":
    main()

