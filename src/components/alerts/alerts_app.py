import streamlit as st
from src.commons.enums.type_message import TypeMessage

def get_alert_message(type_message: TypeMessage, msg:str):
    alert_msg = _alerts()
    return alert_msg[type_message](msg)
    
def _alerts()->any:
    messages= {TypeMessage.INFO: lambda msg: st.success(msg, icon="✅"), TypeMessage.WARNING: lambda msg: st.warning(msg, icon="⚠️"), TypeMessage.ERROR: lambda msg: st.error(msg, icon="🚨")}
    return messages