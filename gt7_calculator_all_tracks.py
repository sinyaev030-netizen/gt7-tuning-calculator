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
# ВСЕ ТРАССЫ
# ============================================

TRACKS = [
    "🏁 Autodromo Nazionale Monza",
    "🌲 Nürburgring Nordschleife",
    "🗻 Suzuka Circuit",
    "🏎️ Spa-Francorchamps",
    "🌊 Circuit de la Sarthe (Le Mans)",
    "🏙️ Tokyo Expressway - Центр",
    "⛰️ Deep Forest Raceway",
    "🏔️ Trial Mountain Circuit",
    "🇯🇵 Fuji International Speedway",
    "🇺🇸 WeatherTech Raceway Laguna Seca",
    "🇦🇺 Mount Panorama",
    "🇨🇦 Circuit Gilles-Villeneuve",
    "🇧🇷 Autódromo de Interlagos",
    "🇦🇹 Red Bull Ring",
    "🇪🇸 Circuit de Barcelona-Catalunya",
    "🇬🇧 Brands Hatch GP",
    "🇺🇸 Watkins Glen",
    "🇯🇵 Tsukuba Circuit",
    "🇯🇵 Autopolis",
    "🇭🇷 Dragon Trail",
]

# ============================================
# ПРЕСЕТЫ НАСТРОЕК ДЛЯ ТРАСС
# ============================================

def apply_track_preset(track_name):
    """Возвращает настройки для выбранной трассы"""
    
    # Базовые настройки
    preset = {
        'height_f': 75, 'height_r': 80,
        'spring_f': 4.5, 'spring_r': 4.8,
        'arb_f': 5, 'arb_r': 5,
        'comp_f': 30, 'comp_r': 32,
        'ext_f': 40, 'ext_r': 42,
        'camber_f': -2.0, 'camber_r': -1.5,
        'toe_f': 0.10, 'toe_r': 0.20,
        'downforce_f': 150, 'downforce_r': 300,
        'lsd_init_f': 10, 'lsd_init_r': 15,
        'lsd_accel_f': 18, 'lsd_accel_r': 25,
        'lsd_brake_f': 12, 'lsd_brake_r': 18,
        'max_speed': 290, 'final_gear': 4.0,
        'brake_balance': -2,
    }
    
    # Monza - скоростная трасса
    if "Monza" in track_name:
        preset.update({
            'height_f': 63, 'height_r': 68,
            'spring_f': 5.0, 'spring_r': 5.4,
            'downforce_f': 140, 'downforce_r': 280,
            'max_speed': 330, 'final_gear': 3.60,
            'brake_balance': -3,
        })
    
    # Nordschleife - сложная трасса
    elif "Nordschleife" in track_name:
        preset.update({
            'height_f': 70, 'height_r': 75,
            'downforce_f': 220, 'downforce_r': 420,
            'max_speed': 280, 'final_gear': 4.20,
        })
    
    # Suzuka - техничная
    elif "Suzuka" in track_name:
        preset.update({
            'height_f': 68, 'height_r': 72,
            'downforce_f': 200, 'downforce_r': 380,
            'max_speed': 290, 'final_gear': 4.00,
        })
    
    # Spa
    elif "Spa" in track_name:
        preset.update({
            'height_f': 67, 'height_r': 72,
            'downforce_f': 210, 'downforce_r': 400,
            'max_speed': 300, 'final_gear': 3.95,
        })
    
    # Le Mans
    elif "Le Mans" in track_name:
        preset.update({
            'height_f': 63, 'height_r': 68,
            'downforce_f': 150, 'downforce_r': 300,
            'max_speed': 340, 'final_gear': 3.50,
            'brake_balance': -3,
        })
    
    # Tokyo - городская
    elif "Tokyo" in track_name:
        preset.update({
            'height_f': 72, 'height_r': 77,
            'spring_f': 4.0, 'spring_r': 4.3,
            'downforce_f': 160, 'downforce_r': 320,
            'max_speed': 270, 'final_gear': 4.50,
            'brake_balance': -1,
        })
    
    return preset

# ============================================
# ФУНКЦИЯ ДЛЯ ТОП-5 МАШИН
# ============================================

def get_top_5_cars(track_name):
    """Возвращает топ-5 машин для трассы"""
    
    track_lower = track_name.lower()
    
    # Определяем приоритетные характеристики
    if "monza" in track_lower or "le mans" in track_lower or "daytona" in track_lower:
        # Скоростные трассы - важна мощность
        cars_sorted = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('power', 0), reverse=True)
    elif "nordschleife" in track_lower or "nürburgring" in track_lower or "spa" in track_lower:
        # Сложные трассы - важен баланс мощность/вес
        cars_sorted = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('power', 0) / max(x[1].get('weight', 1), 1), reverse=True)
    elif "tokyo" in track_lower or "city" in track_lower:
        # Городские трассы - важна управляемость (лёгкие машины)
        cars_sorted = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('weight', 9999))
    elif "suzuka" in track_lower or "fuji" in track_lower or "autopolis" in track_lower:
        # Техничные трассы - баланс
        cars_sorted = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('pp', 0), reverse=True)
    else:
        # По умолчанию - по PP
        cars_sorted = sorted(CAR_DATABASE.items(), key=lambda x: x[1].get('pp', 0), reverse=True)
    
    # Берём топ-5
    top_5 = []
    for name, data in cars_sorted[:5]:
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

def calculate_acceleration(lsd_accel_r, lsd_init_r, power, weight, drive_type):
    power_to_weight = power / weight if weight > 0 else 0
    lsd_bonus = (lsd_accel_r + lsd_init_r) / 20
    drive_bonus = 1.2 if drive_type == "4WD" else 1.0
    return round((power_to_weight * 10 + lsd_bonus) * drive_bonus, 1)

def calculate_braking(brake_balance, weight, downforce):
    brake_power = (weight / 1000) * 10 + downforce / 100
    balance_effect = brake_balance / 10
    return round(brake_power * (1 + balance_effect), 1)

# ============================================
# ИНИЦИАЛИЗАЦИЯ СЕССИИ
# ============================================

if 'height_f' not in st.session_state:
    preset = apply_track_preset("🏁 Autodromo Nazionale Monza")
    for key, value in preset.items():
        st.session_state[key] = value

if 'selected_car' not in st.session_state:
    st.session_state.selected_car = CAR_NAMES[0] if CAR_NAMES else ""

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 Тюнинг Калькулятор")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин")

# Боковая панель
with st.sidebar:
    st.header("🏁 Настройки")
    
    # Выбор трассы
    selected_track = st.selectbox("Выберите трассу", TRACKS)
    
    # Кнопка применения настроек
    if st.button(f"🎯 Применить настройки для трассы", use_container_width=True):
        preset = apply_track_preset(selected_track)
        for key, value in preset.items():
            st.session_state[key] = value
        st.success(f"✅ Применены настройки для {selected_track}")
        st.rerun()
    
    st.markdown("---")
    
    # Выбор машины
    selected_car = st.selectbox("Выберите машину", CAR_NAMES, index=CAR_NAMES.index(st.session_state.selected_car) if st.session_state.selected_car in CAR_NAMES else 0)
    st.session_state.selected_car = selected_car

# ============================================
# ТОП-5 МАШИН
# ============================================

st.subheader(f"🏆 Топ-5 машин для трассы: {selected_track}")

top_5_cars = get_top_5_cars(selected_track)

if top_5_cars:
    cols = st.columns(5)
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    
    for i, car in enumerate(top_5_cars):
        with cols[i]:
            st.markdown(f"### {medals[i]}")
            st.markdown(f"**{car['name'][:25]}**")
            st.metric("PP", f"{car['pp']:.0f}")
            st.metric("Мощность", f"{car['power']:.0f} л.с.")
            st.metric("Вес", f"{car['weight']:.0f} кг")
            st.caption(f"Привод: {car['drive']}")
            
            if st.button(f"Выбрать", key=f"pick_{i}"):
                st.session_state.selected_car = car['name']
                st.rerun()
else:
    st.info("Загрузка рекомендаций...")

st.divider()

# ============================================
# ТЮНИНГ
# ============================================

st.subheader("🔧 Настройки тюнинга")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏗️ Подвеска")
    st.session_state.height_f = st.slider("Высота перед (мм)", 60, 150, st.session_state.height_f)
    st.session_state.height_r = st.slider("Высота зад (мм)", 60, 150, st.session_state.height_r)
    st.session_state.spring_f = st.slider("Пружины перед (N/mm)", 2.0, 6.0, st.session_state.spring_f, 0.1)
    st.session_state.spring_r = st.slider("Пружины зад (N/mm)", 2.0, 6.0, st.session_state.spring_r, 0.1)
    st.session_state.arb_f = st.slider("Стабилизатор перед", 1, 10, st.session_state.arb_f)
    st.session_state.arb_r = st.slider("Стабилизатор зад", 1, 10, st.session_state.arb_r)
    st.session_state.comp_f = st.slider("Сжатие перед", 20, 60, st.session_state.comp_f)
    st.session_state.comp_r = st.slider("Сжатие зад", 20, 60, st.session_state.comp_r)
    st.session_state.ext_f = st.slider("Отбой перед", 20, 60, st.session_state.ext_f)
    st.session_state.ext_r = st.slider("Отбой зад", 20, 60, st.session_state.ext_r)
    
    st.markdown("### 🔧 Углы колёс")
    st.session_state.camber_f = st.slider("Развал перед (°)", -3.5, 0.0, st.session_state.camber_f, 0.1)
    st.session_state.camber_r = st.slider("Развал зад (°)", -3.0, 0.0, st.session_state.camber_r, 0.1)
    st.session_state.toe_f = st.slider("Схождение перед", -0.50, 0.50, st.session_state.toe_f, 0.01)
    st.session_state.toe_r = st.slider("Схождение зад", -0.50, 0.50, st.session_state.toe_r, 0.01)

with col2:
    st.markdown("### 🔧 LSD")
    st.session_state.lsd_init_f = st.slider("Начальный момент (перед)", 5, 40, st.session_state.lsd_init_f)
    st.session_state.lsd_init_r = st.slider("Начальный момент (зад)", 5, 40, st.session_state.lsd_init_r)
    st.session_state.lsd_accel_f = st.slider("Ускорение (перед)", 5, 60, st.session_state.lsd_accel_f)
    st.session_state.lsd_accel_r = st.slider("Ускорение (зад)", 5, 60, st.session_state.lsd_accel_r)
    st.session_state.lsd_brake_f = st.slider("Торможение (перед)", 5, 60, st.session_state.lsd_brake_f)
    st.session_state.lsd_brake_r = st.slider("Торможение (зад)", 5, 60, st.session_state.lsd_brake_r)
    
    st.markdown("### 🌬️ Аэродинамика")
    st.session_state.downforce_f = st.slider("Прижимная сила перед", 0, 400, st.session_state.downforce_f)
    st.session_state.downforce_r = st.slider("Прижимная сила зад", 0, 600, st.session_state.downforce_r)
    
    st.markdown("### ⚙️ Трансмиссия")
    st.session_state.max_speed = st.slider("Максимальная скорость (км/ч)", 200, 400, st.session_state.max_speed)
    st.session_state.final_gear = st.slider("Финальная передача", 2.5, 5.5, st.session_state.final_gear, 0.01)
    
    st.markdown("### 🛑 Тормоза")
    st.session_state.brake_balance = st.slider("Баланс тормозов", -5, 5, st.session_state.brake_balance)

# ============================================
# АНАЛИЗ
# ============================================

st.divider()
st.subheader("📊 Анализ характеристик")

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
    
    acceleration = calculate_acceleration(
        st.session_state.lsd_accel_r, st.session_state.lsd_init_r,
        car_data.get('power', 500),
        car_data.get('weight', 1450),
        car_data.get('drive_type', 'FR')
    )
    
    braking = calculate_braking(st.session_state.brake_balance, 
                                car_data.get('weight', 1450), 
                                total_downforce)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏁 PP", f"{pp:.1f}")
        st.metric("⚡ Ускорение", f"{acceleration:.1f}")
    with col2:
        st.metric("🔄 Поворачиваемость", f"{handling['turn_in']:.1f}")
        st.metric("🛡️ Стабильность", f"{handling['stability']:.1f}/10")
    with col3:
        st.metric("🏎️ Сцепление", f"{handling['grip']:.1f}/10")
        st.metric("📈 Отклик", f"{handling['response']:.1f}/10")
    with col4:
        st.metric("🛑 Торможение", f"{braking:.1f}")
        st.metric("🎯 Трасса", selected_track.split()[1] if len(selected_track.split()) > 1 else selected_track[:15])
    
    # Радар
    categories = ['Ускорение', 'Поворачиваемость', 'Стабильность', 'Сцепление', 'Торможение', 'Отклик']
    values = [
        min(acceleration, 10),
        handling['turn_in'] + 5,
        handling['stability'],
        handling['grip'],
        min(braking / 10, 10),
        handling['response']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', name=selected_car[:30]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=450)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Выберите машину из списка")

st.markdown("---")
st.caption(f"🏎️ GT7 Калькулятор | {len(CAR_DATABASE)} машин | Выберите трассу → Примените настройки → Тюнингуйте")
