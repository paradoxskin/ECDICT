import stardict
import os
import time

base = os.path.dirname(__file__)
sql = f"{base}/out.sql"
ffr = "/tmp/stardict.r.fifo"
ffw = "/tmp/stardict.w.fifo"

def init():
    print(f"{base}/out.sql")
    if not os.path.exists(f"{base}/stardict.csv"):
        input("please unzip stardict.7z ;7za x ?; [enter to continue]")
    stardict.convert_dict(sql, f"{base}/stardict.csv")

def main():
    # init
    # - data
    if not os.path.exists(sql):
        init()
    dt = stardict.StarDict(sql)
    def query_once(idx):
        once = dt.query(idx)
        return f"=> {once['word']}\n{once['translation']}"
    # - fifo in
    if os.path.exists(ffr):
        os.remove(ffr)
    os.mkfifo(ffr)
    # - fifo out
    if os.path.exists(ffw):
        os.remove(ffw)
    os.mkfifo(ffw)
    # main loop
    while True:
        with open(ffr, "r") as fdr:
            line = fdr.readline()
            line = line.replace("\n", "")
        if not line:
            continue
        mat = dt.match(line)
        res = ""
        if mat:
            if mat[0][1] == line:
                res = query_once(mat[0][0])
            else:
                tmpl = []
                for i in range(3):
                    tmpl.append(query_once(mat[i][0]))
                res = "\n;\n".join(tmpl)
                del tmpl
        else:
            res = "not found"
        with open("history", "a+") as hist:
            hist.write(line+"\n")
        with open(ffw, "w") as out:
            out.write(res+"\n")

if __name__ == "__main__":
    main()
