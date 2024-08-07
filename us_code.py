#!/usr/bin/python
# This source is derived from https://github.com/iovisor/bcc/blob/master/examples/tracing/hello_perf_output.py
# the file is modified by Omer Dagan <omerdagan84@gmail.com>

from bcc import BPF
from bcc.utils import printb

# create the BPF program to run in the kernel space
bpf_prog = """
#include <linux/sched.h>

// the data_t struct will be used to transfer information from the kernel space to user-space
struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    char op[6];
};

// define and name the output channel
BPF_PERF_OUTPUT(event_buffer);

// define the function to be linked to the kprobe for write operation
int op_write(struct pt_regs *ctx) {
    // create the data structure
    struct data_t data = {};

    // ignore calls to root processes
     if (bpf_get_current_uid_gid() == 0) {
        return 0;
    }
    // get pid tgid data
    data.pid = bpf_get_current_pid_tgid();
    // get kernel time
    data.ts = bpf_ktime_get_ns();
    // get process name
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    // set the OP (read/write)
    char write_op[] = "write";
    bpf_probe_read_str(&data.op, sizeof(data.op), write_op);

    // submit the data structur to the output channel for the User-space to read
    event_buffer.perf_submit(ctx, &data, sizeof(data));

    return 0;
}

// define the function to be linked to the kprobe for read operation
int op_read(struct pt_regs *ctx) {
    // create the data structure
    struct data_t data = {};

    // ignore calls to root processes
     if (bpf_get_current_uid_gid() == 0) {
        return 0;
    }
    // get pid tgid data
    data.pid = bpf_get_current_pid_tgid();
    // get kernel time
    data.ts = bpf_ktime_get_ns();
    // get process name
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    // set the OP (read/write)
    char read_op[] = "read";
    bpf_probe_read_str(&data.op, sizeof(data.op), read_op);

    // submit the data structur to the output channel for the User-space to read
    event_buffer.perf_submit(ctx, &data, sizeof(data));

    return 0;
}
"""

# load the BPF program to the kernel
bpf_obj = BPF(text=bpf_prog)

# attach the program to the kprobe
bpf_obj.attach_kprobe(event=bpf_obj.get_syscall_fnname("write"), fn_name="op_write")
bpf_obj.attach_kprobe(event=bpf_obj.get_syscall_fnname("read"), fn_name="op_read")

# print out the header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))

# print the event
start = 0
def print_event(cpu, data, size):
    global start
    event = bpf_obj["event_buffer"].event(data)
    if start == 0:
            start = event.ts
    time_s = (float(event.ts - start)) / 1000000000
    if event.op.decode('utf-8') == "write":
        printb(b"%-18.9f %-16s %-6d %s" % (time_s, event.comm, event.pid,
                                           b"hello sys_write was called"))
    elif event.op.decode('utf-8') == "read":
        printb(b"%-18.9f %-16s %-6d %s" % (time_s, event.comm, event.pid,
                                           b"hello sys_read was called"))

# loop with callback to print_event
bpf_obj["event_buffer"].open_perf_buffer(print_event)
while 1:
    try:
        bpf_obj.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
