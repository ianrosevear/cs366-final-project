import sys
with open(sys.argv[1], "r") as fin, open(sys.argv[2], "w") as fout:
    for line in fin:
##         l = line.split("\t")
##         if "/c/en" in l[0]:
##             out = ""
##             rels = l[0][4:-1].split(",")
##             for r in rels:
##                 out = out + r + "\t"
##             out = out[0:-1]
##             out = out + "\t" + l[4]
##             fout.write(out)
        l = line.split("\t")
        if "/c/en" in l[1] and "/c/en" in l[2]:
            fout.write(line)
