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
    "Япония Autopolis International Racing Course - укороченная",
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
# НАСТРОЙКИ ПО УМОЛЧАНИЮ
# ============================================

DEFAULT_SETTINGS = {
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

# ============================================
# БАЗА ДАННЫХ ТРАСС С НАСТРОЙКАМИ
# ============================================

TRACK_SETTINGS = {
    # Alsace - извилистые сельские дороги
    "Франция Alsace - Деревня": {"height_f": 74, "height_r": 79, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 190, "downforce_r": 360, "max_speed": 270, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    "Франция Alsace - Деревня (обратн.)": {"height_f": 74, "height_r": 79, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 190, "downforce_r": 360, "max_speed": 270, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    "Франция Alsace - тестовая трасса": {"height_f": 73, "height_r": 78, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 200, "downforce_r": 380, "max_speed": 275, "final_gear": 4.25, "brake_balance": -2, "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 25},
    "Франция Alsace - тестовая трасса (обратн.)": {"height_f": 73, "height_r": 78, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 200, "downforce_r": 380, "max_speed": 275, "final_gear": 4.25, "brake_balance": -2, "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 25},
    
    # Lago Maggiore - техничные трассы
    "Италия Autodrome Lago Maggiore - Восток": {"height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 280, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    "Италия Autodrome Lago Maggiore - Восток (обратн.)": {"height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 280, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    "Италия Autodrome Lago Maggiore - Запад": {"height_f": 69, "height_r": 73, "spring_f": 4.7, "spring_r": 5.1, "downforce_f": 210, "downforce_r": 400, "max_speed": 285, "final_gear": 4.05, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Италия Autodrome Lago Maggiore - Запад (обратн.)": {"height_f": 69, "height_r": 73, "spring_f": 4.7, "spring_r": 5.1, "downforce_f": 210, "downforce_r": 400, "max_speed": 285, "final_gear": 4.05, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Италия Autodrome Lago Maggiore - Центр": {"height_f": 68, "height_r": 72, "spring_f": 4.8, "spring_r": 5.2, "downforce_f": 220, "downforce_r": 420, "max_speed": 290, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 28},
    "Италия Autodrome Lago Maggiore - Центр (обратн.)": {"height_f": 68, "height_r": 72, "spring_f": 4.8, "spring_r": 5.2, "downforce_f": 220, "downforce_r": 420, "max_speed": 290, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 28},
    "Италия Autodrome Lago Maggiore - полная трасса": {"height_f": 67, "height_r": 71, "spring_f": 4.9, "spring_r": 5.3, "downforce_f": 230, "downforce_r": 440, "max_speed": 295, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.9, "toe_f": 0.14, "toe_r": 0.24, "lsd_init_r": 17, "lsd_accel_r": 29},
    "Италия Autodrome Lago Maggiore - полная трасса (обратн.)": {"height_f": 67, "height_r": 71, "spring_f": 4.9, "spring_r": 5.3, "downforce_f": 230, "downforce_r": 440, "max_speed": 295, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.9, "toe_f": 0.14, "toe_r": 0.24, "lsd_init_r": 17, "lsd_accel_r": 29},
    
    # Monza - скоростные
    "Италия Autodromo Nazionale Monza": {"height_f": 63, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4, "downforce_f": 140, "downforce_r": 280, "max_speed": 330, "final_gear": 3.60, "brake_balance": -3, "camber_f": -2.6, "camber_r": -1.9, "toe_f": 0.18, "toe_r": 0.28, "lsd_init_r": 18, "lsd_accel_r": 30},
    "Италия Autodromo Nazionale Monza (без шиканы)": {"height_f": 62, "height_r": 67, "spring_f": 5.1, "spring_r": 5.5, "downforce_f": 130, "downforce_r": 260, "max_speed": 340, "final_gear": 3.55, "brake_balance": -3, "camber_f": -2.7, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30, "lsd_init_r": 19, "lsd_accel_r": 32},
    
    # Interlagos
    "Бразилия Autódromo de Interlagos": {"height_f": 69, "height_r": 73, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 290, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Autopolis
    "Япония Autopolis International Racing Course": {"height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 210, "downforce_r": 400, "max_speed": 285, "final_gear": 4.05, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Япония Autopolis International Racing Course - укороченная": {"height_f": 71, "height_r": 75, "spring_f": 4.5, "spring_r": 4.9, "downforce_f": 200, "downforce_r": 380, "max_speed": 280, "final_gear": 4.15, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Blue Moon Bay
    "США Blue Moon Bay Speedway - внутренняя A": {"height_f": 66, "height_r": 70, "spring_f": 4.8, "spring_r": 5.2, "downforce_f": 160, "downforce_r": 320, "max_speed": 310, "final_gear": 3.80, "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.14, "toe_r": 0.24, "lsd_init_r": 17, "lsd_accel_r": 28},
    
    # Brands Hatch
    "Великобритания Brands Hatch - Grand Prix Circuit": {"height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 280, "final_gear": 4.20, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 15, "lsd_accel_r": 26},
    "Великобритания Brands Hatch - Indy Circuit": {"height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 200, "downforce_r": 380, "max_speed": 260, "final_gear": 4.40, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Circuit Gilles-Villeneuve
    "Канада Circuit Gilles-Villeneuve": {"height_f": 67, "height_r": 71, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 300, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Barcelona
    "Испания Circuit de Barcelona-Catalunya (GP)": {"height_f": 68, "height_r": 72, "spring_f": 4.7, "spring_r": 5.1, "downforce_f": 210, "downforce_r": 400, "max_speed": 295, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Sainte-Croix
    "Франция Circuit de Sainte-Croix - A": {"height_f": 71, "height_r": 75, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 200, "downforce_r": 380, "max_speed": 285, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    "Франция Circuit de Sainte-Croix - B": {"height_f": 70, "height_r": 74, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 290, "final_gear": 4.05, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Франция Circuit de Sainte-Croix - C": {"height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 220, "downforce_r": 420, "max_speed": 295, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 17, "lsd_accel_r": 28},
    
    # Spa
    "Бельгия Spa (24 часа)": {"height_f": 68, "height_r": 72, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 300, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Daytona
    "США Daytona - дорожная": {"height_f": 64, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4, "downforce_f": 140, "downforce_r": 280, "max_speed": 330, "final_gear": 3.60, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26, "lsd_init_r": 17, "lsd_accel_r": 28},
    
    # Deep Forest
    "Швейцария Deep Forest Raceway": {"height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 200, "downforce_r": 380, "max_speed": 275, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Dragon Trail
    "Хорватия Dragon Trail - Побережье": {"height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 210, "downforce_r": 400, "max_speed": 290, "final_gear": 4.05, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Хорватия Dragon Trail - Сады": {"height_f": 71, "height_r": 76, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 200, "downforce_r": 380, "max_speed": 280, "final_gear": 4.20, "brake_balance": -2, "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 25},
    
    # Eiger Nordwand
    "Швейцария Eiger Nordwand": {"height_f": 73, "height_r": 78, "spring_f": 4.2, "spring_r": 4.5, "downforce_f": 200, "downforce_r": 380, "max_speed": 265, "final_gear": 4.40, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Fuji
    "Япония Fuji International Speedway": {"height_f": 67, "height_r": 71, "spring_f": 4.7, "spring_r": 5.1, "downforce_f": 190, "downforce_r": 360, "max_speed": 310, "final_gear": 3.80, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Grand Valley
    "США Grand Valley - шоссе №1": {"height_f": 70, "height_r": 74, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 200, "downforce_r": 380, "max_speed": 285, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Le Mans
    "Франция Le Mans (24 часа)": {"height_f": 60, "height_r": 65, "spring_f": 5.2, "spring_r": 5.6, "downforce_f": 120, "downforce_r": 250, "max_speed": 360, "final_gear": 3.40, "brake_balance": -3, "camber_f": -2.8, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30, "lsd_init_r": 20, "lsd_accel_r": 35},
    
    # High Speed Ring
    "Япония High Speed Ring": {"height_f": 65, "height_r": 70, "spring_f": 5.0, "spring_r": 5.4, "downforce_f": 130, "downforce_r": 260, "max_speed": 340, "final_gear": 3.50, "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.15, "toe_r": 0.25, "lsd_init_r": 17, "lsd_accel_r": 28},
    
    # Kyoto
    "Япония Kyoto Driving Park - Yamagiwa": {"height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 190, "downforce_r": 360, "max_speed": 270, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Road Atlanta
    "США Michelin Raceway Road Atlanta": {"height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 210, "downforce_r": 400, "max_speed": 295, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Mount Panorama
    "Австралия Mount Panorama": {"height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Nürburgring
    "Германия Nürburgring (24 часа)": {"height_f": 71, "height_r": 76, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 220, "downforce_r": 420, "max_speed": 285, "final_gear": 4.15, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 25},
    "Германия Nürburgring GP": {"height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 210, "downforce_r": 400, "max_speed": 295, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    "Германия Nürburgring Nordschleife": {"height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5, "downforce_f": 230, "downforce_r": 440, "max_speed": 280, "final_gear": 4.20, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Red Bull Ring
    "Австрия Red Bull Ring": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Sardegna
    "Италия Sardegna - Road Track - A": {"height_f": 73, "height_r": 78, "spring_f": 4.3, "spring_r": 4.6, "downforce_f": 190, "downforce_r": 360, "max_speed": 270, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    "Италия Sardegna - Road Track - B": {"height_f": 72, "height_r": 77, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 200, "downforce_r": 380, "max_speed": 275, "final_gear": 4.25, "brake_balance": -2, "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 15, "lsd_accel_r": 25},
    "Италия Sardegna - Road Track - C": {"height_f": 71, "height_r": 76, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 280, "final_gear": 4.20, "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 16, "lsd_accel_r": 26},
    
    # Suzuka
    "Япония Suzuka Circuit": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.00, "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 15, "lsd_accel_r": 26},
    
    # Tokyo Expressway
    "Япония Tokyo Expressway - Центр": {"height_f": 74, "height_r": 79, "spring_f": 4.0, "spring_r": 4.3, "downforce_f": 160, "downforce_r": 320, "max_speed": 270, "final_gear": 4.50, "brake_balance": -1, "camber_f": -1.8, "camber_r": -1.3, "toe_f": 0.05, "toe_r": 0.15, "lsd_init_r": 13, "lsd_accel_r": 23},
    
    # Trial Mountain
    "США Trial Mountain Circuit": {"height_f": 74, "height_r": 79, "spring_f": 4.2, "spring_r": 4.5, "downforce_f": 190, "downforce_r": 360, "max_speed": 285, "final_gear": 4.15, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Tsukuba
    "Япония Tsukuba Circuit": {"height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5, "downforce_f": 200, "downforce_r": 380, "max_speed": 260, "final_gear": 4.40, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24},
    
    # Watkins Glen
    "США Watkins Glen": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 190, "downforce_r": 360, "max_speed": 300, "final_gear": 3.90, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
    
    # Laguna Seca
    "США WeatherTech Raceway Laguna Seca": {"height_f": 70, "height_r": 75, "spring_f": 4.4, "spring_r": 4.7, "downforce_f": 220, "downforce_r": 420, "max_speed": 270, "final_gear": 4.30, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.10, "toe_r": 0.20, "lsd_init_r": 14, "lsd_accel_r": 25},
    
    # Willow Springs
    "США Willow Springs - Big Willow": {"height_f": 65, "height_r": 69, "spring_f": 4.9, "spring_r": 5.3, "downforce_f": 160, "downforce_r": 320, "max_speed": 310, "final_gear": 3.75, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26, "lsd_init_r": 17, "lsd_accel_r": 28},
    
    # Yas Marina
    "ОАЭ Yas Marina Circuit": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 300, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27},
}

# ============================================
# ТОП-5 МАШИН ДЛЯ КАЖДОЙ ТРАССЫ С НАСТРОЙКАМИ
# ============================================

TOP_CARS_DATABASE_DATABASE = {
    # ========== ФРАНЦИЯ ALSACE ==========
    "Франция Alsace - Деревня": {
        "TOP_CARS_DATABASE": [
            "Alpine A110 '17",
            "Renault Sport Mégane R.S. Trophy '11",
            "Peugeot RCZ Gr.4",
            "Renault Clio R.S. 220 EDC Trophy '15",
            "Alpine A110 1600S '72"
        ],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 5, "arb_r": 5, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 270, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    "Франция Alsace - Деревня (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Alpine A110 '17",
            "Renault Sport Mégane R.S. Trophy '11",
            "Peugeot RCZ Gr.4",
            "Renault Clio R.S. 220 EDC Trophy '15",
            "Alpine A110 1600S '72"
        ],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 5, "arb_r": 5, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 270, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    "Франция Alsace - тестовая трасса": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 73, "height_r": 78, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 275, "final_gear": 4.25, "brake_balance": -2,
            "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 25
        }
    },
    "Франция Alsace - тестовая трасса (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 73, "height_r": 78, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 275, "final_gear": 4.25, "brake_balance": -2,
            "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 25
        }
    },

    # ========== LAGO MAGGIORE ==========
    "Италия Autodrome Lago Maggiore - Восток": {
        "TOP_CARS_DATABASE": [
            "Ferrari 458 Italia GT3 '13",
            "Porsche 911 GT3 R '19",
            "McLaren 650S GT3 '15",
            "Nissan GT-R Nismo GT3 '18",
            "Audi R8 LMS '15"
        ],
        "settings": {
            "height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 280, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    "Италия Autodrome Lago Maggiore - Восток (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Ferrari 458 Italia GT3 '13",
            "Porsche 911 GT3 R '19",
            "McLaren 650S GT3 '15",
            "Nissan GT-R Nismo GT3 '18",
            "Audi R8 LMS '15"
        ],
        "settings": {
            "height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 280, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    "Италия Autodrome Lago Maggiore - Запад": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "BMW M6 GT3 '16",
            "Audi R8 LMS Evo '19",
            "Ferrari 488 GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.7, "spring_r": 5.1,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 285, "final_gear": 4.05, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Италия Autodrome Lago Maggiore - Запад (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "BMW M6 GT3 '16",
            "Audi R8 LMS Evo '19",
            "Ferrari 488 GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.7, "spring_r": 5.1,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 285, "final_gear": 4.05, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Италия Autodrome Lago Maggiore - Центр": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Nissan GT-R Nismo GT3 '18",
            "Audi R8 LMS Evo '19"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.8, "spring_r": 5.2,
            "arb_f": 5, "arb_r": 6, "downforce_f": 220, "downforce_r": 420,
            "max_speed": 290, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 28
        }
    },
    "Италия Autodrome Lago Maggiore - Центр (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Nissan GT-R Nismo GT3 '18",
            "Audi R8 LMS Evo '19"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.8, "spring_r": 5.2,
            "arb_f": 5, "arb_r": 6, "downforce_f": 220, "downforce_r": 420,
            "max_speed": 290, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 28
        }
    },
    "Италия Autodrome Lago Maggiore - полная трасса": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Mercedes-AMG GT3 '20",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Audi R8 LMS Evo '19"
        ],
        "settings": {
            "height_f": 67, "height_r": 71, "spring_f": 4.9, "spring_r": 5.3,
            "arb_f": 5, "arb_r": 6, "downforce_f": 230, "downforce_r": 440,
            "max_speed": 295, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.5, "camber_r": -1.9, "toe_f": 0.14, "toe_r": 0.24,
            "lsd_init_r": 17, "lsd_accel_r": 29
        }
    },
    "Италия Autodrome Lago Maggiore - полная трасса (обратн.)": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Mercedes-AMG GT3 '20",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Audi R8 LMS Evo '19"
        ],
        "settings": {
            "height_f": 67, "height_r": 71, "spring_f": 4.9, "spring_r": 5.3,
            "arb_f": 5, "arb_r": 6, "downforce_f": 230, "downforce_r": 440,
            "max_speed": 295, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.5, "camber_r": -1.9, "toe_f": 0.14, "toe_r": 0.24,
            "lsd_init_r": 17, "lsd_accel_r": 29
        }
    },

    # ========== MONZA ==========
    "Италия Autodromo Nazionale Monza": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 458 Italia GT3 '13",
            "McLaren 720S GT3 '23",
            "Nissan GT-R Nismo GT3 '18",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": {
            "height_f": 63, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7, "downforce_f": 140, "downforce_r": 280,
            "max_speed": 330, "final_gear": 3.60, "brake_balance": -3,
            "camber_f": -2.6, "camber_r": -1.9, "toe_f": 0.18, "toe_r": 0.28,
            "lsd_init_r": 18, "lsd_accel_r": 30
        }
    },
    "Италия Autodromo Nazionale Monza (без шиканы)": {
        "TOP_CARS_DATABASE": [
            "Porsche 919 Hybrid '16",
            "Toyota TS050 Hybrid '16",
            "Audi R18 '16",
            "Bugatti Vision GT",
            "McLaren Ultimate Vision GT"
        ],
        "settings": {
            "height_f": 62, "height_r": 67, "spring_f": 5.1, "spring_r": 5.5,
            "arb_f": 6, "arb_r": 7, "downforce_f": 130, "downforce_r": 260,
            "max_speed": 340, "final_gear": 3.55, "brake_balance": -3,
            "camber_f": -2.7, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30,
            "lsd_init_r": 19, "lsd_accel_r": 32
        }
    },

    # ========== INTERLAGOS ==========
    "Бразилия Autódromo de Interlagos": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "BMW M6 GT3 '16",
            "Audi R8 LMS '15"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 5, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 290, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== AUTOPOLIS ==========
    "Япония Autopolis International Racing Course": {
        "TOP_CARS_DATABASE": [
            "Honda NSX GT500 '16",
            "Nissan GT-R GT500 '16",
            "Toyota Supra GT500 '97",
            "Lexus RC F GT500 '16",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 70, "height_r": 74, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 285, "final_gear": 4.05, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Япония Autopolis International Racing Course - укороченная": {
        "TOP_CARS_DATABASE": [
            "Honda NSX '17",
            "Nissan GT-R '17",
            "Toyota GR Supra RZ '19",
            "Subaru WRX STI Type S '14",
            "Mazda RX-7 Spirit R '02"
        ],
        "settings": {
            "height_f": 71, "height_r": 75, "spring_f": 4.5, "spring_r": 4.9,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 280, "final_gear": 4.15, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== BLUE MOON BAY ==========
    "США Blue Moon Bay Speedway - внутренняя A": {
        "TOP_CARS_DATABASE": [
            "Ford GT LM Race Car",
            "Chevrolet Corvette C7 Gr.3",
            "Dodge Viper SRT GT3-R '15",
            "Nissan GT-R Nismo GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 66, "height_r": 70, "spring_f": 4.8, "spring_r": 5.2,
            "arb_f": 6, "arb_r": 6, "downforce_f": 160, "downforce_r": 320,
            "max_speed": 310, "final_gear": 3.80, "brake_balance": -2,
            "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.14, "toe_r": 0.24,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },

    # ========== BRANDS HATCH ==========
    "Великобритания Brands Hatch - Grand Prix Circuit": {
        "TOP_CARS_DATABASE": [
            "Aston Martin Vantage GT3 '12",
            "McLaren 650S GT3 '15",
            "BMW M6 GT3 '16",
            "Ferrari 488 GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 5, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 280, "final_gear": 4.20, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    "Великобритания Brands Hatch - Indy Circuit": {
        "TOP_CARS_DATABASE": [
            "Honda Civic Type R (FK8) '20",
            "Renault Sport Mégane R.S. Trophy '11",
            "Peugeot RCZ Gr.4",
            "Ford Focus RS '18",
            "Volkswagen Golf VII GTI '14"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 4, "arb_r": 4, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 260, "final_gear": 4.40, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== CIRCUIT GILLES-VILLENEUVE ==========
    "Канада Circuit Gilles-Villeneuve": {
        "TOP_CARS_DATABASE": [
            "McLaren 720S GT3 '19",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 67, "height_r": 71, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 300, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== BARCELONA ==========
    "Испания Circuit de Barcelona-Catalunya (GP)": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.7, "spring_r": 5.1,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 295, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== SAINTE-CROIX ==========
    "Франция Circuit de Sainte-Croix - A": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Audi R8 LMS '15",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": {
            "height_f": 71, "height_r": 75, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 285, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    "Франция Circuit de Sainte-Croix - B": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Nissan GT-R Nismo GT3 '18",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": {
            "height_f": 70, "height_r": 74, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 290, "final_gear": 4.05, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Франция Circuit de Sainte-Croix - C": {
        "TOP_CARS_DATABASE": [
            "Porsche 919 Hybrid '16",
            "Toyota TS050 Hybrid '16",
            "Audi R18 '16",
            "McLaren Ultimate Vision GT",
            "Bugatti Vision GT"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 220, "downforce_r": 420,
            "max_speed": 295, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },

    # ========== SPA ==========
    "Бельгия Spa (24 часа)": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Audi R8 LMS '15",
            "McLaren 720S GT3 '19",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 300, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== DAYTONA ==========
    "США Daytona - дорожная": {
        "TOP_CARS_DATABASE": [
            "Ford GT LM Race Car",
            "Chevrolet Corvette C7 Gr.3",
            "Dodge Viper SRT GT3-R '15",
            "Nissan GT-R Nismo GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 64, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7, "downforce_f": 140, "downforce_r": 280,
            "max_speed": 330, "final_gear": 3.60, "brake_balance": -2,
            "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },

    # ========== DEEP FOREST ==========
    "Швейцария Deep Forest Raceway": {
        "TOP_CARS_DATABASE": [
            "Mazda RX-7 Spirit R '02",
            "Honda NSX Type R '92",
            "Nissan Skyline GT-R V-spec II '94",
            "Toyota Supra RZ '97",
            "Subaru Impreza 22B-STi '98"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 4, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 275, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== DRAGON TRAIL ==========
    "Хорватия Dragon Trail - Побережье": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 290, "final_gear": 4.05, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Хорватия Dragon Trail - Сады": {
        "TOP_CARS_DATABASE": [
            "Mazda RX-7 Spirit R '02",
            "Nissan Skyline GT-R V-spec II '94",
            "Toyota Supra RZ '97",
            "Honda NSX Type R '92",
            "Porsche 911 Carrera RS (993) '95"
        ],
        "settings": {
            "height_f": 71, "height_r": 76, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 4, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 280, "final_gear": 4.20, "brake_balance": -2,
            "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 25
        }
    },

    # ========== EIGER NORDWAND ==========
    "Швейцария Eiger Nordwand": {
        "TOP_CARS_DATABASE": [
            "Alpine A110 '17",
            "Renault Sport Mégane R.S. Trophy '11",
            "Peugeot RCZ Gr.4",
            "Ford Focus RS '18",
            "Volkswagen Golf VII GTI '14"
        ],
        "settings": {
            "height_f": 73, "height_r": 78, "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 4, "arb_r": 4, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 265, "final_gear": 4.40, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== FUJI ==========
    "Япония Fuji International Speedway": {
        "TOP_CARS_DATABASE": [
            "Toyota Supra GT500 '97",
            "Nissan GT-R GT500 '08",
            "Honda NSX GT500 '08",
            "Lexus RC F GT500 '16",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 67, "height_r": 71, "spring_f": 4.7, "spring_r": 5.1,
            "arb_f": 5, "arb_r": 6, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 310, "final_gear": 3.80, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== GRAND VALLEY ==========
    "США Grand Valley - шоссе №1": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Mercedes-AMG GT3 '20",
            "Nissan GT-R Nismo GT3 '18"
        ],
        "settings": {
            "height_f": 70, "height_r": 74, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 285, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== LE MANS ==========
    "Франция Le Mans (24 часа)": {
        "TOP_CARS_DATABASE": [
            "Porsche 919 Hybrid '16",
            "Toyota TS050 Hybrid '16",
            "Audi R18 '16",
            "Bugatti Vision GT",
            "Peugeot 908 HDi FAP '10"
        ],
        "settings": {
            "height_f": 60, "height_r": 65, "spring_f": 5.2, "spring_r": 5.6,
            "arb_f": 6, "arb_r": 7, "downforce_f": 120, "downforce_r": 250,
            "max_speed": 360, "final_gear": 3.40, "brake_balance": -3,
            "camber_f": -2.8, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30,
            "lsd_init_r": 20, "lsd_accel_r": 35
        }
    },

    # ========== HIGH SPEED RING ==========
    "Япония High Speed Ring": {
        "TOP_CARS_DATABASE": [
            "Nissan GT-R Nismo '17",
            "Porsche 911 Turbo S '20",
            "Ferrari F8 Tributo '19",
            "McLaren 720S '17",
            "Lamborghini Huracan LP 610-4 '15"
        ],
        "settings": {
            "height_f": 65, "height_r": 70, "spring_f": 5.0, "spring_r": 5.4,
            "arb_f": 6, "arb_r": 7, "downforce_f": 130, "downforce_r": 260,
            "max_speed": 340, "final_gear": 3.50, "brake_balance": -2,
            "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.15, "toe_r": 0.25,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },

    # ========== KYOTO ==========
    "Япония Kyoto Driving Park - Yamagiwa": {
        "TOP_CARS_DATABASE": [
            "Mazda RX-7 Spirit R '02",
            "Nissan Skyline GT-R V-spec II '94",
            "Toyota GR Supra RZ '19",
            "Honda NSX Type R '92",
            "Subaru WRX STI Type S '14"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 4, "arb_r": 5, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 270, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== ROAD ATLANTA ==========
    "США Michelin Raceway Road Atlanta": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 295, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== MOUNT PANORAMA ==========
    "Австралия Mount Panorama": {
        "TOP_CARS_DATABASE": [
            "Holden Commodore Gr.3",
            "Ford Mustang Gr.3",
            "Chevrolet Corvette C7 Gr.3",
            "Nissan GT-R Nismo GT3 '18",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 290, "final_gear": 4.10, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== NÜRBURGRING ==========
    "Германия Nürburgring (24 часа)": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "BMW M4 GT3 '22",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS Evo '19",
            "Ferrari 488 GT3 '18"
        ],
        "settings": {
            "height_f": 71, "height_r": 76, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 5, "arb_r": 5, "downforce_f": 220, "downforce_r": 420,
            "max_speed": 285, "final_gear": 4.15, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 25
        }
    },
    "Германия Nürburgring GP": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16"
        ],
        "settings": {
            "height_f": 69, "height_r": 73, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 295, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Германия Nürburgring Nordschleife": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "BMW M4 GT3 '22",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS Evo '19",
            "Ferrari 488 GT3 '18"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 5, "arb_r": 5, "downforce_f": 230, "downforce_r": 440,
            "max_speed": 280, "final_gear": 4.20, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== RED BULL RING ==========
    "Австрия Red Bull Ring": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16",
            "Ferrari 488 GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 290, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== SARDEGNA ==========
    "Италия Sardegna - Road Track - A": {
        "TOP_CARS_DATABASE": [
            "Alpine A110 '17",
            "Renault Sport Mégane R.S. Trophy '11",
            "Peugeot RCZ Gr.4",
            "Ford Focus RS '18",
            "Volkswagen Golf VII GTI '14"
        ],
        "settings": {
            "height_f": 73, "height_r": 78, "spring_f": 4.3, "spring_r": 4.6,
            "arb_f": 4, "arb_r": 4, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 270, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    "Италия Sardegna - Road Track - B": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 5, "arb_r": 5, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 275, "final_gear": 4.25, "brake_balance": -2,
            "camber_f": -2.1, "camber_r": -1.5, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 25
        }
    },
    "Италия Sardegna - Road Track - C": {
        "TOP_CARS_DATABASE": [
            "Porsche 919 Hybrid '16",
            "Toyota TS050 Hybrid '16",
            "Audi R18 '16",
            "Bugatti Vision GT",
            "McLaren Ultimate Vision GT"
        ],
        "settings": {
            "height_f": 71, "height_r": 76, "spring_f": 4.5, "spring_r": 4.8,
            "arb_f": 5, "arb_r": 6, "downforce_f": 210, "downforce_r": 400,
            "max_speed": 280, "final_gear": 4.20, "brake_balance": -2,
            "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 16, "lsd_accel_r": 26
        }
    },

    # ========== SUZUKA ==========
    "Япония Suzuka Circuit": {
        "TOP_CARS_DATABASE": [
            "Honda NSX GT500 '16",
            "Nissan GT-R GT500 '16",
            "Toyota Supra GT500 '97",
            "Porsche 911 GT3 R '19",
            "Ferrari 488 GT3 '18"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 290, "final_gear": 4.00, "brake_balance": -2,
            "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },

    # ========== TOKYO ==========
    "Япония Tokyo Expressway - Центр": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 Carrera RS (993) '95",
            "Honda NSX Type R '92",
            "Mazda RX-7 Spirit R '02",
            "Nissan Skyline GT-R V-spec II '94",
            "Toyota Supra RZ '97"
        ],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.0, "spring_r": 4.3,
            "arb_f": 4, "arb_r": 4, "downforce_f": 160, "downforce_r": 320,
            "max_speed": 270, "final_gear": 4.50, "brake_balance": -1,
            "camber_f": -1.8, "camber_r": -1.3, "toe_f": 0.05, "toe_r": 0.15,
            "lsd_init_r": 13, "lsd_accel_r": 23
        }
    },

    # ========== TRIAL MOUNTAIN ==========
    "США Trial Mountain Circuit": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 Carrera RS (993) '95",
            "Ferrari F40 '92",
            "Lamborghini Diablo GT '00",
            "Nissan Skyline GT-R V-spec II '94",
            "Mazda RX-7 Spirit R '02"
        ],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 4, "arb_r": 5, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 285, "final_gear": 4.15, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== TSUKUBA ==========
    "Япония Tsukuba Circuit": {
        "TOP_CARS_DATABASE": [
            "Honda Civic Type R (FK8) '20",
            "Mazda RX-7 Spirit R '02",
            "Nissan Skyline GT-R V-spec II '94",
            "Toyota GR Supra RZ '19",
            "Subaru WRX STI Type S '14"
        ],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5,
            "arb_f": 4, "arb_r": 4, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 260, "final_gear": 4.40, "brake_balance": -2,
            "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },

    # ========== WATKINS GLEN ==========
    "США Watkins Glen": {
        "TOP_CARS_DATABASE": [
            "Ford GT LM Race Car",
            "Chevrolet Corvette C7 Gr.3",
            "Dodge Viper SRT GT3-R '15",
            "Nissan GT-R Nismo GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 190, "downforce_r": 360,
            "max_speed": 300, "final_gear": 3.90, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },

    # ========== LAGUNA SECA ==========
    "США WeatherTech Raceway Laguna Seca": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (991) '16",
            "Ferrari 458 Italia '09",
            "McLaren 650S Coupe '14",
            "Chevrolet Corvette C7 ZR1 '19",
            "BMW M4 '14"
        ],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.4, "spring_r": 4.7,
            "arb_f": 5, "arb_r": 5, "downforce_f": 220, "downforce_r": 420,
            "max_speed": 270, "final_gear": 4.30, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 14, "lsd_accel_r": 25
        }
    },

    # ========== WILLOW SPRINGS ==========
    "США Willow Springs - Big Willow": {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Nissan GT-R Nismo GT3 '18",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": {
            "height_f": 65, "height_r": 69, "spring_f": 4.9, "spring_r": 5.3,
            "arb_f": 6, "arb_r": 6, "downforce_f": 160, "downforce_r": 320,
            "max_speed": 310, "final_gear": 3.75, "brake_balance": -2,
            "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },

    # ========== YAS MARINA ==========
    "ОАЭ Yas Marina Circuit": {
        "TOP_CARS_DATABASE": [
            "Mercedes-AMG GT3 '20",
            "Audi R8 LMS '15",
            "BMW M6 GT3 '16",
            "Ferrari 488 GT3 '18",
            "Porsche 911 GT3 R '19"
        ],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "arb_f": 5, "arb_r": 6, "downforce_f": 200, "downforce_r": 380,
            "max_speed": 300, "final_gear": 3.95, "brake_balance": -2,
            "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
}

# ============================================
# ФУНКЦИЯ ПОЛУЧЕНИЯ ТОП-5 МАШИН ДЛЯ ТРАССЫ
# ============================================

def get_TOP_CARS_DATABASE_for_track(track_name):
    """Возвращает топ-5 машин для трассы с их настройками"""
    if track_name in TOP_CARS_DATABASE_DATABASE:
        data = TOP_CARS_DATABASE_DATABASE[track_name]
        return {
            "TOP_CARS_DATABASE": data["TOP_CARS_DATABASE"],
            "settings": data["settings"]
        }
    # Значения по умолчанию для отсутствующих трасс
    return {
        "TOP_CARS_DATABASE": [
            "Porsche 911 GT3 RS (992) '22",
            "Ferrari 488 GT3 '18",
            "McLaren 720S GT3 '19",
            "Nissan GT-R Nismo GT3 '18",
            "Mercedes-AMG GT3 '20"
        ],
        "settings": DEFAULT_SETTINGS
    }

def get_track_settings(track_name):
    """Возвращает оптимальные настройки для трассы"""
    track_data = get_TOP_CARS_DATABASE_for_track(track_name)
    settings = DEFAULT_SETTINGS.copy()
    settings.update(track_data["settings"])
    return settings

# ============================================
# ФУНКЦИИ РАСЧЁТА
# ============================================

def calculate_pp(weight, power, downforce, drive_type, height_f, height_r, spring_f, spring_r, camber_f, camber_r, toe_f, toe_r):
    """Расчёт PP с учётом всех настроек"""
    if weight == 0:
        return 0
    
    # Базовая формула
    base_pp = (power / weight) * 100
    downforce_bonus = downforce / 20
    drive_bonus = 1.1 if drive_type == "4WD" else 1.0
    
    # Влияние подвески (отклонение от стандарта 75/80)
    height_penalty = abs(height_f - 75) * 0.2 + abs(height_r - 80) * 0.2
    
    # Влияние жёсткости пружин (отклонение от стандарта 4.5/4.8)
    spring_penalty = abs(spring_f - 4.5) * 1.5 + abs(spring_r - 4.8) * 1.5
    
    # Влияние развала (отклонение от стандарта -2.0/-1.5)
    camber_penalty = abs(camber_f + 2.0) * 4 + abs(camber_r + 1.5) * 4
    
    # Влияние схождения (отклонение от стандарта 0.10/0.20)
    toe_penalty = abs(toe_f - 0.10) * 40 + abs(toe_r - 0.20) * 40
    
    # Итоговый PP (не может быть ниже 300 и выше 1000)
    total_pp = base_pp * drive_bonus + downforce_bonus - height_penalty - spring_penalty - camber_penalty - toe_penalty
    
    return round(max(300, min(1000, total_pp)), 1)
    
# ============================================
# ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ИНТЕРФЕЙСА
# ============================================

def get_track_description(track_name):
    """Возвращает описание трассы"""
    descriptions = {
        "Италия Autodromo Nazionale Monza": "🏁 Скоростная трасса, длинные прямые",
        "Германия Nürburgring Nordschleife": "🌲 Зелёный ад, 73 поворота",
        "Япония Suzuka Circuit": "🗻 Техничная трасса, S-образные связки",
        "Бельгия Spa (24 часа)": "🏎️ Легендарная трасса, перепады высот",
        "Франция Le Mans (24 часа)": "🌊 Максимальная скорость, длинные прямые",
        "Япония Tokyo Expressway - Центр": "🏙️ Городская трасса, близкие стены",
    }
    return descriptions.get(track_name, "🏎️ Стандартная трасса")

def get_track_settings(track_name):
    """Возвращает настройки для трассы"""
    if track_name in TRACK_SETTINGS:
        settings = DEFAULT_SETTINGS.copy()
        settings.update(TRACK_SETTINGS[track_name])
        return settings
    return DEFAULT_SETTINGS.copy()

def get_TOP_CARS_DATABASE(track_name):
    """Возвращает топ-5 машин для трассы"""
    if track_name in TOP_CARS_DATABASE_DATABASE:
        return TOP_CARS_DATABASE_DATABASE[track_name]["TOP_CARS_DATABASE"]
    return ["Porsche 911 GT3 RS (992) '22", "Ferrari 488 GT3 '18", "McLaren 720S GT3 '19", "Nissan GT-R Nismo GT3 '18", "Mercedes-AMG GT3 '20"]

# ============================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================

if 'height_f' not in st.session_state:
    for key, value in DEFAULT_SETTINGS.items():
        st.session_state[key] = value
if 'selected_car' not in st.session_state:
    st.session_state.selected_car = CAR_NAMES[0] if CAR_NAMES else ""
if 'prev_track' not in st.session_state:
    st.session_state.prev_track = ""

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 Тюнинг Калькулятор - Все трассы")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин | 🏁 Трасс: **{len(TRACKS)}**")

# Боковая панель
with st.sidebar:
    st.header("🏁 Выбор трассы")
    selected_track = st.selectbox("Трасса", TRACKS)
    
    # Автообновление при смене трассы
    if selected_track != st.session_state.prev_track:
        st.session_state.prev_track = selected_track
        settings = get_track_settings(selected_track)
        for key, value in settings.items():
            st.session_state[key] = value
        st.rerun()
    
    st.info(f"📝 {get_track_description(selected_track)}")
    
    st.header("🚗 Выбор автомобиля")
    selected_car = st.selectbox("Автомобиль", CAR_NAMES, 
                                 index=CAR_NAMES.index(st.session_state.selected_car) if st.session_state.selected_car in CAR_NAMES else 0)
    st.session_state.selected_car = selected_car
    
    if st.button("🎯 Применить настройки трассы", use_container_width=True):
        settings = get_track_settings(selected_track)
        for key, value in settings.items():
            st.session_state[key] = value
        st.success(f"✅ Применены настройки для {selected_track}")
        st.rerun()

# ============================================
# ТОП-5 МАШИН
# ============================================

st.subheader(f"🏆 Топ-5 машин для трассы: {selected_track}")

TOP_CARS_DATABASE = get_TOP_CARS_DATABASE(selected_track)
if TOP_CARS_DATABASE:
    cols = st.columns(5)
    for i, car_name in enumerate(TOP_CARS_DATABASE):
        with cols[i]:
            st.markdown(f"**{i+1}. {car_name[:25]}**")
            if car_name in CAR_DATABASE:
                data = CAR_DATABASE[car_name]
                st.caption(f"PP: {data.get('pp', 0)} | {data.get('power', 0)} л.с.")
            if st.button(f"✅ Выбрать", key=f"top_{i}"):
                st.session_state.selected_car = car_name
                st.rerun()
else:
    st.info("Рекомендации загружаются...")
st.divider()

# ============================================
# ТЮНИНГ
# ============================================

st.subheader(f"🔧 Настройки для трассы {selected_track}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏗️ Подвеска")
    st.session_state.height_f = st.slider("Высота перед (мм)", 60, 100, st.session_state.height_f)
    st.session_state.height_r = st.slider("Высота зад (мм)", 60, 100, st.session_state.height_r)
    st.session_state.spring_f = st.slider("Пружины перед (N/mm)", 3.0, 6.0, st.session_state.spring_f, 0.1)
    st.session_state.spring_r = st.slider("Пружины зад (N/mm)", 3.0, 6.0, st.session_state.spring_r, 0.1)
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
    st.session_state.lsd_init_r = st.slider("LSD начальный момент", 5, 25, st.session_state.lsd_init_r)
    st.session_state.lsd_accel_r = st.slider("LSD ускорение", 10, 40, st.session_state.lsd_accel_r)
    
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
    
    # Расчёт PP с учётом всех настроек
    pp = calculate_pp(
        car_data.get('weight', 1450),
        car_data.get('power', 500),
        total_downforce,
        car_data.get('drive_type', 'FR'),
        st.session_state.height_f, st.session_state.height_r,
        st.session_state.spring_f, st.session_state.spring_r,
        st.session_state.camber_f, st.session_state.camber_r,
        st.session_state.toe_f, st.session_state.toe_r
    )
    
    def calculate_handling(camber_f, camber_r, toe_f, toe_r, height_f, height_r, 
                       spring_f, spring_r, arb_f, arb_r, downforce_f, downforce_r):
    """Расчёт управляемости"""
    # Поворачиваемость
    turn_in = round((camber_f - camber_r) * 2 + (toe_f - toe_r) * 10 + (height_r - height_f) / 20 + (arb_f - arb_r) / 10, 1)
    turn_in = max(-10, min(10, turn_in))
    
    # Стабильность
    stability = round(10 - abs(toe_f + toe_r) * 5 - abs(camber_f + camber_r) / 2 - abs(height_f - height_r) / 50, 1)
    stability = max(0, min(10, stability))
    
    # Сцепление
    grip = round(5 + (downforce_f + downforce_r) / 100 + (4 - abs(camber_f + camber_r) / 2) - abs(spring_f - spring_r) / 10, 1)
    grip = max(1, min(10, grip))
    
    # Отклик
    response = round((spring_f + spring_r) / 2 + (100 - (height_f + height_r) / 2) / 20, 1)
    response = max(1, min(10, response))
    
    return {'turn_in': turn_in, 'stability': stability, 'grip': grip, 'response': response}
    
    # Показываем, какие настройки больше всего влияют на PP
    with st.expander("📉 Влияние настроек на PP"):
        st.write("**Как настройки влияют на PP:**")
        
        # Вычисляем потери PP от каждой настройки
        height_loss = abs(st.session_state.height_f - 75) * 0.2 + abs(st.session_state.height_r - 80) * 0.2
        spring_loss = abs(st.session_state.spring_f - 4.5) * 2 + abs(st.session_state.spring_r - 4.8) * 2
        camber_loss = abs(st.session_state.camber_f + 2.0) * 5 + abs(st.session_state.camber_r + 1.5) * 5
        toe_loss = abs(st.session_state.toe_f - 0.10) * 50 + abs(st.session_state.toe_r - 0.20) * 50
        
        st.write(f"- **Высота подвески:** -{height_loss:.1f} PP (чем ниже, тем лучше для PP)")
        st.write(f"- **Жёсткость пружин:** -{spring_loss:.1f} PP (отклонение от стандарта снижает PP)")
        st.write(f"- **Развал:** -{camber_loss:.1f} PP (большой развал снижает PP)")
        st.write(f"- **Схождение:** -{toe_loss:.1f} PP (большое схождение сильно снижает PP)")
    
    # Радар
    categories = ['Ускорение', 'Поворачиваемость', 'Стабильность', 'Сцепление', 'Аэродинамика']
    values = [
        min((car_data.get('power', 500) / car_data.get('weight', 1450)) * 20, 10),
        handling['turn_in'] + 5,
        handling['stability'],
        handling['grip'],
        min(total_downforce / 50, 10)
    ]
    
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', name=selected_car[:20]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    # Рекомендации по улучшению PP
    st.subheader("💡 Как улучшить PP")
    recommendations = []
    
    if st.session_state.height_f < 65:
        recommendations.append("📈 **Высота подвески слишком низкая** — поднимите до 65-75 мм для лучшего PP")
    if st.session_state.height_r < 70:
        recommendations.append("📈 **Задняя подвеска слишком низкая** — поднимите до 70-80 мм")
    if abs(st.session_state.camber_f) > 2.5:
        recommendations.append("📈 **Слишком большой развал спереди** — уменьшите до -2.0..-2.5°")
    if abs(st.session_state.camber_r) > 2.0:
        recommendations.append("📈 **Слишком большой развал сзади** — уменьшите до -1.5..-2.0°")
    if abs(st.session_state.toe_f) > 0.20:
        recommendations.append("📈 **Слишком большое схождение спереди** — уменьшите до 0.05-0.15")
    if abs(st.session_state.toe_r) > 0.25:
        recommendations.append("📈 **Слишком большое схождение сзади** — уменьшите до 0.15-0.25")
    
    if not recommendations:
        recommendations.append("✅ Настройки оптимальны для PP! Отличный баланс.")
    
    for rec in recommendations:
        st.write(rec)
else:
    st.warning("Выберите машину из списка")
