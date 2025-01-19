import argparse
import gzip
import shutil

def remove_samples(beagle_file, samples_to_remove_file, output_file):
    # Read the list of samples to remove
    with open(samples_to_remove_file, 'r') as f:
        samples_to_remove = set(line.strip() for line in f.readlines())

    # Open the input Beagle file and the output (gzipped) file
    with gzip.open(beagle_file, 'rb') as f, gzip.open(output_file, 'wb') as out:
        # Read the header
        header = f.readline().decode('utf-8').strip().split('\t')
        
        # Identify the sample columns (3 columns per individual)
        sample_columns = []
        for i in range(3, len(header), 3):  # Starting from the 4th column (index 3)
            sample_name = header[i]
            sample_columns.append((sample_name, i))
        
        # Filter out samples to remove from the header
        filtered_header = header[:3]  # Keep the first three columns (marker, allele1, allele2)
        for sample_name, idx in sample_columns:
            if sample_name not in samples_to_remove:
                filtered_header.extend([header[idx], header[idx+1], header[idx+2]])

        # Write the filtered header to the output gzipped file
        out.write("\t".join(filtered_header).encode('utf-8') + b"\n")

        # Process the remaining lines of the Beagle file
        for line in f:
            columns = line.decode('utf-8').strip().split('\t')
            filtered_columns = columns[:3]  # Keep the first three columns (marker, allele1, allele2)
            for sample_name, idx in sample_columns:
                if sample_name not in samples_to_remove:
                    filtered_columns.extend([columns[idx], columns[idx+1], columns[idx+2]])
            out.write("\t".join(filtered_columns).encode('utf-8') + b"\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Remove specified samples from a Beagle file.")
    parser.add_argument('-b', '--beagle_file', required=True, help="Path to the Beagle file.")
    parser.add_argument('-s', '--samples_to_remove_file', required=True, help="Path to the file containing sample names to remove.")
    parser.add_argument('-o', '--output_file', required=True, help="Path to the output Beagle file (gzipped).")
    
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Call the function to remove the samples
    temp_output = args.output_file + ".tmp"  # Temporary output file
    remove_samples(args.beagle_file, args.samples_to_remove_file, temp_output)
    
    # Replace the original Beagle file with the modified file
    shutil.move(temp_output, args.output_file)
    print(f"Successfully modified the Beagle file: {args.output_file}")

if __name__ == "__main__":
    main()
