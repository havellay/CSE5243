#! /bin/sh
#
# This file launches the Python script that will launch our feature vector 
# creation script. The script will take to a 'pdb' terminal from where all
# data members of the script can be examined

# Parser.py contains main() and launches all other scripts
# dataset is contained with the source


export PYTHONPATH="/home/4/ruan/local/lib/python2.6/site-packages"
export NLTK_DATA="/home/4/ruan/nltk_data"

cd vector
`which python` Parser.py
