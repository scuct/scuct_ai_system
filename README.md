# SCUCT_AI LINE Bot

這個專案是 FastAPI + LINE Messaging API 的機器人，主要功能：
- 發票圖片辨識（OCR + LLM 抽欄位）
- 卡片確認、修改、取消
- 手動記帳模式（輸入 `記帳` 後用 LLM 解析文字成欄位）
- 寫入 Google Sheets（Invoices / Subsidies / States / Log）

## 1. GitHub Ready 檔案
已提供：
- `render.yaml`：Render Blueprint 設定
- `.env.example`：環境變數範本
- `.gitignore`：忽略敏感資訊與暫存

## 2. 本機啟動
```powershell
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

健康檢查：
- `GET /` 應回 `{"status":"ok", ...}`

## 3. 上傳到 GitHub
```powershell
git init
git add .
git commit -m "prepare render deployment"
git branch -M main
git remote add origin <你的 GitHub repo URL>
git push -u origin main
```

## 4. Render 部署（推薦）
1. 到 Render 建立帳號並連接 GitHub
2. 選擇 `New +` -> `Blueprint`
3. 選你的 repo（Render 會讀 `render.yaml`）
4. 建立服務後，填入環境變數（見下一節）

### 必填環境變數
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`
- `OPENAI_API_KEY`
- `GOOGLE_SHEET_ID`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `BUYER_TAX_ID`（預設 `29902605`）

### 可選
- `PUBLIC_BASE_URL`
- `LIFF_ID`
- `GEMINI_API_KEY`

## 5. GOOGLE_SERVICE_ACCOUNT_JSON 設定方式
把 service account JSON 壓成一行字串後貼到 Render。

範例（PowerShell）：
```powershell
python -c "import json, pathlib; p=pathlib.Path('service_account.json'); print(json.dumps(json.loads(p.read_text(encoding='utf-8')), ensure_ascii=False))"
```

把輸出整段貼到 `GOOGLE_SERVICE_ACCOUNT_JSON`。

## 6. LINE Developers 設定
部署成功後會有 Render 網址，例如：
- `https://your-app.onrender.com`

在 LINE Developers -> Messaging API：
- Webhook URL 設成 `https://your-app.onrender.com/webhook`
- 開啟 `Use webhook`
- 按 `Verify`

## 7. 上線後快速驗證
1. 傳一張發票圖給 Bot
2. 應先收到「已接收到照片，正在處理中」
3. 再收到辨識確認卡
4. 按 `確認` 後資料進 Google Sheets
5. 傳 `記帳`，輸入自然語句（例如：`今天社課開銷 320 收據`）
6. 收到手動記帳確認卡，按 `確認` 成功寫入

## 8. 注意事項
- 不要把 `.env`、金鑰、Google 憑證提交到 GitHub
- 免費 Render 方案可能休眠，Webhook 延遲會增加
- 若收不到訊息，先檢查 Render logs 與 LINE Webhook Verify
