output = {}

# with open("春训一二.csv", "r") as f:
#     for line in f:
#         if line[-1] == "\n":
#             line = line[:-1]
#         if line.startswith("\ufeff"):
#             line = line[1:]
            
#         name, id, c1, c2 = line.split(",")
#         output[name] = [name, id, c1, c2, 0]

# with open("春训三.csv", "r") as f:
#     for line in f:
#         if line[-1] == "\n":
#             line = line[:-1]
#         if line.startswith("\ufeff"):
#             line = line[1:]
#         name, id = line.split(",")
        
#         if name not in output:
#             output[name] = [name, id, 0, 0, 1]
#         else:
#             output[name][4] = 1
        

output = {}
cnt = 1
unknown = {}
with open("春训一二三.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        name, id, c1, _, _, _ = line.split(",")
        if id == "ID" or id == "id":
            continue
        output[name] = [name, id, c1, 0, 0, 0]
with open("春训前9次.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, c2 = line.split(",")[:3]
        if id == "ID" or id == "id":
            continue
        if name == '':
            if id not in unknown:
                unknown[id] = f"未知{cnt}"
                cnt += 1
            name = unknown[id]
        if name in output:
            assert output[name][3] == 0
            output[name][3] = c2
        else:
            output[name] = [name, id, 0, c2, 0, 0]
            
with open("恢复性.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, c3 = line.split(",")[:3]
        if id == "ID" or id == "id":
            continue
        if name == '':
            if id not in unknown:
                unknown[id] = f"未知{cnt}"
                cnt += 1
            name = unknown[id]
        if name in output:
            assert output[name][4] == 0
            output[name][4] = c3
        else:
            output[name] = [name, id, 0, 0, c3, 0]
            
with open("海淀公园.csv", "r") as f:
    for line in f:
        if line[-1] == "\n":
            line = line[:-1]
        if line.startswith("\ufeff"):
            line = line[1:]
        id, name, c4 = line.split(",")[:3]
        if id == "ID" or id == "id":
            continue
        if name == '':
            if id not in unknown:
                unknown[id] = f"未知{cnt}"
                cnt += 1
            name = unknown[id]
        if name in output:
            assert output[name][5] == 0
            output[name][5] = c4
        else:
            output[name] = [name, id, 0, 0, 0, c4]
            
with open("output.csv", "w") as f:
    for name in output:
        f.write(f"{output[name][0]},{output[name][1]},{output[name][2]},{output[name][3]},{output[name][4]},{output[name][5]}\n")
        