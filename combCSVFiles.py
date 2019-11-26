#merge text file in folder
#author MStöcker
import glob2

filenames = glob2.glob('*.csv')  # list of all .txt files in the directory


with open('outfile.csv', 'w') as f:
    for file in filenames:
        with open(file) as infile:
            f.write(infile.read()+'\n')



