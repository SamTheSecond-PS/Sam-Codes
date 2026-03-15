import orjson as rj # type: ignore

stdd = [
    {"name":"CHAD", "score":100},
    {"name":"Sam", "score":99},
    {"name":"steve", "score":99}
]

with open("stdd.json", "wb") as f:
    f.write(rj.dumps(stdd, option=rj.OPT_INDENT_2)) 

with open("stdd.json", "rb") as f:
    dat = rj.loads(f.read())
    top = dat[0]["score"] if dat[0]["score"] > 80 else 0
    top2= dat[1]["score"] if dat[1]["score"] > 80 else 0
    top3 = dat[2]["score"] if dat[2]["score"] > 80 else 0
    maxx = max(top, top3, top2)
    print(maxx)
