Title: Riddle Generation


How to use: Almost everything needed to run the program is located in the Generator folder. In addition to the files provided, a list of every ConceptNet edge needs to be included in this folder, which can be downloaded here: https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz. To generate riddles for a desired startword, modify the startword_list at the top of riddle_generator.py to include any number of nouns to be used as answers for riddles. This will generate a file of several candidate riddles for each word. Then run selection.py with the output file as an argument to get its choice of a single best riddle for each word.


Folders and descriptions


Generator: The files needed to run the program
riddle_functions.py
riddle_generator.py
Neural_net.py
selection.py
TESTING_CLEAN.csv
TRAINING_CLEAN.csv

Old: Development versions of the program that are now not used. 
test-error-handling.py
conceptnet-test.py


Useful Scripts and Word Lists: Word lists (the top 1000 nouns, and these nouns split into train and test sets), formatters to use these lists in our program, and a frequency count program for ConceptNet used in development to determine which riddle forms to pursue. 
nouns.txt:
train_set.txt
test_set.txt
formatter.py
formatter2.py
most-common-nouns-english.csv
frequency_count.py

Outputs and Analysis: Raw outputs from different versions of our program, as well as a script to determine a Pearson correlation coefficient from our ratings. Ratings for past versions of our program are in old_ratings.xlsv, and ratings for the current version of our program are in ratings.xlsv
riddle_outputs folder
pearson_score.py
ratings.xlsx
old_ratings.xlsx

Diagrams: Two images to help conceptualize how our riddle generator works, and to understand the node names used in our code. 
Node_map.png
riddle_form.png

