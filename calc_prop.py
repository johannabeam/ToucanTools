import gzip
import argparse

def calculate_proportions(beagle_file, sample_names_file, output_file):
    # Read the sample names from the provided text file or from the Beagle file header if no sample names are provided
    if sample_names_file:
        with open(sample_names_file, 'r') as sn_file:
            sample_names = [line.strip() for line in sn_file.readlines()]
    else:
        # If no sample names file is provided, extract from the Beagle file header
        with gzip.open(beagle_file, 'rt') as f:
            header_line = f.readline().strip()  # Read the first line (header)
            # Check that the header is well-formed (i.e., contains more than 3 columns)
            header_columns = header_line.split()
            if len(header_columns) < 4:
                raise ValueError("Header in Beagle file seems malformed or too short. Ensure the first line contains the marker and allele information, followed by sample genotypes.")
            # Since each sample has three columns, divide by 3 to get the number of samples
            num_samples = (len(header_columns) - 3) // 3
            sample_names = header_columns[3:3 + num_samples]  # Skip the first 3 columns (marker and allele) to get sample names

    # Initialize lists to store the counts for missing values for each individual
    counts_3333 = [0] * len(sample_names)

    # Open the gzipped Beagle file and process line by line
    with gzip.open(beagle_file, 'rt') as f:
        # Read each line (site)
        for line_num, line in enumerate(f, 1):
            # Split the line into columns (site data)
            values = line.strip().split()

            # Skip the first three columns (marker and allele columns)
            genotype_columns = values[3:]  # Start from the 4th column (index 3)

            # For each individual (3 columns per individual), check the genotype values
            for i in range(0, len(genotype_columns), 3):  # 3 columns per individual
                individual_idx = i // 3  # Calculate individual index (0-based)
                
                # Check if the genotype is .3333
                if genotype_columns[i] == "0.33333":
                    counts_3333[individual_idx] += 1  # Increment count for .3333

    # Calculate and print the proportion for each individual
    with open(output_file, 'w') as out_file:
        # We need to count the total number of sites (lines in the Beagle file)
        with gzip.open(beagle_file, 'rt') as f:
            total_sites = sum(1 for _ in f)  # Count lines in the gzipped file

        # Output the total sites and counts for each individual
        out_file.write(f"Total sites: {total_sites}\n\n")

        # Ensure the number of sample names matches the number of individuals
        if len(sample_names) != len(counts_3333):
            raise ValueError("The number of sample names does not match the number of individuals in the Beagle file.")

        # Output counts and proportions for each individual using their sample names
        for i in range(len(counts_3333)):
            sample_name = sample_names[i]  # Get the sample name for the current individual
            prop_3333 = counts_3333[i] / total_sites  # Proportion of missing for individual i
            

            # Write the proportions and counts for missing values
            out_file.write(f"Sample {sample_name}:\n")
            out_file.write(f"  .3333 count: {counts_3333[i]}  Proportion: {prop_3333:.4f}\n")

    print(f"Proportion calculation complete. Results saved in '{output_file}'.")


def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Calculate proportions of missing data for individuals in a Beagle file.")
    
    # Add command-line arguments
    parser.add_argument('-b', '--beagle_file', required=True, help="Path to the gzipped Beagle file")
    parser.add_argument('-s', '--sample_names', help="Path to the text file containing sample names (one per line), optional")
    parser.add_argument('-o', '--output_file', default='proportion_of_missing.txt', help="Name of the output file (default: 'proportion_of_missing.txt')")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    calculate_proportions(args.beagle_file, args.sample_names, args.output_file)


if __name__ == '__main__':
    main()
