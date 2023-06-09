#!/bin/bash

echo '#######################################################################'
echo '#                             Building docs                           #'
echo '#######################################################################'

export SPHINXOPTS="-W"  # Treat warnings as errors

xvfb-run make --directory $PROJECT_DIR/docs html

DOCS_STATUS=$?
if [[ ("$DOCS_STATUS" == 0) ]]; then
  echo '#######################################################################'
  echo '#                            Build succeded                           #'
  echo '#######################################################################'
  exit 0
else
  echo ''
  echo '#######################################################################'
  echo '#                            Build failed    !                        #'
  echo '#######################################################################'
  exit 1
fi
