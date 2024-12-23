if [ -f test ]; then
    rm test
fi
if [ -f original ]; then
    rm original
fi
as -msyntax=intel -mnaked-reg -o decrypt.o decrypt.asm
objcopy -O binary --only-section=.text decrypt.o decrypt.bin
gcc -no-pie -static -o test test.c
gcc -no-pie -static -o original test.c
python crypt.py

rm decrypt.o
rm decrypt.bin
