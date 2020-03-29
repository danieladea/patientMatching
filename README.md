# patientMatching
## LA Hacks 2020 project to match different patient profiles

My partner Johnny and I found an interest in data science and analytics and wanted to explore that further during the hackathon. We were especially inspired to help in the healthcare industry during this pandemic. 

## Challenge
This is part of the Office Ally challenge at LA Hacks to create an algorithm that matches patient data from various sources to identify whether it is the same patient.
Prompt can be found at https://github.com/OfficeAllyGit/LAHack-2020

Analysis was done with jupyter notebook and pandas and different methods were tested including Levenshtein distances and semaphones. 
We found that using fuzzy matching through the fuzz library by SeatGeek was the best way to check if words were similar although misspelled. 

# Project Info
1) Team: Michael Scott Software Company
- Daniel Adea
- Johnny Urosevic
### Patient Matching Challenge
### Setup
Python3 is needed for this project
pip(3) install requirements.txt

### Steps
run python patientMatching.py 
the arguments are:
 "-w" to weigh missing columns less, allow profiles to be grouped even with a lot of missing information
"--threshold = <int>" default value 87
 "--csv = <str>" filename for csv to be tested against

### Contact:
To get in touch with the Michael Scott Software Company, please leave an email for me at dadea@ucla.edu









