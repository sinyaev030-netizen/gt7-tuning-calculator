import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="GT7 Калькулятор - Все трассы", layout="wide")

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
# ВСЕ ТРАССЫ GT7
# ============================================

TRACKS = [
    "Франция Alsace - Деревня",
    "Франция Alsace - Деревня (обратн.)",
    "Франция Alsace - тестовая трасса",
    "Франция Alsace - тестовая трасса (обратн.)",
    "Италия Autodrome Lago Maggiore - Восток",
    "Италия Autodrome Lago Maggiore - Восток (обратн.)",
    "Италия Autodrome Lago Maggiore - Запад",
    "Италия Autodrome Lago Maggiore - Запад (обратн.)",
    "Италия Autodrome Lago Maggiore - Центр",
    "Италия Autodrome Lago Maggiore - Центр (обратн.)",
    "Италия Autodrome Lago Maggiore - полная трасса",
    "Италия Autodrome Lago Maggiore - полная трасса (обратн.)",
    "Италия Autodromo Nazionale Monza",
    "Италия Autodromo Nazionale Monza (без шиканы)",
    "Бразилия Autódromo de Interlagos",
    "Япония Autopolis International Racing Course",
    "США Blue Moon Bay Speedway - внутренняя A",
    "Великобритания Brands Hatch - Grand Prix Circuit",
    "Великобритания Brands Hatch - Indy Circuit",
    "Канада Circuit Gilles-Villeneuve",
    "Испания Circuit de Barcelona-Catalunya (GP)",
    "Франция Circuit de Sainte-Croix - A",
    "Франция Circuit de Sainte-Croix - B",
    "Франция Circuit de Sainte-Croix - C",
    "Бельгия Spa (24 часа)",
    "США Daytona - дорожная",
    "Швейцария Deep Forest Raceway",
    "Хорватия Dragon Trail - Побережье",
    "Хорватия Dragon Trail - Сады",
    "Швейцария Eiger Nordwand",
    "Япония Fuji International Speedway",
    "США Grand Valley - шоссе №1",
    "Франция Le Mans (24 часа)",
    "Япония High Speed Ring",
    "Япония Kyoto Driving Park - Yamagiwa",
    "США Michelin Raceway Road Atlanta",
    "Австралия Mount Panorama",
    "Германия Nürburgring (24 часа)",
    "Германия Nürburgring GP",
    "Германия Nürburgring Nordschleife",
    "Австрия Red Bull Ring",
    "Италия Sardegna - Road Track - A",
    "Италия Sardegna - Road Track - B",
    "Италия Sardegna - Road Track - C",
    "Япония Suzuka Circuit",
    "Япония Tokyo Expressway - Центр",
    "США Trial Mountain Circuit",
    "Япония Tsukuba Circuit",
    "США Watkins Glen",
    "США WeatherTech Raceway Laguna Seca",
    "США Willow Springs - Big Willow",
    "ОАЭ Yas Marina Circuit",
]

# ============================================
# БАЗА ДАННЫХ ТРАСС С ТОП-5 МАШИНАМИ И НАСТРОЙКАМИ
# ============================================

TRACK_DATABASE = {
    # Скоростные трассы
    "Италия Autodromo Nazionale Monza": {
        "type": "speed",
        "description": "🏁 Скоростная трасса, длинные прямые",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "Ferrari 458 Italia GT3 '13", "McLaren 720S GT3 '23", "Nissan GT-R Nismo GT3 '18", "Mercedes-AMG GT3 '20"],
        "settings": {
            "height_f": 63, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7, "comp_f": 35, "comp_r": 38, "ext_f": 45, "ext_r": 48,
            "downforce_f": 140, "downforce_r": 280, "max_speed": 330, "final_gear": 3.60,
            "brake_balance": -3, "camber_f": -2.6, "camber_r": -1.9, "toe_f": 0.18, "toe_r": 0.28,
            "lsd_init_f": 12, "lsd_init_r": 18, "lsd_accel_f": 20, "lsd_accel_r": 30,
            "lsd_brake_f": 14, "lsd_brake_r": 20
        }
    },
    "Франция Le Mans (24 часа)": {
        "type": "speed",
        "description": "🌊 Максимальная скорость, длинные прямые",
        "top_cars": ["Porsche 919 Hybrid '16", "Toyota TS050 Hybrid '16", "Audi R18 '16", "Bugatti Vision GT", "Peugeot 908 HDi FAP '10"],
        "settings": {
            "height_f": 60, "height_r": 65, "spring_f": 5.2, "spring_r": 5.6,
            "arb_f": 6, "arb_r": 7, "comp_f": 38, "comp_r": 40, "ext_f": 48, "ext_r": 50,
            "downforce_f": 120, "downforce_r": 250, "max_speed": 360, "final_gear": 3.40,
            "brake_balance": -3, "camber_f": -2.8, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30,
            "lsd_init_f": 13, "lsd_init_r": 20, "lsd_accel_f": 22, "lsd_accel_r": 35,
            "lsd_brake_f": 16, "lsd_brake_r": 22
        }
    },
    "Япония High Speed Ring": {
        "type": "speed",
        "description": "🏁 Круговая скоростная трасса",
        "top_cars": ["Nissan GT-R Nismo '17", "Porsche 911 Turbo S '20", "Ferrari F8 Tributo '19", "McLaren 720S '17", "Lamborghini Huracan LP 610-4 '15"],
        "settings": {
            "height_f": 65, "height_r": 70, "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7, "comp_f": 35, "comp_r": 38, "ext_f": 45, "ext_r": 48,
            "downforce_f": 130, "downforce_r": 260, "max_speed": 340, "final_gear": 3.50,
            "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.15, "toe_r": 0.25,
            "lsd_init_f": 11, "lsd_init_r": 17, "lsd_accel_f": 19, "lsd_accel_r": 28,
            "lsd_brake_f": 13, "lsd_brake_r": 19
        }
    },
    # Сложные техничные трассы
    "Германия Nürburgring Nordschleife": {
        "type": "technical",
        "description": "🌲 Зелёный ад, 73 поворота",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "BMW M4 GT3 '22", "Mercedes-AMG GT3 '20", "Audi R8 LMS Evo '19", "Ferrari 488 GT3 '18"],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 5, "arb_r": 5, "comp_f": 30, "comp_r": 32, "ext_f": 40, "ext_r": 42,
            "downforce_f": 230, "downforce_r": 440, "max_speed": 280, "final_gear": 4.20,
            "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_f": 10, "lsd_init_r": 14, "lsd_accel_f": 18, "lsd_accel_r": 24,
            "lsd_brake_f": 12, "lsd_brake_r": 18
        }
    },
    "Бельгия Spa (24 часа)": {
        "type": "technical",
        "description": "🏎️ Легендарная трасса, перепады высот",
        "top_cars": ["Porsche 911 GT3 R '19", "Ferrari 488 GT3 '18", "Audi R8 LMS '15", "McLaren 720S GT3 '19", "Mercedes-AMG GT3 '20"],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6, "comp_f": 32, "comp_r": 34, "ext_f": 42, "ext_r": 44,
            "downforce_f": 210, "downforce_r": 400, "max_speed": 300, "final_gear": 3.95,
            "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_f": 11, "lsd_init_r": 16, "lsd_accel_f": 19, "lsd_accel_r": 27,
            "lsd_brake_f": 13, "lsd_brake_r": 19
        }
    },
    "Япония Suzuka Circuit": {
        "type": "technical",
        "description": "🗻 Техничная трасса, S-образные связки",
        "top_cars": ["Honda NSX GT500 '16", "Nissan GT-R GT500 '16", "Toyota Supra GT500 '97", "Porsche 911 GT3 R '19", "Ferrari 488 GT3 '18"],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "comp_f": 32, "comp_r": 34, "ext_f": 42, "ext_r": 44,
            "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.00,
            "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_f": 11, "lsd_init_r": 15, "lsd_accel_f": 19, "lsd_accel_r": 26,
            "lsd_brake_f": 13, "lsd_brake_r": 19
        }
    },
}

# ============================================
# ФУНКЦИИ
# ============================================

def get_default_settings():
    """Возвращает настройки по умолчанию"""
    return {
        "height_f": 75, "height_r": 80,
        "spring_f": 4.5, "spring_r": 4.8,
        "arb_f": 5, "arb_r": 5,
        "comp_f": 30, "comp_r": 32,
        "ext_f": 40, "ext_r": 42,
        "camber_f": -2.0, "camber_r": -1.5,
        "toe_f": 0.10, "toe_r": 0.20,
        "downforce_f": 180, "downforce_r": 350,
        "max_speed": 290, "final_gear": 4.00,
        "brake_balance": -2,
        "lsd_init_f": 10, "lsd_init_r": 15,
        "lsd_accel_f": 18, "lsd_accel_r": 25,
        "lsd_brake_f": 12, "lsd_brake_r": 18
    }

def get_track_info(track_name):
    """Возвращает информацию о трассе"""
    if track_name in TRACK_DATABASE:
        return TRACK_DATABASE[track_name]
    # Для отсутствующих трасс - стандартные настройки
    return {
        "type": "mixed",
        "description": "🏎️ Стандартная трасса",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "Ferrari 488 GT3 '18", "McLaren 720S GT3 '19", "Nissan GT-R Nismo GT3 '18", "Mercedes-AMG GT3 '20"],
        "settings": get_default_settings()
    }

def get_custom_tune_for_car(car_name, track_name):
    """Возвращает индивидуальные настройки для машины на трассе"""
    car_data = CAR_DATABASE.get(car_name, {})
    drive_type = car_data.get('drive_type', 'FR')
    track_info = get_track_info(track_name)
    base_settings = track_info["settings"].copy()
    
    # Корректировка под тип привода
    if drive_type == "RR":
        base_settings["camber_f"] = max(-3.0, base_settings.get("camber_f", -2.0) - 0.1)
        base_settings["camber_r"] = max(-2.5, base_settings.get("camber_r", -1.5) - 0.1)
    elif drive_type == "4WD":
        base_settings["camber_f"] = min(-1.5, base_settings.get("camber_f", -2.0) + 0.1)
        base_settings["camber_r"] = min(-1.0, base_settings.get("camber_r", -1.5) + 0.1)
    
    return base_settings

def get_top_5_cars_with_data(track_name):
    """Возвращает топ-5 машин для трассы с данными"""
    track_info = get_track_info(track_name)
    top_car_names = track_info.get("top_cars", [])
    
    top_5 = []
    for car_name in top_car_names:
        if car_name in CAR_DATABASE:
            data = CAR_DATABASE[car_name]
            top_5.append({
                'name': car_name,
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
# ИНИЦИАЛИЗАЦИЯ SESSION STATE
# ============================================

def init_session_state():
    """Инициализирует все переменные session_state"""
    default_settings = get_default_settings()
    for key, value in default_settings.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if 'selected_car' not in st.session_state:
        st.session_state.selected_car = CAR_NAMES[0] if CAR_NAMES else ""
    if 'prev_track' not in st.session_state:
        st.session_state.prev_track = ""

# ============================================
# ИНТЕРФЕЙС
# ============================================

# Инициализация
init_session_state()

st.title("🏎️ GT7 Тюнинг Калькулятор - Все трассы")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин | 🏁 Трасс: **{len(TRACKS)}**")

# Боковая панель
with st.sidebar:
    st.header("🏁 Выбор трассы")
    selected_track = st.selectbox("Трасса", TRACKS)
    
    track_info = get_track_info(selected_track)
    st.info(f"**Тип:** {track_info['description']}")
    
    st.header("🚗 Выбор автомобиля")
    selected_car = st.selectbox("Автомобиль", CAR_NAMES, index=CAR_NAMES.index(st.session_state.selected_car) if st.session_state.selected_car in CAR_NAMES else 0)
    st.session_state.selected_car = selected_car
    
    # Обновление настроек при смене трассы
    if selected_track != st.session_state.prev_track:
        st.session_state.prev_track = selected_track
        tune = get_custom_tune_for_car(selected_car, selected_track)
        for key, value in tune.items():
            st.session_state[key] = value
        st.rerun()
    
    if st.button("🎯 Применить оптимальные настройки", use_container_width=True):
        tune = get_custom_tune_for_car(selected_car, selected_track)
        for key, value in tune.items():
            st.session_state[key] = value
        st.success(f"✅ Применены настройки для {selected_car[:30]}")

# ============================================
# ТОП-5 МАШИН
# ============================================

st.subheader(f"🏆 Топ-5 машин для трассы: {selected_track}")

top_cars = get_top_5_cars_with_data(selected_track)
if top_cars:
    cols = st.columns(5)
    for i, car in enumerate(top_cars):
        with cols[i]:
            st.markdown(f"**{i+1}. {car['name'][:20]}**")
            st.caption(f"PP: {car['pp']} | {car['power']} л.с.")
            if st.button(f"✅ Выбрать", key=f"top_{i}"):
                st.session_state.selected_car = car['name']
                st.rerun()
else:
    st.info("Рекомендации загружаются...")
st.divider()

# ============================================
# ТЮНИНГ
# ============================================

st.subheader(f"🔧 Настройки для {selected_car[:35]} на трассе {selected_track}")

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
    st.session_state.max_speed = st.slider("Макс скорость (км/ч)", 250, 360, st.session_state.max_speed)
    st.session_state.final_gear = st.slider("Финальная передача", 3.0, 5.0, st.session_state.final_gear, 0.05)
    
    st.markdown("### 🔧 LSD")
    st.session_state.lsd_init_r = st.slider("LSD начальный", 5, 25, st.session_state.lsd_init_r)
    st.session_state.lsd_accel_r = st.slider("LSD ускорение", 10, 40, st.session_state.lsd_accel_r)
    
    st.markdown("### 🛑 Тормоза")
    st.session_state.brake_balance = st.slider("Баланс тормозов", -5, 5, st.session_state.brake_balance)

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
        st.caption(f"Базовый PP: {car_data.get('pp', 0)}")
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
    
    # Характеристики
    with st.expander("📋 Характеристики автомобиля"):
        st.write(f"**Тип привода:** {car_data.get('drive_type', '?')}")
        st.write(f"**Мощность:** {car_data.get('power', 0)} л.с.")
        st.write(f"**Вес:** {car_data.get('weight', 0)} кг")
        st.write(f"**Удельная мощность:** {car_data.get('weight', 0) / car_data.get('power', 1):.2f} кг/л.с.")

st.markdown("---")
st.caption(f"🏎️ GT7 Калькулятор | {len(CAR_DATABASE)} машин | {len(TRACKS)} трасс")
