# ---------------------------------------------
# Dispatching rules
# ---------------------------------------------
def priority(policy, job, now, machine_state):
    if policy == "FIFO":
        return job["arrive_t"]
    if policy == "SPT":
        return job["proc_time"]
    if policy == "EDD":
        return job["due"] - now
    if policy == "BOTTLENECK":
        # approximate: favor operations at the busiest machine (lower queue length -> lower priority number)
        qlen = machine_state.get(job["op_machine"], 0)
        return (qlen+1) * job["proc_time"]
    raise ValueError("Unknown policy")
