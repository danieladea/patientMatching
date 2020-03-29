# patientMatching
LA Hacks 2020 project to match different patient profiles

This is part of the Office Ally challenge at LA Hacks to create an algorithm which matches Patient data from various sources to identify whether it is the same patient.
Prompt can be found at https://github.com/OfficeAllyGit/LAHack-2020

Analysis was done with jupyter notebookand pandas and different methods were tested including Levenshtein distances and semaphones. 

We found that using fuzzy matching through the fuzz library by SeatGeek gave the best accuracies. 
