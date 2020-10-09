#! /bin/bash

echo "Cleaning up images"
find . -maxdepth 2 -wholename "*MHz/images" | xargs rm -rf
echo "Cleaning up MS/MMS"
find . -maxdepth 2 -wholename "*MHz/*.mms"  | xargs rm -rf
find . -maxdepth 2 -wholename "*MHz/*.mms.flagversions"  | xargs rm -rf
find . -maxdepth 2 -wholename "*MHz/*.data" | xargs rm -rf
find . -maxdepth 2 -wholename "*MHz/*.ms.flagversions"  | xargs rm -rf
find . -maxdepth 2 -wholename "*MHz/*.ms"  | xargs rm -rf
echo "Cleaning up temporary files"
find . -maxdepth 2 -wholename "*MHz/Temp*"  | xargs rm -rf
find . -maxdepth 2 -wholename "*MHz/tmp*"  | xargs rm -rf
echo "Cleaning up cube vis and images"
find . -maxdepth 2 -wholename "*/cubes/vis"  | xargs rm -rf
find . -maxdepth 2 -wholename "*cubes/images*"  | xargs rm -rf
