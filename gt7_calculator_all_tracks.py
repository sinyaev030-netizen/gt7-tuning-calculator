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
# ВСЕ ТРАССЫ GT7 (БОЛЕЕ 90)
# ============================================

TRACKS = [
    "🏁 Автодром (обратн.)", "🏁 Автодром", "🏁 Alsace - Деревня (обратн.)", "🏁 Alsace - Деревня",
    "🏁 Alsace - тестовая трасса (обратн.)", "🏁 Alsace - тестовая трасса",
    "🏁 Autodrome Lago Maggiore - Восток (обратн.)", "🏁 Autodrome Lago Maggiore - Восток",
    "🏁 Autodrome Lago Maggiore - Запад (обратн.)", "🏁 Autodrome Lago Maggiore - Запад",
    "🏁 Autodrome Lago Maggiore - Центр (обратн.)", "🏁 Autodrome Lago Maggiore - Центр",
    "🏁 Autodrome Lago Maggiore - восточная часть (обратн.)", "🏁 Autodrome Lago Maggiore - восточная часть",
    "🏁 Autodrome Lago Maggiore - западная часть (обратн.)", "🏁 Autodrome Lago Maggiore - западная часть",
    "🏁 Autodrome Lago Maggiore - полная трасса (обратн.)", "🏁 Autodrome Lago Maggiore - полная трасса",
    "🏁 Autodromo Nazionale Monza (без шиканы)", "🏁 Autodromo Nazionale Monza",
    "🏁 Autódromo de Interlagos", "🏁 Autopolis International Racing Course (укороченная)",
    "🏁 Autopolis International Racing Course", "🏁 Blue Moon Bay Speedway - внутренняя A (обратн.)",
    "🏁 Blue Moon Bay Speedway - внутренняя A", "🏁 Brands Hatch - Grand Prix Circuit",
    "🏁 Brands Hatch - Indy Circuit", "🏁 Circuit Gilles-Villeneuve",
    "🏁 Circuit de Barcelona-Catalunya - вариант GP (без шиканы)",
    "🏁 Circuit de Barcelona-Catalunya - вариант GP",
    "🏁 Circuit de Barcelona-Catalunya - вариант национальных гонок",
    "🏁 Circuit de Barcelona-Catalunya - вариант ралли-кросса",
    "🏁 Circuit de Sainte-Croix - A (обратн.)", "🏁 Circuit de Sainte-Croix - A",
    "🏁 Circuit de Sainte-Croix - B (обратн.)", "🏁 Circuit de Sainte-Croix - B",
    "🏁 Circuit de Sainte-Croix - C (обратн.)", "🏁 Circuit de Sainte-Croix - C",
    "🏁 Daytona - дорожная", "🏁 Deep Forest Raceway (обратн.)", "🏁 Deep Forest Raceway",
    "🏁 Dragon Trail - Берег (обратн.)", "🏁 Dragon Trail - Побережье",
    "🏁 Dragon Trail - Сады (обратн.)", "🏁 Dragon Trail - Сады",
    "🏁 Eiger Nordwand (обратн.)", "🏁 Eiger Nordwand", "🏁 Fuji International Speedway (короткая)",
    "🏁 Fuji International Speedway", "🏁 Grand Valley - шоссе №1 (обратн.)",
    "🏁 Grand Valley - шоссе №1", "🏁 Grand Valley - юг (обратн.)", "🏁 Grand Valley - юг",
    "🏁 High Speed Ring (обратн.)", "🏁 High Speed Ring",
    "🏁 Kyoto Driving Park - Yamagiwa (обратн.)", "🏁 Kyoto Driving Park - Yamagiwa",
    "🏁 Kyoto Driving Park - Yamagiwa + Miyabi (обратн.)", "🏁 Kyoto Driving Park - Yamagiwa + Miyabi",
    "🏁 Le Mans (24 часа) (без шиканы)", "🏁 Le Mans (24 часа)",
    "🏁 Michelin Raceway Road Atlanta", "🏁 Mount Panorama Motor Racing Circuit",
    "🏁 Nürburgring (24 часа)", "🏁 Nürburgring (гонка на выносливость)",
    "🏁 Nürburgring (спринт)", "🏁 Nürburgring GP", "🏁 Nürburgring Nordschleife",
    "🏁 Red Bull Ring (полная)", "🏁 Sardegna - Road Track - A (обратн.)",
    "🏁 Sardegna - Road Track - A", "🏁 Sardegna - Road Track - B (обратн.)",
    "🏁 Sardegna - Road Track - B", "🏁 Sardegna - Road Track - C (обратн.)",
    "🏁 Sardegna - Road Track - C", "🏁 Spa (24 часа)",
    "🏁 Suzuka Circuit (восточная)", "🏁 Suzuka Circuit",
    "🏁 Tokyo Expressway - Восток (по часовой)", "🏁 Tokyo Expressway - Восток (против часовой)",
    "🏁 Tokyo Expressway - Центр (по часовой)", "🏁 Tokyo Expressway - Центр (против часовой)",
    "🏁 Tokyo Expressway - Юг (по часовой)", "🏁 Tokyo Expressway - Юг (против часовой)",
    "🏁 Trial Mountain (обратн.)", "🏁 Trial Mountain Circuit",
    "🏁 Tsukuba Circuit", "🏁 Watkins Glen (длинная)", "🏁 Watkins Glen (короткая)",
    "🏁 WeatherTech Raceway Laguna Seca", "🏁 Willow Springs - Big Willow",
    "🏁 Willow Springs - Horse Thief Mile (обратн.)", "🏁 Willow Springs - Horse Thief Mile",
    "🏁 Willow Springs - Streets (обратн.)", "🏁 Willow Springs - Streets",
    "🏁 Yas Marina Circuit"
]

# ============================================
# РЕКОМЕНДАЦИИ ТОП-5 МАШИН ДЛЯ ТРАСС
# ============================================

def get_top_cars_for_track(track_name, car_database):
    """Рекомендует лучшие машины для трассы на основе характеристик"""
    
    # Определяем тип трассы
    track_type = "balanced"  # по умолчанию
    
    if any(x in track_name for x in ["Monza", "Le Mans", "Daytona", "High Speed", "Route X"]):
        track_type = "speed"  # скоростная трасса
    elif any(x in track_name for x in ["Nordschleife", "Nürburgring", "Spa", "Green Hell"]):
        track_type = "technical"  # сложная техничная трасса
    elif any(x in track_name for x in ["Tokyo", "City", "Street"]):
        track_type = "city"  # городская трасса
    elif any(x in track_name for x in ["Suzuka", "Fuji", "Autopolis", "Tsukuba"]):
        track_type = "technical"  # техничная японская
    elif any(x in track_name for x in ["Laguna", "Willow", "Trial Mountain", "Deep Forest"]):
        track_type = "twisty"  # извилистая трасса
    elif any(x in track_name for x in ["Sardegna", "Alsace", "Sainte-Croix"]):
        track_type = "mixed"  # смешанная трасса
    
    cars_list = []
    
    for name, data in car_database.items():
        pp = data.get('pp', 0)
        power = data.get('power', 0)
        weight = data.get('weight', 0)
        drive = data.get('drive_type', 'FR')
        
        # Пропускаем машины с нулевыми данными
        if pp == 0 or power == 0 or weight == 0:
            continue
        
        # Базовые показатели
        power_to_weight = power / weight  # соотношение мощность/вес
        weight_kg = weight
        
        # Расчёт рейтинга в зависимости от типа трассы
        score = 0
        
        if track_type == "speed":
            # Для скоростных трасс: важна мощность и аэродинамика
            score = power * 0.15 + (1000 / weight) * 2 + pp * 0.5
            
        elif track_type == "technical":
            # Для техничных трасс: важна управляемость и вес
            score = (1000 / weight) * 5 + (power / 100) * 2 + pp * 0.4
            
        elif track_type == "city":
            # Для городских трасс: важна маневренность и разгон
            score = (1000 / weight) * 6 + (power / 150) * 3 + pp * 0.3
            
        elif track_type == "twisty":
            # Для извилистых трасс: важна лёгкость и сцепление
            score = (1000 / weight) * 7 + (power / 200) * 2 + pp * 0.3
            
        else:
            # Для смешанных трасс: баланс
            score = (power / 100) * 3 + (1000 / weight) * 4 + pp * 0.4
        
        # Бонус за тип привода
        if drive == "4WD" and track_type in ["city", "twisty"]:
            score += 20  # Полный привод хорош для сложных условий
        elif drive == "FR" and track_type == "speed":
            score += 15  # Задний привод хорош для скорости
        elif drive == "MR" and track_type == "technical":
            score += 15  # Среднемоторные хороши для техничных трасс
        elif drive == "RR" and track_type == "technical":
            score += 10  # Заднемоторные (Porsche) хороши на техничных трассах
        
        # Бонус за известные гоночные машины
        if "GT3" in name or "GT4" in name or "Gr.3" in name or "Gr.4" in name:
            score += 30  # Гоночные машины лучше на любых трассах
        if "GT500" in name or "Super GT" in name:
            score += 40
        if "Vision" in name:
            score += 20
        
        cars_list.append({
            'name': name,
            'pp': round(pp, 0),
            'power': round(power, 0),
            'weight': round(weight, 0),
            'power_to_weight': round(power_to_weight, 2),
            'drive': drive,
            'score': round(score, 0),
            'track_type': track_type
        })
    
    # Сортируем по рейтингу (от большего к меньшему)
    cars_list.sort(key=lambda x: x['score'], reverse=True)
    
    # Возвращаем топ-5
    return cars_list[:5]
    
    # Сортируем по score и берём топ-5
    cars_list.sort(key=lambda x: x['score'], reverse=True)
    return cars_list[:5]

# ============================================
# ПРЕДУСТАНОВКИ ДЛЯ ТРАСС
# ============================================

def get_track_preset(track_name):
    """Возвращает предустановки для трассы"""
    
    # Базовые настройки по умолчанию
    default_preset = {
        "height_f": 75, "height_r": 80,
        "spring_f": 4.5, "spring_r": 4.8,
        "arb_f": 5, "arb_r": 5,
        "comp_f": 30, "comp_r": 32,
        "ext_f": 40, "ext_r": 42,
        "camber_f": -2.0, "camber_r": -1.5,
        "toe_f": 0.10, "toe_r": 0.20,
        "downforce_f": 150, "downforce_r": 300,
        "lsd_init_f": 10, "lsd_init_r": 15,
        "lsd_accel_f": 18, "lsd_accel_r": 25,
        "lsd_brake_f": 12, "lsd_brake_r": 18,
        "max_speed": 290, "final_gear": 4.0,
        "brake_balance": -2,
        "power_restrictor": 100, "ballast": 0, "ballast_pos": 0
    }
    
    # Настройки для скоростных трасс
    if "Monza" in track_name or "Le Mans" in track_name or "Daytona" in track_name:
        return {
            "height_f": 63, "height_r": 68,
            "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7,
            "comp_f": 38, "comp_r": 40,
            "ext_f": 48, "ext_r": 50,
            "camber_f": -2.6, "camber_r": -1.9,
            "toe_f": 0.18, "toe_r": 0.28,
            "downforce_f": 140, "downforce_r": 280,
            "lsd_init_f": 13, "lsd_init_r": 19,
            "lsd_accel_f": 22, "lsd_accel_r": 32,
            "lsd_brake_f": 16, "lsd_brake_r": 22,
            "max_speed": 330, "final_gear": 3.60,
            "brake_balance": -3,
            "power_restrictor": 100, "ballast": 0, "ballast_pos": 0
        }
    
    # Настройки для сложных трасс (Нюрбургринг, Спа)
    if "Nordschleife" in track_name or "Nürburgring" in track_name or "Spa" in track_name:
        return {
            "height_f": 70, "height_r": 75,
            "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 5, "arb_r": 5,
            "comp_f": 30, "comp_r": 32,
            "ext_f": 40, "ext_r": 42,
            "camber_f": -2.2, "camber_r": -1.6,
            "toe_f": 0.10, "toe_r": 0.20,
            "downforce_f": 220, "downforce_r": 420,
            "lsd_init_f": 10, "lsd_init_r": 15,
            "lsd_accel_f": 18, "lsd_accel_r": 25,
            "lsd_brake_f": 12, "lsd_brake_r": 18,
            "max_speed": 280, "final_gear": 4.20,
            "brake_balance": -2,
            "power_restrictor": 100, "ballast": 0, "ballast_pos": 0
        }
    
    # Настройки для городских трасс (Токио)
    if "Tokyo" in track_name or "City" in track_name:
        return {
            "height_f": 72, "height_r": 77,
            "spring_f": 4.0, "spring_r": 4.3,
            "arb_f": 4, "arb_r": 4,
            "comp_f": 28, "comp_r": 30,
            "ext_f": 38, "ext_r": 40,
            "camber_f": -1.8, "camber_r": -1.3,
            "toe_f": 0.05, "toe_r": 0.15,
            "downforce_f": 160, "downforce_r": 320,
            "lsd_init_f": 9, "lsd_init_r": 14,
            "lsd_accel_f": 17, "lsd_accel_r": 24,
            "lsd_brake_f": 11, "lsd_brake_r": 17,
            "max_speed": 270, "final_gear": 4.50,
            "brake_balance": -1,
            "power_restrictor": 100, "ballast": 0, "ballast_pos": 0
        }
    
    # Настройки для техничных трасс (Судзука, Фудзи)
    if "Suzuka" in track_name or "Fuji" in track_name:
        return {
            "height_f": 68, "height_r": 72,
            "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6,
            "comp_f": 32, "comp_r": 34,
            "ext_f": 42, "ext_r": 44,
            "camber_f": -2.3, "camber_r": -1.7,
            "toe_f": 0.12, "toe_r": 0.22,
            "downforce_f": 200, "downforce_r": 380,
            "lsd_init_f": 11, "lsd_init_r": 16,
            "lsd_accel_f": 19, "lsd_accel_r": 28,
            "lsd_brake_f": 13, "lsd_brake_r": 19,
            "max_speed": 290, "final_gear": 4.00,
            "brake_balance": -2,
            "power_restrictor": 100, "ballast": 0, "ballast_pos": 0
        }
    
    return default_preset

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
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 Тюнинг Калькулятор - Все трассы")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин | 🏁 Трасс: **{len(TRACKS)}**")

# Боковая панель
with st.sidebar:
    st.header("🏁 Выбор")
    
    selected_car = st.selectbox("Модель автомобиля", CAR_NAMES)
    selected_track = st.selectbox("Выберите трассу", TRACKS)
    
    if st.button(f"🎯 Применить настройки для выбранной трассы", use_container_width=True):
        st.session_state['apply_track'] = True
        st.rerun()

# ============================================
# ВКЛАДКИ
# ============================================

tab_rec, tab_tune, tab_analysis = st.tabs(["🏆 ТОП-5 МАШИН ДЛЯ ТРАССЫ", "🔧 ТЮНИНГ", "📊 АНАЛИЗ"])

# ============================================
# TAB: ТОП-5 МАШИН ДЛЯ ТРАССЫ
# ============================================
with tab_rec:
    st.header(f"🏆 Топ-5 машин для трассы: {selected_track}")
    
    # Определяем тип трассы для отображения
    if any(x in selected_track for x in ["Monza", "Le Mans", "Daytona"]):
        st.info("🏁 **Скоростная трасса** — важна максимальная скорость и мощность")
    elif any(x in selected_track for x in ["Nordschleife", "Nürburgring", "Spa"]):
        st.info("🌲 **Сложная техничная трасса** — важна стабильность и управляемость")
    elif any(x in selected_track for x in ["Tokyo", "City"]):
        st.info("🏙️ **Городская трасса** — важна маневренность и точность")
    elif any(x in selected_track for x in ["Suzuka", "Fuji", "Autopolis"]):
        st.info("🗻 **Техничная трасса** — нужен баланс скорости и управляемости")
    else:
        st.info("🏎️ **Смешанная трасса** — нужен баланс характеристик")
    
    top_cars = get_top_cars_for_track(selected_track, CAR_DATABASE)
    
    if top_cars:
        for i, car in enumerate(top_cars):
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 1, 1, 1, 1])
                
                # Медаль
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                with col1:
                    st.markdown(f"## {medals[i]}")
                
                # Название машины
                with col2:
                    st.markdown(f"**{car['name'][:45]}**")
                    st.caption(f"Рейтинг: {car['score']}")
                
                # Характеристики
                with col3:
                    st.metric("PP", f"{car['pp']:.0f}")
                with col4:
                    st.metric("Мощность", f"{car['power']:.0f} л.с.")
                with col5:
                    st.metric("Вес", f"{car['weight']:.0f} кг")
                with col6:
                    st.metric("Привод", car['drive'])
                
                # Кнопка выбора
                if st.button(f"✅ Выбрать", key=f"select_{i}"):
                    st.session_state['selected_car'] = car['name']
                    st.rerun()
                
                st.divider()
        
        # Показываем ещё рекомендации
        with st.expander("ℹ️ Как рассчитывается рейтинг?"):
            st.write("""
            **Рейтинг учитывает:**
            - **Скоростные трассы** (Monza, Le Mans): мощность и максимальная скорость
            - **Техничные трассы** (Nordschleife, Suzuka): управляемость и вес
            - **Городские трассы** (Tokyo): маневренность и разгон
            - **Извилистые трассы** (Laguna Seca): лёгкость и сцепление
            
            **Бонусы:**
            - Гоночные машины (GT3, GT4, Gr.3) получают преимущество
            - Полный привод (4WD) лучше на сложных трассах
            - Задний привод (FR) лучше на скоростных трассах
            """)
    else:
        st.warning("Недостаточно данных для рекомендаций. Убедитесь, что база машин загружена.")

# ============================================
# TAB: ТЮНИНГ
# ============================================
with tab_tune:
    # Получаем предустановки для трассы
    if 'apply_track' in st.session_state:
        preset = get_track_preset(selected_track)
        for key, value in preset.items():
            st.session_state[key] = value
        st.session_state.pop('apply_track')
        st.success(f"✅ Применены настройки для трассы: {selected_track}")
    
    # Инициализация
    for key, value in get_track_preset(selected_track).items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.header("🏗️ Подвеска")
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
        
        st.header("🔧 Углы колёс")
        st.session_state.camber_f = st.slider("Развал перед (°)", -3.5, 0.0, st.session_state.camber_f, 0.1)
        st.session_state.camber_r = st.slider("Развал зад (°)", -3.0, 0.0, st.session_state.camber_r, 0.1)
        st.session_state.toe_f = st.slider("Схождение перед", -0.50, 0.50, st.session_state.toe_f, 0.01)
        st.session_state.toe_r = st.slider("Схождение зад", -0.50, 0.50, st.session_state.toe_r, 0.01)
    
    with col_right:
        st.header("🔧 LSD")
        st.subheader("Передний дифференциал")
        st.session_state.lsd_init_f = st.slider("Начальный момент (перед)", 5, 40, st.session_state.lsd_init_f)
        st.session_state.lsd_accel_f = st.slider("Ускорение (перед)", 5, 60, st.session_state.lsd_accel_f)
        st.session_state.lsd_brake_f = st.slider("Торможение (перед)", 5, 60, st.session_state.lsd_brake_f)
        
        st.subheader("Задний дифференциал")
        st.session_state.lsd_init_r = st.slider("Начальный момент (зад)", 5, 40, st.session_state.lsd_init_r)
        st.session_state.lsd_accel_r = st.slider("Ускорение (зад)", 5, 60, st.session_state.lsd_accel_r)
        st.session_state.lsd_brake_r = st.slider("Торможение (зад)", 5, 60, st.session_state.lsd_brake_r)
        
        st.header("🌬️ Аэродинамика")
        st.session_state.downforce_f = st.slider("Прижимная сила перед", 0, 400, st.session_state.downforce_f)
        st.session_state.downforce_r = st.slider("Прижимная сила зад", 0, 600, st.session_state.downforce_r)
        
        st.header("⚙️ Трансмиссия")
        st.session_state.max_speed = st.slider("Максимальная скорость (км/ч)", 200, 400, st.session_state.max_speed)
        st.session_state.final_gear = st.slider("Финальная передача", 2.5, 5.5, st.session_state.final_gear, 0.01)
        
        st.header("🛑 Тормоза")
        st.session_state.brake_balance = st.slider("Баланс тормозов", -5, 5, st.session_state.brake_balance)

# ============================================
# TAB: АНАЛИЗ
# ============================================
with tab_analysis:
    st.header("📊 Анализ характеристик")
    
    if selected_car != "Нет данных" and selected_car in CAR_DATABASE:
        car_data = CAR_DATABASE[selected_car]
        
        total_downforce = st.session_state.downforce_f + st.session_state.downforce_r
        pp = calculate_pp(
            car_data.get('weight', 1450) + st.session_state.ballast,
            car_data.get('power', 500) * (st.session_state.power_restrictor / 100),
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
            car_data.get('power', 500) * (st.session_state.power_restrictor / 100),
            car_data.get('weight', 1450) + st.session_state.ballast,
            car_data.get('drive_type', 'FR')
        )
        
        braking = calculate_braking(st.session_state.brake_balance, 
                                    car_data.get('weight', 1450) + st.session_state.ballast, 
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
            st.metric("🎯 Трасса", selected_track[:20])
        
        # Радарная диаграмма
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
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Рекомендации
        st.subheader(f"💡 Рекомендации для трассы: {selected_track}")
        
        if "Monza" in selected_track or "Le Mans" in selected_track:
            st.info("🏁 **Скоростная трасса**: Фокусируйтесь на максимальной скорости. Уменьшите прижимную силу, настройте длинные передачи.")
        elif "Nordschleife" in selected_track or "Nürburgring" in selected_track:
            st.info("🌲 **Сложная трасса**: Нужна стабильная подвеска и хорошая прижимная сила. Увеличьте клиренс.")
        elif "Tokyo" in selected_track:
            st.info("🏙️ **Городская трасса**: Важна точность управления. Сделайте подвеску мягче, настройте точное рулевое.")
        elif "Suzuka" in selected_track or "Fuji" in selected_track:
            st.info("🗻 **Техничная трасса**: Нужен баланс между скоростью и управляемостью.")
        else:
            st.info("✅ Настройки оптимизированы для этой трассы. Двигайте ползунки для точной подстройки.")
        
        # Детальные параметры
        with st.expander("📋 Все текущие настройки"):
            st.json({
                'Трасса': selected_track,
                'Автомобиль': selected_car,
                'PP': pp,
                'Подвеска': {
                    'Высота': f"{st.session_state.height_f}/{st.session_state.height_r} мм",
                    'Пружины': f"{st.session_state.spring_f}/{st.session_state.spring_r} N/mm",
                    'Стабилизаторы': f"{st.session_state.arb_f}/{st.session_state.arb_r}",
                    'Развал': f"{st.session_state.camber_f}°/{st.session_state.camber_r}°",
                    'Схождение': f"{st.session_state.toe_f}°/{st.session_state.toe_r}°"
                },
                'LSD': {
                    'Начальный': f"{st.session_state.lsd_init_f}/{st.session_state.lsd_init_r}",
                    'Ускорение': f"{st.session_state.lsd_accel_f}/{st.session_state.lsd_accel_r}",
                    'Торможение': f"{st.session_state.lsd_brake_f}/{st.session_state.lsd_brake_r}"
                },
                'Аэродинамика': f"{st.session_state.downforce_f}/{st.session_state.downforce_r}",
                'Макс скорость': f"{st.session_state.max_speed} км/ч",
                'Финальная передача': st.session_state.final_gear,
                'Баланс тормозов': st.session_state.brake_balance
            })
    else:
        st.warning("Выберите машину из списка")

st.markdown("---")
st.caption(f"🏎️ GT7 Калькулятор | {len(CAR_DATABASE)} машин | {len(TRACKS)} трасс | Выберите трассу для оптимальных настроек")
