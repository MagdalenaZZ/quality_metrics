# quality_metrics

Small repo to go to a google drive, search for a file named samples.txt updated the last week. If quality falls below 5% for either sample  collection site, email the site with a warning,and a list of the failed samples. 

Test files:
empty.txt
samples.txt

Conda install for the environment needed
environment.yml

Scripts:
find_file.py - script to identify new input

parse_and_email.py - script to process new input, and send emails

run_find_file_weekly.sh - batch script to run script find_file.py weekly

To get started, do:
sbatch run_find_file_weekly.sh

Then once each week the script find_file.py will look for new files, and download them. If there is a new file, it will use the script parse_and_email.py to look for low-quality data

For interacting with the Google API, to find files and download them, the files credentials.json and token.json are needed. You have to create those yourself from the Google Developer Console



