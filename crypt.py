from elftools.elf.elffile import ELFFile
import elftools.elf.sections
import struct


def encrypt(key, plain):
    # not efficient
    lendiff = len(plain) - len(key)
    if lendiff > len(key):
        key *= len(plain) // len(key)
    key = key[0:len(plain)]
    return bytes([a ^ b for a, b in zip(key, plain)])


def main():
    filename = "test"
    print("Procesing file:", filename)
    with open(filename, 'r+b') as f:
        elffile = ELFFile(f)

        # find symbol table
        for sect in elffile.iter_sections():
            #print(sect.name)
            if sect.name == '.symtab':
                symbol_table = sect
                break
        
        function_name = 'add'
        for symbol in symbol_table.iter_symbols():
            if symbol.name == function_name:
                function_addr = symbol.entry['st_value']
                function_size = symbol.entry['st_size']
                print(f"address: 0x{function_addr:x}")
                print(f"size: {function_size} bytes")
                break

        # read in the function
        f.seek(function_addr-0x400000)
        fbytes = f.read(function_size)

        print(f"Bytes read")
        print(fbytes.hex())

        # This is a toy problem - so using a simple xor
        #key = b'\xde\xad\xbe\xef'
        key = b'A'
        new = encrypt(key, fbytes)
        print(new.hex())

        # We have encrypted function
        f.seek(function_addr-0x400000)
        f.write(new)


        ## Load in the decrypter to .note
        ## Modify ELF header to point to the decrypter stub
        ## adjust offsets and sizes if needed
        stub_path = 'decrypt.bin'
        with open(stub_path, 'rb') as sf:
            stub = sf.read()
        f.seek(0, 2)
        new_section_offset = (f.tell() + 0xFFF) & ~0xFFF
        f.seek(new_section_offset)
        f.write(stub)
        #new_section_offset = f.tell()
        new_section_size = len(stub)
        print(hex(new_section_offset))

        base_addr = None
        for segment in elffile.iter_segments():
            if segment['p_type'] == 'PT_LOAD' and (segment['p_flags'] & 0x1):
                base_addr = segment['p_vaddr'] - segment['p_offset']
                break
        if base_addr is None:
            print('error')

        new_section_addr = base_addr + new_section_offset

        new_phdr = struct.pack(
                'IIQQQQQQ',
                1,
                5,
                new_section_offset,
                new_section_addr,
                new_section_addr,
                new_section_size,
                new_section_size,
                0x1000)

        e_phoff = elffile.header['e_phoff']
        e_phnum = elffile.header['e_phnum']
        e_phentsize = elffile.header['e_phentsize']

        f.seek(e_phoff + e_phnum * e_phentsize)
        f.write(new_phdr)

        f.seek(56)
        f.write(struct.pack("<H", e_phnum + 1))
        f.seek(24)
        f.write(struct.pack("<Q", new_section_addr))
        #f.seek(0)
        #f.write(elffile.stream.getvalue())

    with open(filename, "r+b") as f:
        elffile = ELFFile(f)

        ph_offset = elffile.header['e_phoff']
        ph_entsize = elffile.header['e_phentsize']
        ph_num = elffile.header['e_phnum']

        text_segment_index = None
        for i, segment in enumerate(elffile.iter_segments()):
            if segment['p_type'] == 'PT_LOAD' and segment['p_flags'] & 0x1:
                text_segment_index = i
                break
        if text_segment_index is None:
            print("error")

        target_phdr_offset = ph_offset + text_segment_index * ph_entsize

        # Read the current program header
        f.seek(target_phdr_offset)
        phdr_data = f.read(ph_entsize)

        # Parse the program header
        p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack(
            '<IIQQQQQQ', phdr_data
        )

        # Update the p_flags to include PF_W (0x2 for writable)
        new_p_flags = p_flags | 0x2  # Add writable flag
        print(f"New p_flags: {bin(new_p_flags)}")

        # Pack the modified program header
        new_phdr_data = struct.pack(
            '<IIQQQQQQ',
            p_type,
            new_p_flags,  # Updated flags
            p_offset,
            p_vaddr,
            p_paddr,
            p_filesz,
            p_memsz,
            p_align
        )

        # Write the modified program header back to the file
        f.seek(target_phdr_offset)
        f.write(new_phdr_data)


if __name__ == '__main__':
    main()
