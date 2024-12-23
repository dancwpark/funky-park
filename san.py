# Input and output file paths
input_file = "libc_raw_func.txt"  # Replace with your input file name
output_file = "output.txt"  # Replace with your desired output file name

# Process the file
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        first_part = line.strip()
        if '@' in line:
            first_part = line.split("@")[0].strip()
        # Write to the output file
        outfile.write(first_part + "\n")

print(f"Processed lines have been written to {output_file}.")

