# FUNKY PARK
Function packer with stub for runtime unpacking in python

Instead of encrypting a payload and appending it to a benign file, this project looks at encrypting functions in the target binary; no claims are made on benefit to evasion. 
This is specifically for making reverse engineering of any function somewhat more difficult; designed for creating simple CTF challenges. 

## TODO
* Do both 32 and 64 bit ELFs
* Do relocations so binary does not have to be statically compiled
* Make a wrapper to deal with managing addresses (get rid of hardcoded variables)
