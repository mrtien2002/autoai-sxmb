
import pandas as pd
from pathlib import Path
import json

def load_config():
    return json.loads(Path("configs/app.json").read_text(encoding="utf-8"))

def _bien_value_on_day(df, day_idx, num):
    # distance from day_idx to the previous occurrence (including day_idx)
    draws = df["Draws"].tolist()
    for k in range(0, min(300, len(draws)-day_idx)):
        idx = day_idx + k
        if idx >= len(draws): break
        if num in draws[idx]:
            return k
    return 41

def build_bien_table_40_ab():
    from src.dataops.ingest import ensure_data_master
    cfg = load_config()
    df = ensure_data_master()
    numbers = [f"{i:02d}" for i in range(100)]
    rows = []
    for day_idx, row in df.iterrows():
        bien_vals = {}
        for num in numbers:
            b = _bien_value_on_day(df, day_idx, num)
            bien_vals[num] = min(b, 40)
        rec = {"Ngay": row["Ngay"].strftime("%d/%m/%Y")}
        # B_b = count==b; A_b = count>=b
        for b in range(0,41):
            B = sum(1 for v in bien_vals.values() if v==b)
            A = sum(1 for v in bien_vals.values() if v>=b)
            rec[f"Bien_{b}"] = f"{A}_{B}"
        rows.append(rec)
    out = pd.DataFrame(rows)
    outpath = Path(cfg["paths"]["exports"])/"bien_table_40_AB.csv"
    out.to_csv(outpath, index=False, encoding="utf-8")
    print(f"✅ Đã ghi {outpath}")
