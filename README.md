# interview

## introduction
the repository shall contain the answer for the home assignment given regarding the eBPF Linux subsystem

## the question definition
* Create an eBPF program
* eBPF program should use Cilium/bcc frameworks
* eBPF program should be able to probe, using kprobes for both sys_read and sys_write
kernel functions.
* The expected result:

Every time a call to sys_read and sys_write on the Linux machine it runs on, the
eBPF program will print “hello sys_read/sys_write was called”

* Please provide the eBPF as well as the user plan code
* Please provide instructions for installation/running it.
Optional/Advantage
* Be able to pass configuration information from the user plan code to the eBPF program.
* Be able to pass some information from the eBPF program to the user plan code.

## relevant Links
* https://ebpf.io/labs/
* https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html

## repository contents
```
├── commands.txt
├── README.md
├── run_instructions.txt
└── us_code.py
```
* `commands.txt` - a text helper file to list some commands learnt in the tutorial
* `README.md` - this text file
* `run_instructions.txt` - a text helper file that contains the instructions and prerequisists needed to run the program
* `us_code.py` - the program file to be run using python

## implementation notes
* I decided to use python as the user-space code base due to it's relativly low ramp-up time
* the C code for the BPF program is embedded within the main source code as text
* I am passing the operation (read or write) within the data structure passed to the user-space code
* I have yet to implement a configuration passing between the user-space code to the BPF program due to lack of time
* I have decided to ignore ops from the root user as my system is quite noisy and there are many concurrent operations
