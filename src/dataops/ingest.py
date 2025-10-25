
import pandas as pd
from pathlib import Path
import json

def load_config():
    cfg = json.loads(Path("configs/app.json").read_text(encoding="utf-8"))
    return cfg

def ensure_data_master():
    cfg = load_config()
    path = Path(cfg["paths"]["data_master"])
    if not path.exists():
        raise FileNotFoundError(f"Không thấy {path}. Hãy đặt data_master.csv đúng vị trí.")
    df = pd.read_csv(path, dtype=str)
    df["Ngay"] = pd.to_datetime(df["Ngay"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Ngay"]).sort_values("Ngay", ascending=False).reset_index(drop=True)
    def split_draws(x):
        parts = []
        for p in str(x).replace(" ", "").split(","):
            if p and p != "nan":
                parts.append(f"{int(p):02d}" if p.isdigit() else p)
        return parts
    df["Draws"] = df["KetQua"].apply(split_draws)
    # basic len check
    bad = df[~df["Draws"].apply(lambda lst: 20 <= len(lst) <= 35)]
    if len(bad) > 0:
        print(f"⚠️ Có {len(bad)} ngày có số lượng kết quả khác thường.")
    # persist canonical
    out = df[["Ngay","KetQua"]].copy()
    out["Ngay"] = out["Ngay"].dt.strftime("%d/%m/%Y")
    path.write_text(out.to_csv(index=False), encoding="utf-8")
    return df
