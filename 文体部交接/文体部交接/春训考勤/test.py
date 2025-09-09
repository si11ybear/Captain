output = {}
cnt = 1
unknown = {}
with open("晚训考勤.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, c1, c2 = line.split(",")
        if id == "ID" or id == "id":
            continue
        if name == '':
            name = f"未知{cnt}"
            cnt+=1
        if name in output:
            print(name)
            assert 0
        output[name] = [id, name, c1, c2, 0]
        
with open("海淀公园.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, c3 = line.split(",")[:3]
        if id == "ID" or id == "id":
            continue
        if name not in output:
            output[name] = [id, name, 0, 0, c3]
        else:
            output[name][4] = c3
            
with open("output.csv", "w") as f:
    for name in output:
        f.write(f"{output[name][0]},{output[name][1]},{output[name][2]},{output[name][3]},{output[name][4]}\n")
        