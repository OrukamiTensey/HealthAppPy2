# HealthApp — Desktop Nutrition & Calorie Tracker

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Database](https://img.shields.io/badge/SQLite-3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

**HealthApp** — це сучасний десктопний застосунок для відстеження харчування, підрахунку калорій, розрахунку добової норми білків, жирів та вуглеводів (БЖВ), а також аналізу динаміки маси тіла та фізичної активності.

---

## Основні можливості

* **Персоналізований розрахунок норм (BMR/TDEE):** Автоматичне обчислення добової калорійності та макронутрієнтів за формулою Міффліна-Сан Жеора з урахуванням статі, віку, ваги, зросту, рівня активності та цілі (схуднення, підтримка, набір ваги).
* **Інтерактивні кільцеві діаграми:** Візуальне відображення прогресу споживання калорій та БЖВ у режимі реального часу.
* **Щоденник харчування:** Додавання продуктів із вбудованої бази даних із автоматичним розрахунком макронутрієнтів залежно від вказаної ваги.
* **Динамічна система порад:** Плавна анімація з рекомендаціями щодо корекції раціону на основі поточного споживання.
* **Аналітика та статистика:** Перегляд історії харчування за тиждень, місяць або пів року у вигляді таблиць.
* **Експорт даних:** Можливість збереження звіту про харчування у формати CSV та TXT.
* **Кастомний профіль:** Налаштування та редагування персональних даних, зміна аватарки користувача.

---

## Скріншоти інтерфейсу

| Головна панель (БЖВ & Калорії) | Щоденник харчування |
| :---: | :---: |
| ![BMI Calculator](assets/screenshots/calculator.png) | ![Nutrition](assets/screenshots/nutrition.png) |

| Профіль користувача | Зміна даних |
| :---: | :---: |
| ![Profile](assets/screenshots/profile.png) | ![Statistics](assets/screenshots/enterdata.png) |

---

##  Архітектура та Модульність

Проєкт побудовано за модульним принципом ООП:

* `app.py` / `main.py` — Точка входу та головний каркас додатка (`ctk.CTk`).
* `calorie_counting.py` — Математична логіка обчислення BMR, БЖВ та формування порад.
* `bmi_calculator.py` — Вікно з кільцевими діаграмами та анімованими підказками.
* `nutrition.py` / `nutrition_window.py` — Модуль управління щоденним меню та відображення списку продуктів.
* `bmi_statistics_window.py` — Вікно перегляду та експорту статистики.
* `DB_control.py` — Обгортка для роботи з локальною базою даних SQLite (`Health_database.db`).
* `user.py` — Модель користувача та управління сесією (`current_user.json`).

---

##  Стек технологій

* **Мова програмування:** Python 3.10+
* **GUI Framework:** `customtkinter`, `tkinter`, `ttk`
* **Обробка зображень:** `Pillow` (PIL)
* **База даних:** SQLite3

---

##  Як запустити проєкт

### 1. Клонувати репозиторій
```bash
git clone [https://github.com/OrukamiTensey/HealthAppPy2.git](https://github.com/OrukamiTensey/HealthAppPy2.git)
cd HealthAppPy2
```
### 2. Встановити залежності
```bash
pip install customtkinter pillow
```
### 3. Запустити додаток
```bash
python main.py
```
