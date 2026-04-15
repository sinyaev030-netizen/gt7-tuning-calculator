import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="GT7 Полный Калькулятор", layout="wide")

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
    
    # Поворачиваемость
    turn_in = round(
        (camber_f - camber_r) * 2 +
        (toe_f - toe_r) * 10 +
        (height_r - height_f) / 20 +
        (arb_f - arb_r) / 10, 1
    )
    turn_in = max(-10, min(10, turn_in))
    
    # Стабильность
    stability = round(
        10 - abs(toe_f + toe_r) * 5 -
        abs(camber_f + camber_r) / 2 -
        abs(height_f - height_r) / 50, 1
    )
    stability = max(0, min(10, stability))
    
    # Сцепление
    grip = round(
        5 + (downforce_f + downforce_r) / 100 +
        (4 - abs(camber_f + camber_r) / 2) -
        abs(spring_f - spring_r) / 10, 1
    )
    grip = max(1, min(10, grip))
    
    # Отклик подвески
    response = round(
        (spring_f + spring_r) / 2 +
        (100 - (height_f + height_r) / 2) / 20, 1
    )
    response = max(1, min(10, response))
    
    return {
        'turn_in': turn_in,
        'stability': stability,
        'grip': grip,
        'response': response
    }

def calculate_acceleration(lsd_accel, lsd_init, power, weight, drive_type):
    power_to_weight = power / weight if weight > 0 else 0
    lsd_bonus = (lsd_accel + lsd_init) / 20
    drive_bonus = 1.2 if drive_type == "4WD" else 1.0
    return round((power_to_weight * 10 + lsd_bonus) * drive_bonus, 1)

def calculate_braking(brake_balance, weight, downforce):
    brake_power = (weight / 1000) * 10 + downforce / 100
    balance_effect = brake_balance / 10
    return round(brake_power * (1 + balance_effect), 1)

def calculate_top_speed(power, downforce, final_gear, max_speed_setting):
    base_speed = power / 10
    drag_penalty = downforce / 50
    gear_penalty = final_gear * 10
    return round(base_speed - drag_penalty - gear_penalty + max_speed_setting / 2, 1)

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 ПОЛНЫЙ ТЮНИНГ КАЛЬКУЛЯТОР")
st.markdown(f"📊 В базе данных: **{len(CAR_DATABASE)}** машин")

# Инициализация переменных сессии
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = CAR_NAMES[0] if CAR_NAMES else ""

# ============================================
# БОКОВАЯ ПАНЕЛЬ - ВЫБОР МАШИНЫ
# ============================================
with st.sidebar:
    st.header("🏁 Выбор автомобиля")
    
    selected_car = st.selectbox("Модель", CAR_NAMES, key="car_select")
    st.session_state.selected_car = selected_car
    
    if selected_car != "Нет данных" and selected_car in CAR_DATABASE:
        car_data = CAR_DATABASE[selected_car]
        st.metric("📊 Базовый PP", car_data.get('pp', 0))
        st.metric("⚡ Мощность", f"{car_data.get('power', 0):.0f} л.с.")
        st.metric("⚖️ Вес", f"{car_data.get('weight', 0):.0f} кг")
        st.metric("🔧 Привод", car_data.get('drive_type', '?'))
    
    st.markdown("---")
    st.caption("Настройте параметры в основных вкладках")

# ============================================
# ОСНОВНЫЕ ВКЛАДКИ
# ============================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏗️ ПОДВЕСКА", 
    "🔧 LSD / ДИФФЕРЕНЦИАЛ", 
    "🌬️ АЭРОДИНАМИКА",
    "⚙️ ТРАНСМИССИЯ",
    "🛑 ТОРМОЗА / ДВИГАТЕЛЬ",
    "📊 АНАЛИЗ"
])

# ============================================
# TAB 1: ПОДВЕСКА
# ============================================
with tab1:
    st.header("🏗️ Настройки подвески")
    st.caption("Влияют на устойчивость, поворачиваемость и комфорт управления")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Высота подвески")
        height_f = st.slider("Высота перед (мм)", 60, 150, 75, key="height_f")
        height_r = st.slider("Высота зад (мм)", 60, 150, 80, key="height_r")
        
        st.subheader("Жесткость пружин")
        spring_f = st.slider("Пружины перед (N/mm)", 2.0, 6.0, 4.5, 0.1, key="spring_f")
        spring_r = st.slider("Пружины зад (N/mm)", 2.0, 6.0, 4.8, 0.1, key="spring_r")
        
        st.subheader("Стабилизаторы")
        arb_f = st.slider("Стабилизатор перед", 1, 10, 4, key="arb_f")
        arb_r = st.slider("Стабилизатор зад", 1, 10, 5, key="arb_r")
    
    with col2:
        st.subheader("Демпферы (сжатие)")
        comp_f = st.slider("Сжатие перед", 20, 60, 28, key="comp_f")
        comp_r = st.slider("Сжатие зад", 20, 60, 30, key="comp_r")
        
        st.subheader("Демпферы (отбой)")
        ext_f = st.slider("Отбой перед", 20, 60, 40, key="ext_f")
        ext_r = st.slider("Отбой зад", 20, 60, 42, key="ext_r")
        
        st.subheader("Частота")
        freq_f = st.slider("Частота перед (Гц)", 1.5, 4.0, 2.2, 0.1, key="freq_f")
        freq_r = st.slider("Частота зад (Гц)", 1.5, 4.0, 2.0, 0.1, key="freq_r")

# ============================================
# TAB 2: УГЛЫ КОЛЁС
# ============================================
with tab2:
    st.header("🔧 Углы установки колёс")
    st.caption("Влияют на поворачиваемость, износ шин и устойчивость")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Развал (Camber)")
        camber_f = st.slider("Развал перед (°)", -3.5, 0.0, -2.0, 0.1, key="camber_f")
        camber_r = st.slider("Развал зад (°)", -3.0, 0.0, -1.5, 0.1, key="camber_r")
        
        st.subheader("Схождение (Toe)")
        toe_f = st.slider("Схождение перед", -0.50, 0.50, 0.10, 0.01, key="toe_f")
        toe_r = st.slider("Схождение зад", -0.50, 0.50, 0.20, 0.01, key="toe_r")
    
    with col2:
        st.subheader("🔧 Дифференциал (LSD)")
        st.info("Настройка переднего и заднего дифференциала")
        
        lsd_init_f = st.slider("LSD начальный момент (перед)", 5, 40, 8, key="lsd_init_f")
        lsd_init_r = st.slider("LSD начальный момент (зад)", 5, 40, 15, key="lsd_init_r")
        
        lsd_accel_f = st.slider("LSD ускорение (перед)", 5, 60, 20, key="lsd_accel_f")
        lsd_accel_r = st.slider("LSD ускорение (зад)", 5, 60, 25, key="lsd_accel_r")
        
        lsd_brake_f = st.slider("LSD торможение (перед)", 5, 60, 10, key="lsd_brake_f")
        lsd_brake_r = st.slider("LSD торможение (зад)", 5, 60, 15, key="lsd_brake_r")

# ============================================
# TAB 3: АЭРОДИНАМИКА
# ============================================
with tab3:
    st.header("🌬️ Аэродинамика")
    st.caption("Влияет на прижимную силу, скорость и устойчивость в поворотах")
    
    col1, col2 = st.columns(2)
    
    with col1:
        downforce_f = st.slider("Прижимная сила перед", 0, 400, 120, key="downforce_f")
        downforce_r = st.slider("Прижимная сила зад", 0, 600, 280, key="downforce_r")
        
        total_downforce = downforce_f + downforce_r
        st.metric("📊 Общая прижимная сила", f"{total_downforce}")
        
        if total_downforce < 100:
            st.warning("⚠️ Маленькая прижимная сила - машина будет неустойчива в поворотах")
        elif total_downforce > 400:
            st.success("✅ Высокая прижимная сила - отличная устойчивость")
    
    with col2:
        st.subheader("Баланс аэродинамики")
        balance_ratio = downforce_f / (downforce_r + 0.01)
        
        if balance_ratio < 0.3:
            st.info("📉 Баланс смещён назад - больше сцепления задней оси")
        elif balance_ratio > 0.5:
            st.info("📈 Баланс смещён вперёд - больше сцепления передней оси")
        else:
            st.success("⚖️ Сбалансированная аэродинамика")

# ============================================
# TAB 4: ТРАНСМИССИЯ
# ============================================
with tab4:
    st.header("⚙️ Настройки трансмиссии")
    st.caption("Влияют на разгон, максимальную скорость и поведение в поворотах")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_speed = st.slider("Максимальная скорость (км/ч)", 200, 450, 290, key="max_speed")
        final_gear = st.slider("Финальная передача", 2.5, 5.5, 4.730, 0.01, key="final_gear")
        
        st.subheader("Передачи")
        gear1 = st.number_input("1-я передача", 1.5, 4.0, 2.569, 0.01, key="gear1")
        gear2 = st.number_input("2-я передача", 1.0, 3.0, 1.828, 0.01, key="gear2")
        gear3 = st.number_input("3-я передача", 0.8, 2.5, 1.380, 0.01, key="gear3")
    
    with col2:
        gear4 = st.number_input("4-я передача", 0.6, 2.0, 1.087, 0.01, key="gear4")
        gear5 = st.number_input("5-я передача", 0.5, 1.5, 0.895, 0.01, key="gear5")
        gear6 = st.number_input("6-я передача", 0.4, 1.2, 0.770, 0.01, key="gear6")
        gear7 = st.number_input("7-я передача", 0.3, 1.0, 0.650, 0.01, key="gear7")
        gear8 = st.number_input("8-я передача", 0.3, 0.9, 0.550, 0.01, key="gear8")

# ============================================
# TAB 5: ТОРМОЗА / ДВИГАТЕЛЬ
# ============================================
with tab5:
    st.header("🛑 Тормозная система")
    
    col1, col2 = st.columns(2)
    
    with col1:
        brake_balance = st.slider("Баланс тормозов (перед/зад)", -5, 5, -2, key="brake_balance")
        
        if brake_balance < 0:
            st.info("🔴 Тормоза смещены назад - устойчивость при торможении")
        elif brake_balance > 0:
            st.info("🟡 Тормоза смещены вперёд - более резкое торможение")
        else:
            st.info("⚖️ Сбалансированные тормоза")
    
    with col2:
        st.subheader("Дополнительные параметры")
        power_restrictor = st.slider("Ограничитель мощности (%)", 70, 100, 100, key="power_restrictor")
        ballast = st.slider("Балласт (кг)", 0, 200, 0, key="ballast")
        ballast_pos = st.slider("Позиция балласта (%)", -50, 50, 0, key="ballast_pos")

# ============================================
# TAB 6: АНАЛИЗ
# ============================================
with tab6:
    st.header("📊 Анализ характеристик")
    
    if selected_car != "Нет данных" and selected_car in CAR_DATABASE:
        car_data = CAR_DATABASE[selected_car]
        
        # Расчёты
        total_downforce = downforce_f + downforce_r
        pp = calculate_pp(
            car_data.get('weight', 1450) + ballast,
            car_data.get('power', 500) * (power_restrictor / 100),
            total_downforce,
            car_data.get('drive_type', 'FR')
        )
        
        handling = calculate_handling(
            camber_f, camber_r, toe_f, toe_r, height_f, height_r,
            spring_f, spring_r, arb_f, arb_r, downforce_f, downforce_r
        )
        
        acceleration = calculate_acceleration(
            lsd_accel_r, lsd_init_r,
            car_data.get('power', 500) * (power_restrictor / 100),
            car_data.get('weight', 1450) + ballast,
            car_data.get('drive_type', 'FR')
        )
        
        braking = calculate_braking(brake_balance, car_data.get('weight', 1450) + ballast, total_downforce)
        top_speed = calculate_top_speed(car_data.get('power', 500), total_downforce, final_gear, max_speed)
        
        # Метрики
        st.subheader("🏁 Итоговые характеристики")
        
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
            st.metric("💨 Макс скорость", f"{top_speed:.0f} км/ч")
        
        # Радарная диаграмма
        st.subheader("📈 Визуализация характеристик")
        
        categories = ['Ускорение', 'Поворачиваемость', 'Стабильность', 'Сцепление', 'Торможение', 'Отклик']
        values = [
            min(acceleration, 10),
            handling['turn_in'] + 5,
            handling['stability'],
            handling['grip'],
            min(braking / 10, 10),
            handling['response']
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_car[:30]
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Рекомендации
        st.subheader("💡 Рекомендации по настройке")
        
        recommendations = []
        
        if handling['stability'] < 5:
            recommendations.append("⚠️ **Низкая стабильность** → уменьшите высоту подвески или увеличьте жесткость пружин")
        if handling['turn_in'] < -2:
            recommendations.append("⚠️ **Недостаточная поворачиваемость** → увеличьте задний стабилизатор или уменьшите передний")
        elif handling['turn_in'] > 2:
            recommendations.append("⚠️ **Избыточная поворачиваемость** → уменьшите задний стабилизатор или увеличьте передний")
        if total_downforce < 150:
            recommendations.append("💨 **Маленькая прижимная сила** → увеличьте аэродинамику для лучшей устойчивости")
        if handling['grip'] >= 8:
            recommendations.append("✅ **Отличное сцепление** → машина уверенно держит дорогу")
        if acceleration >= 8:
            recommendations.append("🚀 **Отличный разгон** → эффективная работа LSD")
        if ballast > 50:
            recommendations.append("⚖️ **Большой балласт** → машина стала тяжелее, что влияет на ускорение")
        
        if not recommendations:
            recommendations.append("✅ **Отличный баланс!** Настройки оптимальны для большинства трасс")
        
        for rec in recommendations:
            st.write(rec)
        
        # Детальные параметры
        with st.expander("📋 Детальные параметры"):
            st.json({
                'Машина': selected_car,
                'PP': pp,
                'Подвеска': {
                    'Высота': f"{height_f}/{height_r} мм",
                    'Пружины': f"{spring_f}/{spring_r} N/mm",
                    'Стабилизаторы': f"{arb_f}/{arb_r}",
                    'Развал': f"{camber_f}°/{camber_r}°",
                    'Схождение': f"{toe_f}°/{toe_r}°"
                },
                'LSD': {
                    'Начальный': f"{lsd_init_f}/{lsd_init_r}",
                    'Ускорение': f"{lsd_accel_f}/{lsd_accel_r}",
                    'Торможение': f"{lsd_brake_f}/{lsd_brake_r}"
                },
                'Аэродинамика': {
                    'Прижимная сила': f"{downforce_f}/{downforce_r}",
                    'Всего': total_downforce
                },
                'Трансмиссия': {
                    'Макс скорость': f"{max_speed} км/ч",
                    'Финальная передача': final_gear
                }
            })
    else:
        st.warning("Выберите машину из списка в боковой панели")

st.markdown("---")
st.caption(f"🏎️ GT7 ПОЛНЫЙ КАЛЬКУЛЯТОР | База: {len(CAR_DATABASE)} машин | Все параметры тюнинга")