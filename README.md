# ToucanTools
Some (kind of) clunky tools that help filter beagle files. 

# Calc_prop.py: Calculate missingness per individual from beagle file
A lil python script to compile missingness per individual for beagle files output from angsd.

Ever wanted to calculate how much missing data you have in your genotype likelihood files? Now you can!
There are three arguments: 

`-b` supply your beagle file (gzipped; **required**) 

`-s` supply _optional_ sample names file, where the file is a simple txt with one sample name per line 

`-o` where you can _optionally_ change the name of the output txt file with your missing data values 

Note that missing data proportions are calculated based on the genotype likelihoods of 0.33333 for each "allele" per individual, not based on absense of genotype likelihood data (such as a 0 or a '.' ).

Use as you like.


# Remove_indivs.py
Another lil python script to remove individuals from a beagle file.

`-b` to input the beagle file.

`-s` to input the text file that has one sample per line.

`-o` to name the output of the finished beagle file. Probably should gzip it so that angsd/pcangsd can read it.


# read_q.py
Python script to read in a q matrix from pcangsd and then add columns for your sample names and coordinates if you want to. Currently the sample names file is required.
`-q` to input your Q matrix from PCAngsd

`-s` to input a sample csv that has however many columns you want. Can have sample names, coordinates, etc.

`-k` tell the k-value of the Q matrix. This will automatically populate the correct headers for the number of k's you used

`-o` write your output file name. Should be something.csv.
