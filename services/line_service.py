from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    FlexMessage,
    FlexContainer,
)
from config import config

configuration = Configuration(access_token=config.LINE_CHANNEL_ACCESS_TOKEN)


class LineService:
    def __init__(self):
        self.api_client = ApiClient(configuration)
        self.messaging_api = MessagingApi(self.api_client)
        self.messaging_api_blob = MessagingApiBlob(self.api_client)

    def get_message_content(self, message_id: str) -> bytes:
        """Download image/content from LINE servers."""
        return self.messaging_api_blob.get_message_content(message_id)

    def reply_text(self, reply_token: str, text: str):
        request = ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=text)],
        )
        self.messaging_api.reply_message(request)

    def reply_flex(self, reply_token: str, alt_text: str, flex_dict: dict):
        flex_container = FlexContainer.from_dict(flex_dict)
        request = ReplyMessageRequest(
            reply_token=reply_token,
            messages=[FlexMessage(alt_text=alt_text, contents=flex_container)],
        )
        self.messaging_api.reply_message(request)

    def push_text(self, user_id: str, text: str):
        request = PushMessageRequest(
            to=user_id,
            messages=[TextMessage(text=text)],
        )
        self.messaging_api.push_message(request)

    def push_flex(self, user_id: str, alt_text: str, flex_dict: dict):
        flex_container = FlexContainer.from_dict(flex_dict)
        request = PushMessageRequest(
            to=user_id,
            messages=[FlexMessage(alt_text=alt_text, contents=flex_container)],
        )
        self.messaging_api.push_message(request)

    def build_confirmation_flex(self, data: dict) -> dict:
        """
        Build confirmation card for OCR + user-edited invoice data.
        """
        amount = data.get("amount") if data.get("amount") is not None else 0
        date = data.get("date") or "未填寫"
        items = data.get("items", [])
        invoice_type = data.get("invoice_type") or "未填寫"
        v_tax = data.get("vendor_tax_id") or "未填寫"
        b_tax = data.get("buyer_tax_id") or "未填寫"
        consumption_category = data.get("consumption_category") or "未分類"

        item_names = [str(it.get("name", "")).strip() for it in items if str(it.get("name", "")).strip()]
        if item_names:
            items_str = "\n".join([f"- {name}" for name in item_names])
        else:
            items_str = f"推測品項：{consumption_category}(推測品項)"

        flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "發票辨識結果",
                        "weight": "bold",
                        "color": "#1DB446",
                        "size": "sm",
                    },
                    {
                        "type": "text",
                        "text": f"${amount}",
                        "weight": "bold",
                        "size": "xxl",
                        "margin": "md",
                    },
                    {
                        "type": "separator",
                        "margin": "xxl",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "xxl",
                        "spacing": "sm",
                        "contents": [
                            self._create_flex_row("日期", date),
                            self._create_flex_row("類型", invoice_type),
                            self._create_flex_row("賣方統編", v_tax),
                            self._create_flex_row("買方統編", b_tax),
                            self._create_flex_row("消費品項", items_str, wrap=True),
                            self._create_flex_row("消費分類", consumption_category, wrap=True),
                        ],
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "確認並送出",
                            "text": "確認",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "修改內容",
                            "text": "修改",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "取消",
                            "text": "取消",
                        },
                    },
                ],
                "flex": 0,
            },
        }
        return flex

    def build_manual_record_flex(self, data: dict) -> dict:
        date = data.get("date") or "未填寫"
        receipt_type = data.get("receipt_type") or "無"
        item_name = (data.get("item_name") or "").strip() or "未填寫"
        category = data.get("category") or "日常開銷"
        amount = data.get("amount") if data.get("amount") is not None else 0

        flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "手動記帳確認",
                        "weight": "bold",
                        "size": "lg",
                    },
                    {
                        "type": "text",
                        "text": "請確認以下資料",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "md",
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            self._create_flex_row("日期", date),
                            self._create_flex_row("收據", receipt_type),
                            self._create_flex_row("消費品項", item_name, wrap=True),
                            self._create_flex_row("消費分類", category, wrap=True),
                            self._create_flex_row("總金額", f"${amount}"),
                        ],
                    },
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "確認並送出",
                            "text": "確認",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "修改內容",
                            "text": "修改",
                        },
                    },
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "取消",
                            "text": "取消",
                        },
                    },
                ],
                "flex": 0,
            },
        }
        return flex

    def _create_flex_row(self, label: str, value: str, wrap: bool = False) -> dict:
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0,
                    "wrap": wrap,
                },
                {
                    "type": "text",
                    "text": str(value),
                    "size": "sm",
                    "color": "#111111",
                    "align": "end",
                    "wrap": wrap,
                },
            ],
        }
