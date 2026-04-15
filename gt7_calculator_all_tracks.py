import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="GT7 Калькулятор", layout="wide")

# ============================================
# ЗАГРУЗКА БАЗЫ МАШИН
# ============================================

def load_car_database():
    if os.path.exists("gt7_cars_database.json"):
        with open("gt7_cars_database.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CAR_DATABASE = load_car_database()
CAR_NAMES = sorted(list(CAR_DATABASE.keys())) if CAR_DATABASE else ["Нет данных"]

# ============================================
# ТРАССЫ
# ============================================

TRACKS = [
    "🏁 Autodromo Nazionale Monza",
    "🌲 Nürburgring Nordschleife",
    "🗻 Suzuka Circuit",
    "🏎️ Spa-Francorchamps",
    "🌊 Circuit de la Sarthe (Le Mans)",
    "🏙️ Tokyo Expressway",
    "⛰️ Deep Forest Raceway",
    "🏔️ Trial Mountain Circuit",
    "🇯🇵 Fuji International Speedway",
    "🇺🇸 WeatherTech Raceway Laguna Seca",
]

# ============================================
# ИНДИВИДУАЛЬНЫЕ НАСТРОЙКИ ДЛЯ МАШИНЫ+ТРАССЫ
# ============================================

def get_custom_tune(car_name, track_name):
    """Возвращает индивидуальные настройки для машины на конкретной трассе"""
    
    car_data = CAR_DATABASE.get(car_name, {})
    drive_type = car_data.get('drive_type', 'FR')
    power = car_data.get('power', 500)
    weight = car_data.get('weight', 1400)
    
    # Базовые настройки в зависимости от типа привода
    if drive_type == "RR":  # Porsche
        base = {
            'height_f': 70, 'height_r': 75,
            'spring_f': 4.8, 'spring_r': 5.2,
            'arb_f': 6, 'arb_r': 5,
            'comp_f': 32, 'comp_r': 34,
            'ext_f': 42, 'ext_r': 44,
            'camber_f': -2.2, 'camber_r': -1.6,
            'toe_f': 0.12, 'toe_r': 0.18,
            'brake_balance': -3,
        }
    elif drive_type == "MR":  # Ferrari, McLaren
        base = {
            'height_f': 68, 'height_r': 72,
            'spring_f': 4.6, 'spring_r': 5.0,
            'arb_f': 5, 'arb_r': 6,
            'comp_f': 30, 'comp_r': 32,
            'ext_f': 40, 'ext_r': 42,
            'camber_f': -2.0, 'camber_r': -1.4,
            'toe_f': 0.10, 'toe_r': 0.20,
            'brake_balance': -2,
        }
    elif drive_type == "4WD":  # Nissan, Audi
        base = {
            'height_f': 72, 'height_r': 77,
            'spring_f': 4.2, 'spring_r': 4.5,
            'arb_f': 5, 'arb_r': 5,
            'comp_f': 28, 'comp_r': 30,
            'ext_f': 38, 'ext_r': 40,
            'camber_f': -1.8, 'camber_r': -1.3,
            'toe_f': 0.05, 'toe_r': 0.15,
            'brake_balance': -1,
        }
    else:  # FR
        base = {
            'height_f': 75, 'height_r': 80,
            'spring_f': 4.5, 'spring_r': 4.8,
            'arb_f': 5, 'arb_r': 5,
            'comp_f': 30, 'comp_r': 32,
            'ext_f': 40, 'ext_r': 42,
            'camber_f': -2.0, 'camber_r': -1.5,
            'toe_f': 0.10, 'toe_r': 0.20,
            'brake_balance': -2,
        }
    
    # Корректировка под трассу
    if "Monza" in track_name:
        return {
            **base,
            'height_f': base['height_f'] - 5, 'height_r': base['height_r'] - 5,
            'downforce_f': 140, 'downforce_r': 280,
            'max_speed': 330, 'final_gear': 3.60,
            'lsd_init_f': 12, 'lsd_init_r': 18,
            'lsd_accel_f': 20, 'lsd_accel_r': 30,
            'lsd_brake_f': 14, 'lsd_brake_r': 20,
        }
    elif "Nordschleife" in track_name:
        return {
            **base,
            'height_f': base['height_f'] + 5, 'height_r': base['height_r'] + 5,
            'downforce_f': 220, 'downforce_r': 420,
            'max_speed': 280, 'final_gear': 4.20,
            'lsd_init_f': 10, 'lsd_init_r': 15,
            'lsd_accel_f': 18, 'lsd_accel_r': 25,
            'lsd_brake_f': 12, 'lsd_brake_r': 18,
        }
    elif "Suzuka" in track_name:
        return {
            **base,
            'downforce_f': 200, 'downforce_r': 380,
            'max_speed': 290, 'final_gear': 4.00,
            'lsd_init_f': 11, 'lsd_init_r': 16,
            'lsd_accel_f': 19, 'lsd_accel_r': 28,
            'lsd_brake_f': 13, 'lsd_brake_r': 19,
        }
    elif "Tokyo" in track_name:
        return {
            **base,
            'height_f': base['height_f'] + 3, 'height_r': base['height_r'] + 3,
            'downforce_f': 160, 'downforce_r': 320,
            'max_speed': 270, 'final_gear': 4.50,
            'lsd_init_f': 9, 'lsd_init_r': 14,
            'lsd_accel_f': 17, 'lsd_accel_r': 24,
            'lsd_brake_f': 11, 'lsd_brake_r': 17,
        }
    else:
        return {
            **base,
            'downforce_f': 180, 'downforce_r': 350,
            'max_speed': 290, 'final_gear': 4.00,
            'lsd_init_f': 10, 'lsd_init_r': 15,
            'lsd_accel_f': 18, 'lsd_accel_r': 25,
            'lsd_brake_f': 12, 'lsd_brake_r': 18,
        }

# ============================================
# ТОП-5 МАШИН
# ============================================

def get_top_5_cars(track_name):
    """Возвращает топ-5 машин для трассы"""
    
    if "Monza" in track_name:
        sorted_cars = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('power', 0), reverse=True)
    elif "Nordschleife" in track_name:
        sorted_cars = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('power', 0) / max(x[1].get('weight', 1), 1), reverse=True)
    elif "Tokyo" in track_name:
        sorted_cars = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('weight', 9999))
    else:
        sorted_cars = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('pp', 0), reverse=True)
    
    top_5 = []
    for name, data in sorted_cars[:5]:
        if data.get('pp', 0) > 0:
            top_5.append({
                'name': name,
                'pp': data.get('pp', 0),
                'power': data.get('power', 0),
                'weight': data.get('weight', 0),
                'drive': data.get('drive_type', '?')
            })
    return top_5

# ============================================
# ФУНКЦИИ РАСЧЁТА
# ============================================

def calculate_pp(weight, power, downforce, drive_type):
    if weight == 0:
        return 0
    base_pp = (power / weight) * 100
    downforce_bonus = downforce / 20
    drive_bonus = 1.1 if drive_type == "4WD" else 1.0
    return round(base_pp * drive_bonus + downforce_bonus, 1)

def calculate_handling(camber_f, camber_r, toe_f, toe_r, height_f, height_r, 
                       spring_f, spring_r, arb_f, arb_r, downforce_f, downforce_r):
    
    turn_in = round((camber_f - camber_r) * 2 + (toe_f - toe_r) * 10 + (height_r - height_f) / 20 + (arb_f - arb_r) / 10, 1)
    turn_in = max(-10, min(10, turn_in))
    stability = round(10 - abs(toe_f + toe_r) * 5 - abs(camber_f + camber_r) / 2 - abs(height_f - height_r) / 50, 1)
    stability = max(0, min(10, stability))
    grip = round(5 + (downforce_f + downforce_r) / 100 + (4 - abs(camber_f + camber_r) / 2) - abs(spring_f - spring_r) / 10, 1)
    grip = max(1, min(10, grip))
    response = round((spring_f + spring_r) / 2 + (100 - (height_f + height_r) / 2) / 20, 1)
    response = max(1, min(10, response))
    
    return {'turn_in': turn_in, 'stability': stability, 'grip': grip, 'response': response}

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 Тюнинг Калькулятор v3")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин")

# Боковая панель
with st.sidebar:
    st.header("🏁 Выбор")
    
    selected_track = st.selectbox("Трасса", TRACKS)
    selected_car = st.selectbox("Автомобиль", CAR_NAMES)
    
    if st.button("🎯 Применить оптимальные настройки", use_container_width=True):
        tune = get_custom_tune(selected_car, selected_track)
        for key, value in tune.items():
            st.session_state[key] = value
        st.success(f"✅ Применены настройки для {selected_car} на трассе {selected_track}")
        st.rerun()

# Инициализация
if 'height_f' not in st.session_state:
    tune = get_custom_tune(CAR_NAMES[0] if CAR_NAMES else "", TRACKS[0])
    for key, value in tune.items():
        st.session_state[key] = value

# ============================================
# ТОП-5 МАШИН
# ============================================

st.subheader(f"🏆 Топ-5 машин для трассы: {selected_track}")

top_cars = get_top_5_cars(selected_track)
if top_cars:
    cols = st.columns(5)
    for i, car in enumerate(top_cars):
        with cols[i]:
            st.markdown(f"**{i+1}. {car['name'][:20]}**")
            st.caption(f"PP: {car['pp']} | {car['power']} л.с.")
            if st.button(f"Выбрать", key=f"top_{i}"):
                st.session_state.selected_car = car['name']
                st.rerun()
st.divider()

# ============================================
# ТЮНИНГ
# ============================================

st.subheader(f"🔧 Настройки для {selected_car} на трассе {selected_track}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏗️ Подвеска")
    st.session_state.height_f = st.slider("Высота перед (мм)", 60, 100, st.session_state.height_f)
    st.session_state.height_r = st.slider("Высота зад (мм)", 60, 100, st.session_state.height_r)
    st.session_state.spring_f = st.slider("Пружины перед", 3.0, 6.0, st.session_state.spring_f, 0.1)
    st.session_state.spring_r = st.slider("Пружины зад", 3.0, 6.0, st.session_state.spring_r, 0.1)
    st.session_state.arb_f = st.slider("Стабилизатор перед", 3, 8, st.session_state.arb_f)
    st.session_state.arb_r = st.slider("Стабилизатор зад", 3, 8, st.session_state.arb_r)
    st.session_state.camber_f = st.slider("Развал перед (°)", -3.0, 0.0, st.session_state.camber_f, 0.1)
    st.session_state.camber_r = st.slider("Развал зад (°)", -3.0, 0.0, st.session_state.camber_r, 0.1)
    st.session_state.toe_f = st.slider("Схождение перед", -0.3, 0.3, st.session_state.toe_f, 0.01)
    st.session_state.toe_r = st.slider("Схождение зад", -0.3, 0.3, st.session_state.toe_r, 0.01)

with col2:
    st.markdown("### 🌬️ Аэродинамика")
    st.session_state.downforce_f = st.slider("Прижимная сила перед", 100, 300, st.session_state.downforce_f)
    st.session_state.downforce_r = st.slider("Прижимная сила зад", 200, 500, st.session_state.downforce_r)
    
    st.markdown("### ⚙️ Трансмиссия")
    st.session_state.max_speed = st.slider("Макс скорость (км/ч)", 250, 350, st.session_state.max_speed)
    st.session_state.final_gear = st.slider("Финальная передача", 3.0, 5.0, st.session_state.final_gear, 0.05)
    
    st.markdown("### 🔧 LSD")
    st.session_state.lsd_init_r = st.slider("LSD начальный", 5, 25, st.session_state.lsd_init_r)
    st.session_state.lsd_accel_r = st.slider("LSD ускорение", 10, 40, st.session_state.lsd_accel_r)

# ============================================
# АНАЛИЗ
# ============================================

st.divider()
st.subheader("📊 Результат")

if selected_car in CAR_DATABASE:
    car_data = CAR_DATABASE[selected_car]
    total_downforce = st.session_state.downforce_f + st.session_state.downforce_r
    
    pp = calculate_pp(
        car_data.get('weight', 1450),
        car_data.get('power', 500),
        total_downforce,
        car_data.get('drive_type', 'FR')
    )
    
    handling = calculate_handling(
        st.session_state.camber_f, st.session_state.camber_r,
        st.session_state.toe_f, st.session_state.toe_r,
        st.session_state.height_f, st.session_state.height_r,
        st.session_state.spring_f, st.session_state.spring_r,
        st.session_state.arb_f, st.session_state.arb_r,
        st.session_state.downforce_f, st.session_state.downforce_r
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏁 Итоговый PP", f"{pp}")
    with col2:
        st.metric("🔄 Поворачиваемость", f"{handling['turn_in']:.1f}")
    with col3:
        st.metric("🛡️ Стабильность", f"{handling['stability']:.1f}/10")
    
    # Радар
    categories = ['Поворачиваемость', 'Стабильность', 'Сцепление', 'Отклик']
    values = [handling['turn_in'] + 5, handling['stability'], handling['grip'], handling['response']]
    
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', name=selected_car[:20]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("💡 Нажмите «Применить оптимальные настройки» для индивидуального тюнинга под вашу машину и трассу")
