def cOut(msg):
    import time
    clock = [str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]

    for idx, i in enumerate(clock):
        clock[idx] = "0"*(2-len(i))+i if len(i) < 2 else i

    h, m, s = clock
    print("[{}:{}:{}] > {}".format(h, m, s, msg))