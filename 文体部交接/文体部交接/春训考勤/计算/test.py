output = {}
cnt = 1
unknown = {}
with open("总考勤.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, *c = line.split(",")
        if id == "ID" or id == "id":
            continue
        output[name] = [id, name, *c] + ['0'] * 4
        
with open("春训一二三.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        name, id, *c = line.split(",")
        if id == "ID" or id == "id":
            continue
        if name not in output:
            output[name] = [id, name] + ['0']*12 + c
        else:
            output[name] = output[name][:14] + c
            
with open("output.csv", "w") as f:
    f.write("\ufeff")
    for name in output:
        f.write(f"{','.join(output[name])}\n")
        