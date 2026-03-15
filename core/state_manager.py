import json
from enum import Enum
from core.schemas import UserState, InvoiceData

# Enum for states to prevent typos
class AppState(str, Enum):
    NORMAL = "NORMAL"
    WAITING_FOR_INFO = "WAITING_FOR_INFO"
    WAITING_FOR_CONFIRM = "WAITING_FOR_CONFIRM"

class StateManager:
    def __init__(self, sheets_service):
        self.sheets = sheets_service
        
    def get_state(self, line_id: str) -> UserState:
        """Fetch user state from Sheets"""
        return self.sheets.get_user_state(line_id)
        
    def set_state(self, line_id: str, state: AppState, temp_data: dict = None):
        """Save user state to Sheets"""
        user_state = UserState(
            line_id=line_id,
            state=state.value,
            temp_data=json.dumps(temp_data, ensure_ascii=False) if temp_data else None
        )
        self.sheets.set_user_state(user_state)
        
    def clear_state(self, line_id: str):
        """Reset user state to NORMAL"""
        self.set_state(line_id, AppState.NORMAL, None)
        
    def get_temp_data(self, line_id: str) -> dict:
        """Parse temp JSON data from state"""
        state = self.get_state(line_id)
        if state.temp_data:
            try:
                return json.loads(state.temp_data)
            except json.JSONDecodeError:
                return {}
        return {}
