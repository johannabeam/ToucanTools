import pandas as pd
import argparse

def generate_column_names(k_value):
    # Generate column names using list comprehension
    return [f'pop{i+1}' for i in range(k_value)]


def read_file(q_file_path, sample_file_path, k_value, output_file_path):
    q_file = pd.read_csv(q_file_path, sep="\\s+", names=generate_column_names(k_value))
    sample_file = pd.read_csv(sample_file_path)
    output_file = pd.concat([q_file, sample_file], axis=1)

    # Write the merged file to a new csv
    output_file.to_csv(output_file_path, index=False)
    print(f"Output saved to {output_file_path}")

def main():
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Take a Q matrix output from PCAngsd Admix and merge.")
    
    # Add command-line arguments
    parser.add_argument('-q', '--q_file', required=True, help="Path to the gzipped Beagle file")
    parser.add_argument('-s', '--sample_file', required=True, help="Path to the text file containing sample names (one per line), optional")
    parser.add_argument('-k', '--k_value',type=int, required=True, help="Input the number of k-values used for the analysis")
    parser.add_argument('-o', '--output_file', default='output.csv', help="Name of the output file (default: 'output.csv')")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    read_file(args.q_file, args.sample_file, args.k_value, args.output_file)


if __name__ == '__main__':
    main()
