#!/bin/bash
#SBATCH --job-name=find_file_weekly
#SBATCH --output=find_file_weekly_%A.out
#SBATCH --error=find_file_weekly_%A.err
#SBATCH --time=7-00:00:00

sleep $(( 7 * 24 * 60 * 60 ))  # Sleep for 7 days
/usr/bin/python /path/to/find_file.py

