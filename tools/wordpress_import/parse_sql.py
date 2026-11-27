"""Parse INSERT statements from a phpMyAdmin MySQL dump into JSON rows."""
import json
import re
import sys

ESC = {"0": "\0", "n": "\n", "r": "\r", "t": "\t", "Z": "\x1a", "b": "\b"}


def parse_values(s, i):
    """Parse '(..),(..);' starting at index i. Yields lists of values."""
    n = len(s)
    while i < n:
        while i < n and s[i] in " \n\r\t,":
            i += 1
        if i >= n or s[i] == ";":
            return
        assert s[i] == "(", s[i:i + 50]
        i += 1
        row = []
        while True:
            while s[i] in " \n\r\t":
                i += 1
            c = s[i]
            if c == "'":
                i += 1
                buf = []
                while True:
                    c = s[i]
                    if c == "\\":
                        nx = s[i + 1]
                        buf.append(ESC.get(nx, nx))
                        i += 2
                    elif c == "'":
                        if i + 1 < n and s[i + 1] == "'":
                            buf.append("'")
                            i += 2
                        else:
                            i += 1
                            break
                    else:
                        j = i
                        while s[j] not in "\\'":
                            j += 1
                        buf.append(s[i:j])
                        i = j
                row.append("".join(buf))
            else:
                j = i
                while s[j] not in ",)":
                    j += 1
                tok = s[i:j].strip()
                row.append(None if tok == "NULL" else tok)
                i = j
            while s[i] in " \n\r\t":
                i += 1
            if s[i] == ",":
                i += 1
                continue
            if s[i] == ")":
                i += 1
                break
        yield row


def extract(path, tables):
    data = open(path, encoding="utf-8", errors="replace").read()
    out = {t: [] for t in tables}
    pat = re.compile(r"INSERT INTO `(\w+)` \(([^)]*)\) VALUES\s*")
    for m in pat.finditer(data):
        t = m.group(1)
        if t not in out:
            continue
        cols = [c.strip(" `") for c in m.group(2).split(",")]
        for row in parse_values(data, m.end()):
            out[t].append(dict(zip(cols, row)))
    return out


if __name__ == "__main__":
    path, outpath, *tables = sys.argv[1:]
    res = extract(path, tables)
    json.dump(res, open(outpath, "w"), ensure_ascii=False)
    for t, rows in res.items():
        print(t, len(rows))
