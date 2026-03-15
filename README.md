# SCUCT_AI LINE Bot

FastAPI + LINE Messaging API bot for:
- invoice image parsing (LLM)
- confirmation/edit/cancel card flow
- manual bookkeeping flow
- Google Sheets integration (Invoices, Subsidies, States, Log)

## Local Run
```powershell
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Deploy (Render)
This repo includes Render-ready files:
- render.yaml
- runtime.txt
- .env.example
- .gitignore

Set env vars in Render:
- LINE_CHANNEL_ACCESS_TOKEN
- LINE_CHANNEL_SECRET
- OPENAI_API_KEY
- GOOGLE_SHEET_ID
- GOOGLE_SERVICE_ACCOUNT_JSON
- BUYER_TAX_ID (default: 29902605)

Optional:
- PUBLIC_BASE_URL
- LIFF_ID
- GEMINI_API_KEY

## LINE Webhook
After deploy, set webhook URL in LINE Developers:
`https://<your-render-domain>/webhook`

## Note
Do not commit secrets (.env, API keys, service-account JSON).
