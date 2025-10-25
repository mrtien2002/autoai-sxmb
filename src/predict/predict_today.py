
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

from src.features.builder import build_features_today
from src.models.rule_adaptive import score_df

def load_config():
    return json.loads(Path("configs/app.json").read_text(encoding="utf-8"))

def predict_today(topk: int = 15):
    cfg = load_config()
    df_feat = build_features_today()
    df_scored = score_df(df_feat)
    df_scored = df_scored.sort_values("p_rule", ascending=False).reset_index(drop=True)
    today_str = datetime.now().strftime("%Y%m%d")
    out_csv = Path(cfg["paths"]["exports"]) / f"predict_today_{today_str}.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df_scored.to_csv(out_csv, index=False, encoding="utf-8")

    # write text report
    top = df_scored.head(topk)
    lines = []
    lines.append(f"🧠 AUTOAI SXMB – Gợi ý {topk} số | Ngày: {datetime.now().strftime('%d/%m/%Y')}")
    lines.append("number  p_rule  bien  group  khan_len  month_pts")
    for _, r in top.iterrows():
        lines.append(f"{r['number']:>5}  {r['p_rule']:.3f}   {int(r['bien_now']):>3}   {r['group']:^5}    {int(r['khan_len']):>3}        {int(r['month_points'])}")
    out_txt = Path(cfg["paths"]["reports"]) / f"daily_report_{today_str}.txt"
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    Path(out_txt).write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ Đã ghi {out_csv}")
    print(f"📝 Báo cáo: {out_txt}")

if __name__ == "__main__":
    predict_today(topk=15)
