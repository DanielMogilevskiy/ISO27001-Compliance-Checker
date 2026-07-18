import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.checker import load_controls, compute_score
from src.models import ComplianceStatus

# Настройка страницы
st.set_page_config(
    page_title="ISO 27001 Compliance Checker",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 ISO 27001 Compliance Assessment")
st.markdown("### Interactive compliance checker for Annex A controls")

# Загрузка контролов
@st.cache_data
def get_controls():
    return load_controls("data/iso27001_controls.csv")

controls = get_controls()

# Инициализация состояния
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "completed" not in st.session_state:
    st.session_state.completed = False

# Прогресс
total = len(controls)
answered = len(st.session_state.answers)
progress = answered / total

st.progress(progress)
st.write(f"Progress: {answered}/{total} controls answered")

# Основной интерфейс
if not st.session_state.completed and answered < total:
    idx = st.session_state.current_index
    ctrl = controls[idx]
    
    with st.container():
        st.markdown(f"### Control {idx+1}/{total}")
        st.markdown(f"**ID:** `{ctrl.id}`")
        st.markdown(f"**Name:** {ctrl.name}")
        st.markdown(f"**Category:** {ctrl.category}")
        st.markdown(f"**Description:** {ctrl.description}")
        
        status = st.radio(
            "Implementation status:",
            options=[
                "1 - Implemented",
                "2 - Partially Implemented",
                "3 - Not Implemented",
                "4 - Not Applicable"
            ],
            key=f"status_{idx}",
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏮ Previous", disabled=idx == 0):
                st.session_state.current_index -= 1
                st.rerun()
        with col2:
            if st.button("⏭ Next"):
                st.session_state.answers[ctrl.id] = status[0]  # 1, 2, 3, 4
                if idx + 1 < total:
                    st.session_state.current_index += 1
                else:
                    st.session_state.completed = True
                st.rerun()

# Финишный отчёт
else:
    st.balloons()
    st.success("✅ Assessment completed!")
    
    # Применяем статусы к контролам
    for ctrl in controls:
        if ctrl.id in st.session_state.answers:
            answer = st.session_state.answers[ctrl.id]
            mapping = {
                "1": ComplianceStatus.IMPLEMENTED,
                "2": ComplianceStatus.PARTIAL,
                "3": ComplianceStatus.NOT_IMPLEMENTED,
                "4": ComplianceStatus.NOT_APPLICABLE
            }
            ctrl.status = mapping[answer]
    
    # Считаем результаты
    scores = compute_score(controls)
    
    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Compliance", f"{scores['overall_pct']:.1f}%")
    with col2:
        st.metric("Implemented", scores['implemented'])
    with col3:
        st.metric("Partial", scores['partial'])
    with col4:
        st.metric("Not Implemented", scores['not_implemented'])
    
    # График по категориям
    st.subheader("📊 Compliance by Category")
    cat_df = pd.DataFrame({
        "Category": list(scores['category_scores'].keys()),
        "Compliance %": list(scores['category_scores'].values())
    }).sort_values("Compliance %", ascending=False)
    
    fig = px.bar(
        cat_df,
        x="Compliance %",
        y="Category",
        orientation="h",
        color="Compliance %",
        color_continuous_scale="RdYlGn",
        title="Category Compliance Scores",
        text_auto=True
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Таблица с проблемными контролами
    missing = [c for c in controls if c.status in (ComplianceStatus.NOT_IMPLEMENTED, ComplianceStatus.PARTIAL)]
    if missing:
        st.subheader("⛔ Controls Needing Attention")
        missing_data = []
        for c in missing:
            missing_data.append({
                "ID": c.id,
                "Category": c.category,
                "Name": c.name,
                "Status": c.status.value
            })
        st.dataframe(pd.DataFrame(missing_data), use_container_width=True)
    
    # Кнопка для повторного прохождения
    if st.button("🔄 Start Over"):
        st.session_state.clear()
        st.rerun()