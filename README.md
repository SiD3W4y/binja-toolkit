# binja-toolkit
This repository contains scripts I use for CTF challenges or personal 
projects.

## Pointer search
Tool made at first for kernel challenges. It can load \*.map symbol files
to recover symbols. Its purpose is to find pointers in rw sections pointing
to code or writable data.

![Pointer search](images/pointer_search.png)

## GBA Utils
Loads GBA roms. It can additionally load code coverage traces from
[this](https://github.com/SiD3W4y/mgba) fork and provide reports for
hits by function or hits by basic block.

![GBA Coverage](images/gba.png)
