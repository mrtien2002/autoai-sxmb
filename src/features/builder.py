
import pandas as pd
import numpy as np
from pathlib import Path
import json

def load_config():
    return json.loads(Path("configs/app.json").read_text(encoding="utf-8"))

def _parse_ab_row_to_vector(rec, max_b=6):
    v = []
    for b in range(0, max_b+1):
        A,B = rec[f"Bien_{b}"].split("_")
        v.extend([float(A), float(B)])
    return np.array(v, dtype=float)

def reflect_similarity_today(df_ab, lookback=30):
    def cos(a,b):
        na = np.linalg.norm(a); nb = np.linalg.norm(b)
        return 0.0 if na==0 or nb==0 else float(np.dot(a,b)/(na*nb))
    if len(df_ab) < 2:
        return 0.0
    v_today = _parse_ab_row_to_vector(df_ab.iloc[0])
    sims = []
    for i in range(1, min(lookback, len(df_ab))):
        v_past = _parse_ab_row_to_vector(df_ab.iloc[i])
        sims.append(cos(v_today, v_past))
    return float(np.max(sims)) if sims else 0.0

def month_group_for_number(df_master, num_str):
    m0 = df_master.iloc[0]["Ngay"].month
    df_mon = df_master[df_master["Ngay"].dt.month == m0]
    cnt = sum(1 for lst in df_mon["KetQua"].str.split(",") if num_str in [x.strip() for x in lst])
    if cnt >= 9: return "MAX", cnt
    if cnt >= 5: return "TRUNG", cnt
    return "MIN", cnt

def build_features_today():
    cfg = load_config()
    path_master = Path(cfg["paths"]["data_master"])
    path_ab = Path(cfg["paths"]["exports"])/"bien_table_40_AB.csv"
    if not path_ab.exists():
        raise FileNotFoundError("Thiếu bien_table_40_AB.csv. Hãy chạy bước AB trước.")
    df_ab = pd.read_csv(path_ab, dtype=str)
    df_ab["Ngay"] = pd.to_datetime(df_ab["Ngay"], format="%d/%m/%Y", dayfirst=True)
    df_ab = df_ab.sort_values("Ngay", ascending=False).reset_index(drop=True)
    sim = reflect_similarity_today(df_ab, lookback=30)
    # master
    dfm = pd.read_csv(path_master, dtype=str)
    dfm["Ngay"] = pd.to_datetime(dfm["Ngay"], format="%d/%m/%Y", dayfirst=True)
    dfm = dfm.sort_values("Ngay", ascending=False).reset_index(drop=True)
    numbers = [f"{i:02d}" for i in range(100)]
    # compute bien_now per number relative to newest day
    bien_now = {}
    for num in numbers:
        b = None
        for k in range(len(dfm)):
            lst = dfm.iloc[k]["KetQua"].replace(" ","").split(",")
            if num in lst:
                b = k
                break
        if b is None: b = 41
        bien_now[num] = min(b, 40)
    # simple pull_down proxy from AB row 1 stats
    rec0 = df_ab.iloc[0]
    A1, B1 = map(float, rec0["Bien_1"].split("_"))
    pull_down = 0.0 if A1==0 else min(1.0, B1 / A1)
    # build rows
    rows = []
    for num in numbers:
        group, month_pts = month_group_for_number(dfm, num)
        rows.append({
            "number": num,
            "bien_now": int(bien_now[num]),
            "khan_len": int(bien_now[num]),
            "group": group,
            "month_points": int(month_pts),
            "sim_reflect": float(sim),
            "pull_down": float(pull_down),
        })
    return pd.DataFrame(rows)
