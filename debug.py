def cOut(msg):
    import time
    clock = [str(time.localtime()[3]), str(time.localtime()[4]), str(time.localtime()[5])]

    for idx, i in enumerate(clock):
        clock[idx] = "0"*(2-len(i))+i if len(i) < 2 else i

    h, m, s = clock
    print("[{}:{}:{}] > {}".format(h, m, s, msg))

def end(text = "Press enter to exit."):
    input(text)
    return SystemExit

# Provide any string such as "-flag1 flag1_arg1 -flag2 -flag2_arg1 flag2_arg2"
# Provide how much args each flag takes as a dict {"flag1":1, "flag2":2}

# If there is a flag that demands an argument, it will take the next one in regardless of if it's got a "-" prefixing it.
# eg. flags -flag2 takes 2 additional args so it will take both "-flag2_arg1" and "flag2_arg2" as its args.

def flagParse(txt, acc_flags):
    output = {}
    demand = 0
    belongsto = None

    for i in txt.split(" "):
        if (i.replace("-", "", 1) in acc_flags) and demand == 0:
            demand = acc_flags[i.replace("-", "", 1)]  # get the demand of args for that flag
            output[i] = []
            belongsto = i  # mark any following ARGS as belonging to this flag

            # we don't wanna accept that one again
            del acc_flags[i.replace("-", "", 1)]

        else:
            # is arg
            if demand == 0:  # exceeds accepted args for the flag; no demand
                return Exception("Unexpected argument '{}'".format(i))

            else:
                # add it as an arg to the flag it belongs to
                output[belongsto].append(i)
                # fulfill the demand
                demand -= 1

    if demand > 0:  # if there is still demand
        return Exception("Not enough arguments supplied.")

    return output