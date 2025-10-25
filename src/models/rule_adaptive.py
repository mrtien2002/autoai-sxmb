
import pandas as pd

def p_rule_row(r):
    s_bien = max(0.0, 1.2 - 0.03*float(r["bien_now"])) + 0.02*float(r["khan_len"])
    s_grp = {"MAX":0.25, "TRUNG":0.15, "MIN":0.05}.get(str(r["group"]), 0.05)
    s_pull = 0.4 * float(r["pull_down"])
    s_ref  = 0.5 * float(r["sim_reflect"])
    p = s_bien + s_grp + s_pull + s_ref
    return max(0.0, min(1.0, p))

def score_df(df_features: pd.DataFrame) -> pd.DataFrame:
    df = df_features.copy()
    df["p_rule"] = df.apply(p_rule_row, axis=1)
    return df
