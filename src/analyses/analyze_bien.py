
import pandas as pd
import numpy as np
from pathlib import Path
import json

def load_config():
    return json.loads(Path("configs/app.json").read_text(encoding="utf-8"))

def _current_bien_table(df):
    # df newest→oldest
    numbers = [f"{i:02d}" for i in range(100)]
    draws = df["Draws"].tolist()
    # positions per number
    pos = {num: [] for num in numbers}
    for idx, lst in enumerate(draws):
        for x in lst:
            if x in pos: pos[x].append(idx)  # 0=newest
    header = ["Bien"] + numbers
    data = []
    # n0
    row0 = ["n0"]
    for num in numbers:
        occ = pos[num]
        if len(occ)==0:
            row0.append("")
        else:
            row0.append(int(occ[0]))
    data.append(row0)
    # n1..n61
    for r in range(1,62):
        row = [f"n{r}"]
        for num in numbers:
            occ = pos[num]
            if len(occ) >= r+0:
                if r-1 < len(occ)-1:
                    gap = occ[r] - occ[r-1] - 1
                    row.append(int(gap))
                else:
                    row.append("")
            else:
                row.append("")
        data.append(row)
    return pd.DataFrame(data, columns=header)

def build_bang_bien():
    from src.dataops.ingest import ensure_data_master
    cfg = load_config()
    df = ensure_data_master()
    table = _current_bien_table(df)
    outpath = Path(cfg["paths"]["exports"])/"bang_bien.csv"
    outpath.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(outpath, index=False, encoding="utf-8")
    print(f"✅ Đã ghi {outpath}")
