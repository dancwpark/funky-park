import struct

import elftools.elf.sections
from elftools.elf.elffile import ELFFile


def encrypt(key, plain):
    # not efficient
    lendiff = len(plain) - len(key)
    if lendiff > len(key):
        key *= len(plain) // len(key)
    key = key[0 : len(plain)]
    return bytes([a ^ b for a, b in zip(key, plain)])


def main():
    # filename is the target binary name, currently hardcoded
    filename = "test2"
    print("Procesing file:", filename)
    with open(filename, "r+b") as f:
        elffile = ELFFile(f)

        # find symbol table
        for sect in elffile.iter_sections():
            # print(sect.name)
            if sect.name == ".symtab":
                symbol_table = sect
                break

        # function_name is the function that will be edited to
        # trampoline to the encrypted blob
        # currently hardcoded
        function_name = "add"
        for symbol in symbol_table.iter_symbols():
            if symbol.name == "_init":
                print(f"Found init at 0x{symbol.entry['st_value']:x}")
            if symbol.name == function_name:
                function_addr = symbol.entry["st_value"]
                function_size = symbol.entry["st_size"]
                print(f"address: 0x{function_addr:x}")
                print(f"size: {function_size} bytes")
                break

        # read in the function
        # offset is also hardcoded
        # f.seek(function_addr - 0x400000)
        f.seek(function_addr)
        fbytes = f.read(function_size)

        print(f"Bytes read")
        print(fbytes.hex())

        # This is a toy problem - so using a simple xor
        # key = b'\xde\xad\xbe\xef'
        key = b"A"
        new = encrypt(key, fbytes)
        print(new.hex())

        # We have encrypted function
        # f.seek(function_addr - 0x400000)
        f.seek(function_addr)
        f.write(new)


if __name__ == "__main__":
    main()
