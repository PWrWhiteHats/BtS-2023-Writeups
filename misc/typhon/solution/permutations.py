import zipfile
import sys
import os
import itertools

# get the name of the ZIP file from the command line argument
if len(sys.argv) < 2:
    print('Please specify the name of the ZIP file.')
    sys.exit()

zip_filename = sys.argv[1]

# open the ZIP file
with zipfile.ZipFile(zip_filename, 'r') as zip_file:
    # open "words.txt" file for writing
    with open('words.txt', 'w') as words_file:
        # display the file names inside the archive
        for info in zip_file.infolist():
            # extract the filename from the path and write it to "words.txt" if it's not empty
            filename = os.path.basename(info.filename)
            if filename and filename != '!   cGVybXV0NSxuby1kdXBs':
                words_file.write(filename + '\n')

# open the input file for reading
with open('words.txt', 'r') as input_file:
    # read all lines as individual words
    words = [line.strip() for line in input_file.readlines()]

# create permutations of 5 without repetitions
permutations = itertools.permutations(words, 5)

# open the output file for writing
with open('dictionary.txt', 'w') as output_file:
    # write each combination as a separate line
    for permutation in permutations:
        output_file.write(''.join(permutation) + '\n')
