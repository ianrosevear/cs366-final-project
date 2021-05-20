import sys
with open(sys.argv[1], "r") as fin, open(sys.argv[2], "w") as fout:
    for line in fin:
        outline = "\"" + line.split(",")[0].rstrip("\n") + "\",\n"
        fout.write(outline)
