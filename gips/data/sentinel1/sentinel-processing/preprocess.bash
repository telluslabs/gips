#!/bin/bash
# enable next line for debugging purpose
# set -x 

############################################
# User Configuration
############################################
# start counting time
start=`date +%s`
starttime=`date "+%Y-%m-%d %H:%M:%S"`
echo "Starttime is ${starttime}"
# adapt this path to your needs
gptPath="/usr/bin/gpt"

############################################
# Command line handling
############################################

# first parameter is a path to the graph xml
graphXmlPath="/sentinel-processing/graphs/${GRAPH}.xml"

# use third parameter for path to source products
sourceDirectory="/data"

# use fourth parameter for path to target products
targetDirectory="/output"

# the fifth parameter is a file prefix for the target product name, typically indicating the type of processing
targetFilePrefix="processed"

   
############################################
# Helper functions
############################################
removeExtension() {
    file="$1"
    echo "$(echo "$file" | sed -r 's/\.[^\.]*$//')"
}


############################################
# Main processing
############################################

# Create the target directory
mkdir -p "${targetDirectory}"

# the d option limits the elemeents to loop over to directories. Remove it, if you want to use files.
for F in $(ls -1d "${sourceDirectory}"/S1*.zip); do
  sourceFile="$(realpath "$F")"
  targetFile="${targetDirectory}/${targetFilePrefix}_$(removeExtension "$(basename ${F})").tif"
  echo ${sourceFile}
  echo ${targetFile}
  ${gptPath} ${graphXmlPath} -e -PtargetProduct=${targetFile} -SsourceProduct=${sourceFile} -Dsnap.dataio.bigtiff.compression.type=LZW
done

end=`date +%s`
endtime=`date "+%Y-%m-%d %H:%M:%S"`
echo "Endtime is ${endtime}"
runtime=$((end-start))
echo "Runtime is ${runtime} seconds"
