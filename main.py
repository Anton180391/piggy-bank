"""
КОПИЛКА - Консольное приложение для управления накоплениями
"""

import json
import os
from datetime import datetime


class Goal:
    """Класс для хранения информации о цели накопления"""
    
    # Список доступных категорий
    CATEGORIES = ["Работа", "Здоровье", "Образование", 
                  "Путешествия", "Техника", "Дом", "Хобби", "Другое"]
    
    def __init__(self, name, target_amount, category="Другое", current_amount=0):
        self.name = name                      # Название цели
        self.target_amount = target_amount    # Целевая сумма
        self.category = category              # Категория
        self.current_amount = current_amount  # Текущий баланс
    
    @property
    def progress(self):
        """Прогресс в процентах"""
        if self.target_amount <= 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
    
    @property
    def status(self):
        """Статус цели (Активна / Выполнена)"""
        if self.current_amount >= self.target_amount:
            return "Выполнена"
        return "Активна"
    
    def add_money(self, amount):
        """Пополнить цель"""
        if amount <= 0:
            return False, "Сумма должна быть положительной"
        
        self.current_amount += amount
        if self.current_amount > self.target_amount:
            self.current_amount = self.target_amount
        
        return True, f"Добавлено {amount:.2f} руб"
    
    def withdraw_money(self, amount):
        """Снять с цели"""
        if amount <= 0:
            return False, "Сумма должна быть положительной"
        
        if amount > self.current_amount:
            return False, f"Недостаточно средств. Доступно: {self.current_amount:.2f} руб"
        
        self.current_amount -= amount
        return True, f"Снято {amount:.2f} руб"
    
    def edit(self, name=None, target_amount=None, category=None):
        """Редактировать цель"""
        if name:
            self.name = name
        if target_amount and target_amount > 0:
            self.target_amount = target_amount
        if category and category in self.CATEGORIES:
            self.category = category
    
    def to_dict(self):
        """Превратить цель в словарь (для сохранения)"""
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "category": self.category,
            "current_amount": self.current_amount
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создать цель из словаря (для загрузки)"""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            category=data.get("category", "Другое"),
            current_amount=data.get("current_amount", 0)
        )


class Storage:
    """Класс для сохранения и загрузки данных"""
    
    FILE_NAME = "data.json"
    
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), self.FILE_NAME)
    
    def save(self, goals):
        """Сохранить список целей в файл"""
        data = {
            "goals": [goal.to_dict() for goal in goals]
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load(self):
        """Загрузить список целей из файла"""
        if not os.path.exists(self.file_path):
            return []
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return [Goal.from_dict(goal_data) for goal_data in data.get("goals", [])]


class PiggyBankApp:
    """Главное приложение Копилка"""
    
    def __init__(self):
        self.storage = Storage()
        self.goals = self.storage.load()
    
    def clear_screen(self):
        """Очистить экран"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_menu(self):
        """Показать главное меню"""
        self.clear_screen()
        print("=" * 50)
        print("🐷 КОПИЛКА - Управление накоплениями")
        print("=" * 50)
        print("1. Добавить цель")
        print("2. Показать все цели")
        print("3. Пополнить цель")
        print("4. Снять с цели")
        print("5. Редактировать цель")
        print("6. Удалить цель")
        print("7. Цели по категориям")
        print("8. Общая статистика")
        print("0. Выход")
        print("-" * 50)
    
    def create_goal(self):
        """Создать новую цель"""
        print("\n📌 НОВАЯ ЦЕЛЬ")
        print("-" * 40)
        
        name = input("Название цели: ").strip()
        if not name:
            print("❌ Название не может быть пустым")
            return
        
        try:
            target_amount = float(input("Сумма цели (руб): "))
            if target_amount <= 0:
                print("❌ Сумма должна быть положительной")
                return
        except ValueError:
            print("❌ Введите число")
            return
        
        # Выбор категории
        print("\nКатегории:")
        for i, cat in enumerate(Goal.CATEGORIES, 1):
            print(f"   {i}. {cat}")
        
        try:
            cat_choice = int(input("Выберите категорию: "))
            category = Goal.CATEGORIES[cat_choice - 1] if 1 <= cat_choice <= len(Goal.CATEGORIES) else "Другое"
        except ValueError:
            category = "Другое"
        
        goal = Goal(name, target_amount, category)
        self.goals.append(goal)
        self.storage.save(self.goals)
        print(f"\n✅ Цель '{name}' создана!")
        print(f"   Нужно накопить: {target_amount:.2f} руб")
        print(f"   Категория: {category}")
    
    def show_all_goals(self):
        """Показать все цели"""
        print("\n📊 ВСЕ ЦЕЛИ")
        print("=" * 50)
        
        if not self.goals:
            print("Нет созданных целей")
            return
        
        for i, goal in enumerate(self.goals, 1):
            # Статус
            status_icon = "✅" if goal.status == "Выполнена" else "⏳"
            
            print(f"\n{i}. {status_icon} {goal.name}")
            print(f"   Категория: {goal.category}")
            print(f"   Статус: {goal.status}")
            print(f"   Сумма: {goal.current_amount:.2f} / {goal.target_amount:.2f} руб")
            print(f"   Прогресс: {goal.progress:.1f}%")
            
            # Визуальный прогресс-бар
            bar_length = 30
            filled = int(bar_length * goal.progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"   [{bar}]")
            print(f"   Осталось: {goal.target_amount - goal.current_amount:.2f} руб")
    
    def select_goal(self, action):
        """Выбрать цель по номеру"""
        if not self.goals:
            print("Нет созданных целей")
            return -1
        
        print("\n📋 СПИСОК ЦЕЛЕЙ:")
        for i, goal in enumerate(self.goals, 1):
            print(f"   {i}. {goal.name}")
        
        try:
            choice = int(input(f"\nВыберите цель для {action}: "))
            if 1 <= choice <= len(self.goals):
                return choice - 1
            print(f"❌ Введите число от 1 до {len(self.goals)}")
            return -1
        except ValueError:
            print("❌ Введите число")
            return -1
    
    def add_money(self):
        """Пополнить цель"""
        idx = self.select_goal("пополнения")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n💰 ПОПОЛНЕНИЕ: {goal.name}")
        print(f"   Текущий баланс: {goal.current_amount:.2f} руб")
        
        try:
            amount = float(input("Сумма пополнения (руб): "))
        except ValueError:
            print("❌ Введите число")
            return
        
        success, message = goal.add_money(amount)
        if success:
            self.storage.save(self.goals)
            print(f"✅ {message}")
            # Проверка на достижение цели
            if goal.status == "Выполнена":
                print(f"🎉 ПОЗДРАВЛЯЮ! Цель '{goal.name}' ДОСТИГНУТА! 🎉")
        else:
            print(f"❌ {message}")
    
    def withdraw_money(self):
        """Снять с цели"""
        idx = self.select_goal("снятия")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n💸 СНЯТИЕ: {goal.name}")
        print(f"   Текущий баланс: {goal.current_amount:.2f} руб")
        
        try:
            amount = float(input("Сумма снятия (руб): "))
        except ValueError:
            print("❌ Введите число")
            return
        
        success, message = goal.withdraw_money(amount)
        if success:
            self.storage.save(self.goals)
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
    
    def edit_goal(self):
        """Редактировать цель"""
        idx = self.select_goal("редактирования")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n✏️ РЕДАКТИРОВАНИЕ: {goal.name}")
        print("(оставьте поле пустым, чтобы не менять)")
        
        new_name = input(f"Новое название [{goal.name}]: ").strip()
        
        try:
            new_target = input(f"Новая сумма [{goal.target_amount}]: ").strip()
            new_target = float(new_target) if new_target else None
        except ValueError:
            new_target = None
        
        new_category = input(f"Новая категория [{goal.category}]: ").strip()
        
        goal.edit(
            name=new_name if new_name else None,
            target_amount=new_target,
            category=new_category if new_category in Goal.CATEGORIES else None
        )
        
        self.storage.save(self.goals)
        print("✅ Цель обновлена")
    
    def delete_goal(self):
        """Удалить цель"""
        idx = self.select_goal("удаления")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n🗑️ УДАЛЕНИЕ: {goal.name}")
        confirm = input(f"Удалить цель '{goal.name}'? (y/n): ").lower()
        
        if confirm == 'y':
            self.goals.pop(idx)
            self.storage.save(self.goals)
            print("✅ Цель удалена")
        else:
            print("❌ Удаление отменено")
    
    def show_categories(self):
        """Показать цели по категориям"""
        print("\n🏷️ ЦЕЛИ ПО КАТЕГОРИЯМ")
        print("=" * 50)
        
        if not self.goals:
            print("Нет созданных целей")
            return
        
        # Группировка по категориям
        categories_dict = {}
        for goal in self.goals:
            if goal.category not in categories_dict:
                categories_dict[goal.category] = []
            categories_dict[goal.category].append(goal)
        
        for category, goals_list in categories_dict.items():
            total_target = sum(g.target_amount for g in goals_list)
            total_current = sum(g.current_amount for g in goals_list)
            
            print(f"\n📌 {category}:")
            print(f"   Целей: {len(goals_list)}")
            print(f"   Накоплено: {total_current:.2f} / {total_target:.2f} руб")
            
            for goal in goals_list:
                status = "✅" if goal.status == "Выполнена" else "⏳"
                print(f"     {status} {goal.name}: {goal.current_amount:.2f}/{goal.target_amount:.2f} руб")
    
    def show_statistics(self):
        """Общая статистика по всем целям"""
        print("\n📈 ОБЩАЯ СТАТИСТИКА")
        print("=" * 50)
        
        if not self.goals:
            print("Нет созданных целей")
            return
        
        total_target = sum(g.target_amount for g in self.goals)
        total_current = sum(g.current_amount for g in self.goals)
        completed = sum(1 for g in self.goals if g.status == "Выполнена")
        
        total_progress = (total_current / total_target * 100) if total_target > 0 else 0
        
        print(f"   Всего целей: {len(self.goals)}")
        print(f"   Выполнено целей: {completed}")
        print(f"   Всего накоплено: {total_current:.2f} руб")
        print(f"   Целевая сумма: {total_target:.2f} руб")
        print(f"   Общий прогресс: {total_progress:.1f}%")
        
        # Визуальный прогресс-бар
        bar_length = 40
        filled = int(bar_length * total_progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"   [{bar}]")
    
    def run(self):
        """Запуск приложения"""
        while True:
            self.show_menu()
            choice = input("\n👉 Выберите действие: ").strip()
            
            if choice == "1":
                self.create_goal()
            elif choice == "2":
                self.show_all_goals()
            elif choice == "3":
                self.add_money()
            elif choice == "4":
                self.withdraw_money()
            elif choice == "5":
                self.edit_goal()
            elif choice == "6":
                self.delete_goal()
            elif choice == "7":
                self.show_categories()
            elif choice == "8":
                self.show_statistics()
            elif choice == "0":
                print("\n👋 До свидания! Хороших накоплений!")
                break
            else:
                print("❌ Неверный выбор")
            
            input("\nНажмите Enter для продолжения...")


# Запуск программы
if __name__ == "__main__":
    app = PiggyBankApp()
    app.run()
