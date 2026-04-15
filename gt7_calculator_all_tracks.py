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
            "downforce_f": 140, "downforce_r": 280, "max_speed": 330, "final_gear": 3.60,
            "brake_balance": -3, "camber_f": -2.6, "camber_r": -1.9, "toe_f": 0.18, "toe_r": 0.28,
            "lsd_init_r": 18, "lsd_accel_r": 30
        }
    },
    "Франция Le Mans (24 часа)": {
        "type": "speed",
        "description": "🌊 Максимальная скорость, длинные прямые",
        "top_cars": ["Porsche 919 Hybrid '16", "Toyota TS050 Hybrid '16", "Audi R18 '16", "Bugatti Vision GT", "Peugeot 908 HDi FAP '10"],
        "settings": {
            "height_f": 60, "height_r": 65, "spring_f": 5.2, "spring_r": 5.6,
            "downforce_f": 120, "downforce_r": 250, "max_speed": 360, "final_gear": 3.40,
            "brake_balance": -3, "camber_f": -2.8, "camber_r": -2.0, "toe_f": 0.20, "toe_r": 0.30,
            "lsd_init_r": 20, "lsd_accel_r": 35
        }
    },
    "Япония High Speed Ring": {
        "type": "speed",
        "description": "🏁 Круговая скоростная трасса",
        "top_cars": ["Nissan GT-R Nismo '17", "Porsche 911 Turbo S '20", "Ferrari F8 Tributo '19", "McLaren 720S '17", "Lamborghini Huracan LP 610-4 '15"],
        "settings": {
            "height_f": 65, "height_r": 70, "spring_f": 5.0, "spring_r": 5.4,
            "downforce_f": 130, "downforce_r": 260, "max_speed": 340, "final_gear": 3.50,
            "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.7, "toe_f": 0.15, "toe_r": 0.25,
            "lsd_init_r": 17, "lsd_accel_r": 28
        }
    },
    
    # Сложные техничные трассы
    "Германия Nürburgring Nordschleife": {
        "type": "technical",
        "description": "🌲 Зелёный ад, 73 поворота",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "BMW M4 GT3 '22", "Mercedes-AMG GT3 '20", "Audi R8 LMS Evo '19", "Ferrari 488 GT3 '18"],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5,
            "downforce_f": 230, "downforce_r": 440, "max_speed": 280, "final_gear": 4.20,
            "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    "Бельгия Spa (24 часа)": {
        "type": "technical",
        "description": "🏎️ Легендарная трасса, перепады высот",
        "top_cars": ["Porsche 911 GT3 R '19", "Ferrari 488 GT3 '18", "Audi R8 LMS '15", "McLaren 720S GT3 '19", "Mercedes-AMG GT3 '20"],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.5, "spring_r": 4.8,
            "downforce_f": 210, "downforce_r": 400, "max_speed": 300, "final_gear": 3.95,
            "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Япония Suzuka Circuit": {
        "type": "technical",
        "description": "🗻 Техничная трасса, S-образные связки",
        "top_cars": ["Honda NSX GT500 '16", "Nissan GT-R GT500 '16", "Toyota Supra GT500 '97", "Porsche 911 GT3 R '19", "Ferrari 488 GT3 '18"],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.00,
            "brake_balance": -2, "camber_f": -2.4, "camber_r": -1.8, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    "США WeatherTech Raceway Laguna Seca": {
        "type": "twisty",
        "description": "🇺🇸 Знаменитая шикана, перепады высот",
        "top_cars": ["Porsche 911 GT3 RS (991) '16", "Ferrari 458 Italia '09", "McLaren 650S Coupe '14", "Chevrolet Corvette C7 ZR1 '19", "BMW M4 '14"],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.4, "spring_r": 4.7,
            "downforce_f": 220, "downforce_r": 420, "max_speed": 270, "final_gear": 4.30,
            "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 14, "lsd_accel_r": 25
        }
    },
    "Австралия Mount Panorama": {
        "type": "technical",
        "description": "🏔️ Горная трасса, узкие участки",
        "top_cars": ["Holden Commodore Gr.3", "Ford Mustang Gr.3", "Chevrolet Corvette C7 Gr.3", "Nissan GT-R Nismo GT3 '18", "BMW M6 GT3 '16"],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8,
            "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.10,
            "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    
    # Городские трассы
    "Япония Tokyo Expressway - Центр": {
        "type": "city",
        "description": "🏙️ Городская трасса, близкие стены",
        "top_cars": ["Porsche 911 Carrera RS (993) '95", "Honda NSX Type R '92", "Mazda RX-7 Spirit R '02", "Nissan Skyline GT-R V-spec II '94", "Toyota Supra RZ '97"],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.0, "spring_r": 4.3,
            "downforce_f": 160, "downforce_r": 320, "max_speed": 270, "final_gear": 4.50,
            "brake_balance": -1, "camber_f": -1.8, "camber_r": -1.3, "toe_f": 0.05, "toe_r": 0.15,
            "lsd_init_r": 13, "lsd_accel_r": 23
        }
    },
    "Великобритания Brands Hatch - Grand Prix Circuit": {
        "type": "twisty",
        "description": "🏁 Извилистая трасса, перепады высот",
        "top_cars": ["Aston Martin Vantage GT3 '12", "McLaren 650S GT3 '15", "BMW M6 GT3 '16", "Ferrari 488 GT3 '18", "Porsche 911 GT3 R '19"],
        "settings": {
            "height_f": 70, "height_r": 75, "spring_f": 4.5, "spring_r": 4.8,
            "downforce_f": 210, "downforce_r": 400, "max_speed": 280, "final_gear": 4.20,
            "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    
    # Техничные трассы
    "Япония Fuji International Speedway": {
        "type": "technical",
        "description": "🗻 Длинная прямая, техничные повороты",
        "top_cars": ["Toyota Supra GT500 '97", "Nissan GT-R GT500 '08", "Honda NSX GT500 '08", "Lexus RC F GT500 '16", "Porsche 911 GT3 R '19"],
        "settings": {
            "height_f": 67, "height_r": 71, "spring_f": 4.7, "spring_r": 5.1,
            "downforce_f": 190, "downforce_r": 360, "max_speed": 310, "final_gear": 3.80,
            "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22,
            "lsd_init_r": 16, "lsd_accel_r": 27
        }
    },
    "Австрия Red Bull Ring": {
        "type": "mixed",
        "description": "🏎️ Короткая, но техничная",
        "top_cars": ["Mercedes-AMG GT3 '20", "Audi R8 LMS '15", "BMW M6 GT3 '16", "Ferrari 488 GT3 '18", "Porsche 911 GT3 R '19"],
        "settings": {
            "height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0,
            "downforce_f": 200, "downforce_r": 380, "max_speed": 290, "final_gear": 4.00,
            "brake_balance": -2, "camber_f": -2.2, "camber_r": -1.6, "toe_f": 0.10, "toe_r": 0.20,
            "lsd_init_r": 15, "lsd_accel_r": 26
        }
    },
    
    # Извилистые трассы
    "Швейцария Deep Forest Raceway": {
        "type": "twisty",
        "description": "⛰️ Лесная трасса, тоннель",
        "top_cars": ["Mazda RX-7 Spirit R '02", "Honda NSX Type R '92", "Nissan Skyline GT-R V-spec II '94", "Toyota Supra RZ '97", "Subaru Impreza 22B-STi '98"],
        "settings": {
            "height_f": 72, "height_r": 77, "spring_f": 4.3, "spring_r": 4.6,
            "downforce_f": 200, "downforce_r": 380, "max_speed": 275, "final_gear": 4.30,
            "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    "США Trial Mountain Circuit": {
        "type": "twisty",
        "description": "🏔️ Горная трасса, прыжки",
        "top_cars": ["Porsche 911 Carrera RS (993) '95", "Ferrari F40 '92", "Lamborghini Diablo GT '00", "Nissan Skyline GT-R V-spec II '94", "Mazda RX-7 Spirit R '02"],
        "settings": {
            "height_f": 74, "height_r": 79, "spring_f": 4.2, "spring_r": 4.5,
            "downforce_f": 190, "downforce_r": 360, "max_speed": 285, "final_gear": 4.15,
            "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18,
            "lsd_init_r": 14, "lsd_accel_r": 24
        }
    },
    
    # Остальные трассы (стандартные настройки)
    "США Watkins Glen": {
        "type": "mixed",
        "description": "🏎️ Быстрая, плавные повороты",
        "top_cars": ["Ford GT LM Race Car", "Chevrolet Corvette C7 Gr.3", "Dodge Viper SRT GT3-R '15", "Ferrari 488 GT3 '18", "Porsche 911 GT3 R '19"],
        "settings": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 190, "downforce_r": 360, "max_speed": 300, "final_gear": 3.90, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27}
    },
    "Канада Circuit Gilles-Villeneuve": {
        "type": "mixed",
        "description": "🏁 Городская трасса, шиканы",
        "top_cars": ["McLaren 720S GT3 '19", "Ferrari 488 GT3 '18", "Mercedes-AMG GT3 '20", "Audi R8 LMS '15", "Porsche 911 GT3 R '19"],
        "settings": {"height_f": 67, "height_r": 71, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 300, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27}
    },
    "Бразилия Autódromo de Interlagos": {
        "type": "technical",
        "description": "🌧️ Неровная трасса, нет прямой",
        "top_cars": ["Porsche 911 GT3 R '19", "Ferrari 488 GT3 '18", "Mercedes-AMG GT3 '20", "BMW M6 GT3 '16", "Audi R8 LMS '15"],
        "settings": {"height_f": 69, "height_r": 73, "spring_f": 4.5, "spring_r": 4.8, "downforce_f": 210, "downforce_r": 400, "max_speed": 290, "final_gear": 4.10, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 15, "lsd_accel_r": 26}
    },
    "США Daytona - дорожная": {
        "type": "speed",
        "description": "🏁 Овальная + шикана",
        "top_cars": ["Ford GT LM Race Car", "Chevrolet Corvette C7 Gr.3", "Dodge Viper SRT GT3-R '15", "Nissan GT-R Nismo GT3 '18", "Porsche 911 GT3 R '19"],
        "settings": {"height_f": 64, "height_r": 68, "spring_f": 5.0, "spring_r": 5.4, "downforce_f": 140, "downforce_r": 280, "max_speed": 330, "final_gear": 3.60, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26, "lsd_init_r": 17, "lsd_accel_r": 28}
    },
    "Япония Tsukuba Circuit": {
        "type": "twisty",
        "description": "🗻 Короткая техничная трасса",
        "top_cars": ["Honda Civic Type R (FK8) '20", "Mazda RX-7 Spirit R '02", "Nissan Skyline GT-R V-spec II '94", "Toyota GR Supra RZ '19", "Subaru WRX STI Type S '14"],
        "settings": {"height_f": 72, "height_r": 77, "spring_f": 4.2, "spring_r": 4.5, "downforce_f": 200, "downforce_r": 380, "max_speed": 260, "final_gear": 4.40, "brake_balance": -2, "camber_f": -2.0, "camber_r": -1.4, "toe_f": 0.08, "toe_r": 0.18, "lsd_init_r": 14, "lsd_accel_r": 24}
    },
    "США Willow Springs - Big Willow": {
        "type": "speed",
        "description": "🏁 Быстрая трасса, длинные повороты",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "Ferrari 488 GT3 '18", "McLaren 720S GT3 '19", "Nissan GT-R Nismo GT3 '18", "Mercedes-AMG GT3 '20"],
        "settings": {"height_f": 65, "height_r": 69, "spring_f": 4.9, "spring_r": 5.3, "downforce_f": 160, "downforce_r": 320, "max_speed": 310, "final_gear": 3.75, "brake_balance": -2, "camber_f": -2.5, "camber_r": -1.8, "toe_f": 0.16, "toe_r": 0.26, "lsd_init_r": 17, "lsd_accel_r": 28}
    },
    "ОАЭ Yas Marina Circuit": {
        "type": "technical",
        "description": "🏎️ Современная трасса, отель",
        "top_cars": ["Mercedes-AMG GT3 '20", "Audi R8 LMS '15", "BMW M6 GT3 '16", "Ferrari 488 GT3 '18", "Porsche 911 GT3 R '19"],
        "settings": {"height_f": 68, "height_r": 72, "spring_f": 4.6, "spring_r": 5.0, "downforce_f": 200, "downforce_r": 380, "max_speed": 300, "final_gear": 3.95, "brake_balance": -2, "camber_f": -2.3, "camber_r": -1.7, "toe_f": 0.12, "toe_r": 0.22, "lsd_init_r": 16, "lsd_accel_r": 27}
    },
}


def get_track_info(track_name):
    if track_name in TRACK_DATABASE:
        return TRACK_DATABASE[track_name]
    return {
        "type": "mixed",
        "description": "🏎️ Стандартная трасса",
        "top_cars": ["Porsche 911 GT3 RS (992) '22", "Ferrari 488 GT3 '18", "McLaren 720S GT3 '19"],
        "settings": get_default_settings()
    }

def get_custom_tune_for_car(car_name, track_name):
    car_data = CAR_DATABASE.get(car_name, {})
    drive_type = car_data.get('drive_type', 'FR')
    track_info = get_track_info(track_name)
    base_settings = track_info["settings"].copy()
    
    if drive_type == "RR":
        base_settings["camber_f"] = max(-3.0, base_settings.get("camber_f", -2.0) - 0.1)
        base_settings["camber_r"] = max(-2.5, base_settings.get("camber_r", -1.5) - 0.1)
    elif drive_type == "4WD":
        base_settings["camber_f"] = min(-1.5, base_settings.get("camber_f", -2.0) + 0.1)
        base_settings["camber_r"] = min(-1.0, base_settings.get("camber_r", -1.5) + 0.1)
    
    return base_settings

def get_top_5_cars_with_data(track_name):
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
# ИНИЦИАЛИЗАЦИЯ
# ============================================

def init_session_state():
    default_settings = get_default_settings()
    for key, value in default_settings.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if 'selected_car' not in st.session_state:
        st.session_state.selected_car = CAR_NAMES[0] if CAR_NAMES else ""
    if 'prev_track' not in st.session_state:
        st.session_state.prev_track = ""
    if 'prev_car' not in st.session_state:
        st.session_state.prev_car = st.session_state.selected_car

init_session_state()

# ============================================
# ИНТЕРФЕЙС
# ============================================

st.title("🏎️ GT7 Тюнинг Калькулятор")
st.markdown(f"📊 В базе: **{len(CAR_DATABASE)}** машин")

# Боковая панель
with st.sidebar:
    st.header("🏁 Выбор трассы")
    selected_track = st.selectbox("Трасса", TRACKS, key="track_select")
    track_info = get_track_info(selected_track)
    st.info(f"**Тип:** {track_info['description']}")
    
    st.header("🚗 Выбор автомобиля")
    selected_car = st.selectbox("Автомобиль", CAR_NAMES, 
                                 index=CAR_NAMES.index(st.session_state.selected_car) if st.session_state.selected_car in CAR_NAMES else 0,
                                 key="car_select")
    
    # АВТООБНОВЛЕНИЕ ПРИ СМЕНЕ МАШИНЫ ИЛИ ТРАССЫ
    need_update = False
    
    if selected_car != st.session_state.selected_car:
        st.session_state.selected_car = selected_car
        need_update = True
    
    if selected_track != st.session_state.prev_track:
        st.session_state.prev_track = selected_track
        need_update = True
    
    if need_update:
        tune = get_custom_tune_for_car(selected_car, selected_track)
        for key, value in tune.items():
            st.session_state[key] = value
        st.rerun()
    
    if st.button("🎯 Применить настройки", use_container_width=True):
        tune = get_custom_tune_for_car(selected_car, selected_track)
        for key, value in tune.items():
            st.session_state[key] = value
        st.success(f"✅ Применены настройки")

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
st.divider()

# ============================================
# ТЮНИНГ
# ============================================

st.subheader(f"🔧 Настройки для {selected_car[:35]}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏗️ Подвеска")
    st.session_state.height_f = st.slider("Высота перед", 60, 100, st.session_state.height_f)
    st.session_state.height_r = st.slider("Высота зад", 60, 100, st.session_state.height_r)
    st.session_state.spring_f = st.slider("Пружины перед", 3.0, 6.0, st.session_state.spring_f, 0.1)
    st.session_state.spring_r = st.slider("Пружины зад", 3.0, 6.0, st.session_state.spring_r, 0.1)
    st.session_state.arb_f = st.slider("Стаб перед", 3, 8, st.session_state.arb_f)
    st.session_state.arb_r = st.slider("Стаб зад", 3, 8, st.session_state.arb_r)
    st.session_state.camber_f = st.slider("Развал перед", -3.0, 0.0, st.session_state.camber_f, 0.1)
    st.session_state.camber_r = st.slider("Развал зад", -3.0, 0.0, st.session_state.camber_r, 0.1)
    st.session_state.toe_f = st.slider("Схождение перед", -0.3, 0.3, st.session_state.toe_f, 0.01)
    st.session_state.toe_r = st.slider("Схождение зад", -0.3, 0.3, st.session_state.toe_r, 0.01)

with col2:
    st.markdown("### 🌬️ Аэродинамика")
    st.session_state.downforce_f = st.slider("Прижимная перед", 100, 300, st.session_state.downforce_f)
    st.session_state.downforce_r = st.slider("Прижимная зад", 200, 500, st.session_state.downforce_r)
    st.markdown("### ⚙️ Трансмиссия")
    st.session_state.max_speed = st.slider("Макс скорость", 250, 360, st.session_state.max_speed)
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
    with col2:
        st.metric("🔄 Поворачиваемость", f"{handling['turn_in']:.1f}")
    with col3:
        st.metric("🛡️ Стабильность", f"{handling['stability']:.1f}/10")
    
    categories = ['Поворачиваемость', 'Стабильность', 'Сцепление', 'Отклик']
    values = [handling['turn_in'] + 5, handling['stability'], handling['grip'], handling['response']]
    
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', name=selected_car[:20]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(f"🏎️ GT7 Калькулятор | {len(CAR_DATABASE)} машин")
