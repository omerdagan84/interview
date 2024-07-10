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
