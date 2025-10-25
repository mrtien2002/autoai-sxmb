# AutoAI SXMB – Rule‑Adaptive Core (Bootstrap)

Nền tảng **tự chạy** dự đoán SXMB dựa trên hệ **Biên** của anh.
- Đầu vào: `data/data_master.csv` (định dạng **DD/MM/YYYY**; 27 số/ngày, "00..99").
- Đầu ra: 
  - `exports/bang_bien.csv`
  - `exports/bien_table_40_AB.csv`
  - `exports/bang_diem_thang.csv` (chưa dùng trong bản tối giản)
  - `exports/predict_today_YYYYMMDD.csv`
  - `reports/daily_report_YYYYMMDD.txt`

Nếu **chưa có** `data_master.csv`, hệ sẽ **tự tạo dữ liệu giả lập 300 ngày** để chạy thử.

## Chạy nhanh (local)
```bash
pip install -r requirements.txt
python -m src.cli.run --pipeline full --topk 15
```
Kết quả ở thư mục `exports/` & `reports/`.

## Cấu trúc
```
autoai_sxmb_core/
├─ src/
│  ├─ dataops/ingest.py
│  ├─ analyses/analyze_bien.py
│  ├─ analyses/analyze_bien_table_40.py
│  ├─ features/builder.py
│  ├─ models/rule_adaptive.py
│  ├─ predict/predict_today.py
│  └─ cli/run.py
├─ data/data_master.csv
├─ exports/  # đầu ra
├─ reports/  # báo cáo TXT
├─ configs/app.json
└─ requirements.txt
```

## Ghi chú Biên
- **Biên 0 = ngày mới nhất (max(Ngay))** trong `data_master.csv`.
- `bang_bien.csv`: 
  - Hàng `n0` = số ngày tính từ lần về gần nhất (0 nếu về hôm nay).
  - Hàng `n1..n61` = khoảng cách không về giữa các lần về liên tiếp (ngược thời gian).
- `bien_table_40_AB.csv`: với mỗi ngày t và Biên b∈[0..40],
  - **B** = số lượng số có **biên đúng bằng b** tại ngày t.
  - **A** = số lượng số có **biên ≥ b** tại ngày t (đang còn “chưa về” ít nhất b ngày).
  → Ô lưu dạng `A_B`.

## Tùy chỉnh
- Định dạng ngày & múi giờ trong `configs/app.json` (mặc định DD/MM/YYYY, Asia/Bangkok).
- Số lượng gợi ý mỗi ngày: tham số `--topk` khi chạy `run.py`.
