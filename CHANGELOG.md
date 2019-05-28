# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [UNRELEASED]


## v0.14.6
### Fixed
- fixed less common use-case with NameError

## v0.14.5
### Fixed
- was passing str, instead of list-of-str, to landsat's `_cache_if_vsicurl`
### Added
- retry scheme for deletion of temp directories
### Changed
- utils code was using print instead of verbose_out

## v0.14.4
### Fixed
- fixed bug in mosaicking code where scene is missing a product

## v0.14.3
### Fixed
- another case of not using gcs backoff downloader.

## v0.14.2
### Fixed
- fixed bug from unstaging coreg testing tweaks.

## v0.14.1
### Fixed
- (#641) gips not using gcs downloader for coreg imagery
- (notix) gips coreg search skipping s2 search on same day

## v0.14.0
### Added
- mask out Landsat C1 edge effect isues (E-W edge and SLC-off)

### Changed
- use RedEdge4 as NIR band for index computations -- it is
  more similar to LC8's NIR.

## v0.13.0
### Added
- add support to fetch MODIS MCD43A4 from AWS S3
- HLS driver
- python-acolite support

### Changed
- Upgraded license

### Fixed
- GCS API conformance

## v0.12.0
### Added
- added DOI badge to README.md
- preliminary SRTM driver
- initial version of google cloud based assets

### Changed
- migrated CHANGES.txt to CHANGELOG.md
- squelched out https `InsecureRequestWarning`s for CDL, and added
  `urllib3[secure]` to stop same warning in Sentinel-2

### Fixed
- Landsat coregistration #572
- Various items in Sentinel-2's ACOLITE processing:
    - Fix #506 by always keying off band 1 for resolution.
    - Fix #548/#437, wastefully processing entire datastrips, by using acolite's
      limit config/param
    - Fix #438, off-by-one errors in tile selection, by shrinking the limit
      down to avoid overlap (thanks MGRS!).

## v0.11.0
- Documentation (README) improved
- aod-6.1
- file system race conditions in directory creation addresseed (Thanks for
  finding that AWS)
- MODIS MCD12Q1 to collection 006
- `cloudmask` products for s2 and landsat inverted (1=cloud, 0=nodata)
- Provenance improved (add "SOURCE_ASSET" and always add metadata, not subtract)

## v0.10.0
- modis using gippy.algorithms.Indices
- changed system tests to use gdalinfo based comparator
- added Sentinel2 MTCI and S2REP products
- CDL fetch enabled
- copious amounts of tempdir usage to prevent bad data pollution
- MODIS updated to use Collection 6 (where avalable  some products lag)
- integrated AROP for coregistration of Landsat to Sentinel-2 grid.
- Gridded exports use integral mask to define spatial extent and resolution of
  exports (CLI `-r rastermask`)
- added support for pulling Landsat from AWS S3 storage.
- `gips_stats` now has CSV formatting and is tweakable via settings.
- drivers can pass arguments out to the CLI (`--pclouds N` allows filtering
  based on MSIL1C and Landsat C1 metadata)
- system tests now include `-m lite` for running small subset of system tests
- Docker files for use with .gitlab-ci.yml
- gips_project deprecated and functionality moved to gips_export script.
- MOD08_D3 shutdown their FTP..moved to https
- System tests now use artifact store, instead of fetching repeatedly.

## v0.9.2
- PR#448 from Applied-GeoSolutions/445-get-geometry
- PR#440 from Applied-GeoSolutions/433-sentinel2-gain
- PR#447 from Applied-GeoSolutions/444-install
- PR#434 from Applied-GeoSolutions/428-sentinel2-cloud-filter
- PR#435 from Applied-GeoSolutions/landsat-cloud-cover-filter
- PR#431 from Applied-GeoSolutions/landsat-coreg-product
- PR#422 from Applied-GeoSolutions/388-spatialextent-from-raster
- PR#421 from Applied-GeoSolutions/chirps-goes-global
- PR#411 from Applied-GeoSolutions/fix-gips-config-env-bug
- PR#410 from Applied-GeoSolutions/85-silly-bugs
- PR#408 from Applied-GeoSolutions/366-aot550
- PR#406 from Applied-GeoSolutions/palsar-mask-fix
- drink versioning DRY
- added "mask" product; updated implicit "sign" masking
- PR#402 from Applied-GeoSolutions/113-numprocs-toplevel
- proposed fix for IEEE_UNDERFLOW_FLAG and DENORMAL issues

## v0.9.1
- Optional database inventory using the Django ORM, currently used for
  managing metadata for products and assets.
- Sentinel-2 support
- Landsat Collection 1 support
- ACOLITE atmospheric correction support
- Palsar2 support
- tempdir context managers to prevent data corruption
- Switched to MODIS Collection 6 (for AOD as well)
- Improved NASS CDL driver
- Switched to regular expressions for asset pattern specification.
- Reusable EarthData authentication for drivers

## v0.8.4
- ndvi8 re-enabled
- cleaned up all gippy HDF subdataset(sds) images (appear to be a limited number of
  SDS handles in gdal1.x).

## v0.8.2
- landsat assets now tagged as 'DN' and 'SR' for USGS downloaded surface
  reflectance.
- added landsat 'bqashadow' product that uses `gippy.algorithms.AddShadowMask`
  to catch shadows of BQA detected clouds via shadow smear.
- enabled `--sensors` filter for landsat.
- fixed: `gips.tiles.Tiles.pprint` TypeError when `colors` is None

## v0.8.1
- added support for `alltouch` paramter in CookieCutter (gippy==0.3.6)

## v0.8.0
- Indvidual data utilities deprecated (e.g., landsat), replaced with gips_ scripts
- New gips scripts, each with more specific functionatlity: gips_inventory, gips_warptiles, gips_process
- Refactor of core inventory and tiles for streamlined code reuse
- Requirements (python libraries) can be specified for each data module
- Interpolation option added to project function (neartest neighbor, bilinear, or cubic)
- Setup now puts settings.py at /etc/gips/settings.py
- Ability to loop through all features in a vector layer (using the --loop option)
- where argument added to include SQL where clauses
- Setup no-longer puts settings.py in /etc/gips/
- Configuration managed through gips_config command
- Fixed bug in handling date specification

Landsat
- Added wtemp product (Water temperature, atm corrected with MODTRAN using custom profiles from MERRA data)

MODIS
- fixed bug in MODIS temperature making them unable to be used in project (multiple identical output band names)
- addition of obstime product (observation time for MCD derived products)

CDL
- Updated CDL directory structure to use standard GIPS format (tiledir/datedir)
- added tiles.shp to repository

MERRA
- Updated merra data module

AOD
- updated to be in-line with new gips.utils.settings framework


## v0.7.1
- Better internal handling of sensors for data where there can be multiple sensors on a single day
- Tile projects (no shapefile or nomosaic set) now creates subdirectories for each tile in project folder
- Project inventories (gips_project inventory) doesn't fail if directory has extraneous files
- datadir option added back allowing saving of files into specified directory

New functionality
- 'gips_project stack' for creating stacks of products in a GIPS project directory
- added mapreduce utilities for multiprocessing
- added 'nomosaic' option to project, which will keep the data as tiles (but still warp)

AOD
- fixed retrieval of Aerosol Optical Depth from MOD08 data

LANDSAT
- products added: dn (digital numbers), volref (volumetric reflectance of water)
- Files read directly from tar.gz (rather than extracting) using GDAL's virtual filesystem

MODIS
- fixed segfault in indices and cleaned up extraneous printing
- fixed nodata value in ndvi8 product

## v0.7.0
- Refactoring of inventory classes and printing
- Renaming of products to replace underscores (_) with dashes (-) in the product name
- Addition of gips_project script (print inventory, create browse images)
- Changed naming convention of project directories to shapefile_resolution_datasetname
- misc fixes/improvements to argument parsing and verbose output
- refactored argument parsing of products, now use -p switch rather than individual product switches
- added 'products' sub-command to get listing of available products
- fixed creation of mosaics without warping

landsat:
- fixed bug with TOA indices generating wrong values

AOD:
- throw error if unable to retrieve AOD estimate

SARannual
- fixed bug when processing product for multiple tiles and asset doesn't exist for some tiles

MODIS
- Refactored code and implemented product naming convention

## v0.6.8
- added Algorithm base class and updated scripts to utilize Algorithm class
- additional algorithm scripts added (gips_tclass, gips_truth, gips_mask)

landsat:
- fixed check of negative reflectances (was converted to NoData)
- fixed bug where AOD was not calculating long term average if data not available

## v0.6.7
- changed library name to GIPS
- added algorithms module back to main GIPS
- bumped GIPPY dependency to 0.9.7

landsat:
- added tassled cap transformation
- reflectance not allowed to be negative (capped at 0)


## v0.6.6
- removed masking feature from 'project' command (replaced with gip_mask)
- changed file naming for project files.  Directory named with shape or tileid and resolution, files named  date_sensor_product
- added gip.py script for general purpose processing on project data directories
- project: metadata properly copied from data
- metadata added to all processed files
- bumped version of GIPPY dependency to 0.9.6

landsat changes:
- exception handling when calling atmospheric model
- added NDWI and MSAVI2 indices to products
