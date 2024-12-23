# Main file
import argparse
from elftools.elf.elffile import ELFFile
import elftools.elf.sections
import os
import subprocess

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--binary', 
            help='ELF binary to pack', required=True)
    args = parser.parse_args()
    return args

def print_text_functions(binary):
    command = [
        "objdump", "-t", binary,
        "|", "grep", ".text",
        "|", "awk", "'{print $6}'"
    ]
    command = " ".join(command)
    result = subprocess.run(command, shell=True,
            capture_output=True, text=True)
    result = result.stdout.strip().splitlines()
    result = [a.strip().strip('_') for a in result]
    counter = 0
    with open('libc_functions.txt', 'r') as f:
        libc_funcs = f.readlines()
        libc_funcs = [a.strip() for a in libc_funcs]
        for line in result:
            if line == '.hidden':
                continue
            if line in libc_funcs:
                continue
            print(line)
            counter += 1
    print(counter)



def main():
    args = parse_args()
    binary_file = args.binary

    if not os.path.isfile(binary_file):
        raise FileNotFoundError('Input binary does not exist')

    # Check if binary was statically compiled (hacky)
    # TODO: make this less hacky
    result = subprocess.run(['file', binary_file], 
            capture_output=True, text=True)
    if not ('statically' in str(result)):
        raise Exception('Input binary was not statically compiled')

    # Options
    print("Options")
    print_text_functions(binary_file)
    # 1. Pack entire .text section
    # 2. Pack specific function
    


if __name__ == '__main__':
    main()
