
import argparse
from src.dataops.ingest import ensure_data_master
from src.analyses.analyze_bien import build_bang_bien
from src.analyses.analyze_bien_table_40 import build_bien_table_40_ab
from src.predict.predict_today import predict_today

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pipeline", choices=["full","light"], default="full")
    ap.add_argument("--topk", type=int, default=15)
    args = ap.parse_args()

    ensure_data_master()
    build_bang_bien()
    build_bien_table_40_ab()
    if args.pipeline == "full":
        predict_today(topk=args.topk)

if __name__ == "__main__":
    main()
