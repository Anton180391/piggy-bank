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
    
    def __init__(self, name, target_amount, category="Другое", current_amount=0.0):
        """
        Инициализация цели
        
        Args:
            name: Название цели
            target_amount: Целевая сумма
            category: Категория цели
            current_amount: Текущий баланс
        """
        self.name = name
        self.target_amount = target_amount
        self.category = category
        self.current_amount = current_amount
    
    @property
    def progress(self) -> float:
        """Прогресс в процентах"""
        if self.target_amount <= 0:
            return 0.0
        return (self.current_amount / self.target_amount) * 100
    
    @property
    def status(self) -> str:
        """Статус цели"""
        if self.current_amount >= self.target_amount:
            return "Выполнена"
        return "Активна"
    
    def add_money(self, amount: float) -> tuple:
        """
        Пополнение цели
        
        Args:
            amount: Сумма пополнения
            
        Returns:
            tuple: (успех, сообщение)
        """
        if amount <= 0:
            return False, "Ошибка: Сумма должна быть положительной"
        
        self.current_amount += amount
        if self.current_amount > self.target_amount:
            self.current_amount = self.target_amount
        
        return True, f"Успешно: Добавлено {amount:.2f} руб"
    
    def withdraw_money(self, amount: float) -> tuple:
        """
        Снятие средств с цели
        
        Args:
            amount: Сумма снятия
            
        Returns:
            tuple: (успех, сообщение)
        """
        if amount <= 0:
            return False, "Ошибка: Сумма должна быть положительной"
        
        if amount > self.current_amount:
            return False, f"Ошибка: Недостаточно средств. Доступно: {self.current_amount:.2f} руб"
        
        self.current_amount -= amount
        return True, f"Успешно: Снято {amount:.2f} руб"
    
    def edit(self, name: str = None, target_amount: float = None, category: str = None) -> None:
        """
        Редактирование цели
        
        Args:
            name: Новое название
            target_amount: Новая целевая сумма
            category: Новая категория
        """
        if name:
            self.name = name
        if target_amount and target_amount > 0:
            self.target_amount = target_amount
        if category and category in self.CATEGORIES:
            self.category = category
    
    def to_dict(self) -> dict:
        """Сериализация цели в словарь"""
        return {
            "name": self.name,
            "target_amount": self.target_amount,
            "category": self.category,
            "current_amount": self.current_amount
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Goal':
        """Десериализация цели из словаря"""
        return cls(
            name=data["name"],
            target_amount=data["target_amount"],
            category=data.get("category", "Другое"),
            current_amount=data.get("current_amount", 0.0)
        )


class Storage:
    """Класс для работы с файловым хранилищем"""
    
    FILE_NAME = "data.json"
    
    def __init__(self):
        """Инициализация хранилища"""
        self.file_path = os.path.join(os.path.dirname(__file__), self.FILE_NAME)
    
    def save(self, goals: list) -> bool:
        """
        Сохранение списка целей в файл
        
        Args:
            goals: Список объектов Goal
            
        Returns:
            bool: Успешность операции
        """
        try:
            data = {"goals": [goal.to_dict() for goal in goals]}
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load(self) -> list:
        """
        Загрузка списка целей из файла
        
        Returns:
            list: Список объектов Goal
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Goal.from_dict(goal_data) for goal_data in data.get("goals", [])]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка загрузки: {e}")
            return []


class PiggyBankApp:
    """Главное приложение Копилка"""
    
    def __init__(self):
        """Инициализация приложения"""
        self.storage = Storage()
        self.goals = self.storage.load()
    
    def _clear_screen(self) -> None:
        """Очистка экрана"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def _get_progress_bar(self, progress: float, width: int = 30) -> str:
        """
        Создание текстового прогресс-бара
        
        Args:
            progress: Процент прогресса
            width: Ширина бара
            
        Returns:
            str: Текстовый прогресс-бар
        """
        filled = int(width * progress / 100)
        return "[" + "#" * filled + "-" * (width - filled) + "]"
    
    def _show_menu(self) -> None:
        """Отображение главного меню"""
        self._clear_screen()
        print("=" * 60)
        print(" КОПИЛКА - Система управления накоплениями")
        print("=" * 60)
        print(" 1. Создать новую цель")
        print(" 2. Просмотреть все цели")
        print(" 3. Пополнить цель")
        print(" 4. Снять средства с цели")
        print(" 5. Редактировать цель")
        print(" 6. Удалить цель")
        print(" 7. Просмотреть цели по категориям")
        print(" 8. Общая статистика")
        print(" 0. Выход")
        print("-" * 60)
    
    def _create_goal(self) -> None:
        """Создание новой цели"""
        print("\n" + "=" * 40)
        print("СОЗДАНИЕ НОВОЙ ЦЕЛИ")
        print("=" * 40)
        
        # Ввод названия
        name = input("Название цели: ").strip()
        if not name:
            print("[ОШИБКА] Название не может быть пустым")
            return
        
        # Ввод суммы
        try:
            target_amount = float(input("Целевая сумма (руб): "))
            if target_amount <= 0:
                print("[ОШИБКА] Сумма должна быть положительной")
                return
        except ValueError:
            print("[ОШИБКА] Введите корректное число")
            return
        
        # Выбор категории
        print("\nДоступные категории:")
        for i, cat in enumerate(Goal.CATEGORIES, 1):
            print(f" {i:2d}. {cat}")
        
        try:
            cat_choice = int(input("\nВыберите категорию: "))
            if 1 <= cat_choice <= len(Goal.CATEGORIES):
                category = Goal.CATEGORIES[cat_choice - 1]
            else:
                print("[ПРЕДУПРЕЖДЕНИЕ] Выбрана категория по умолчанию: Другое")
                category = "Другое"
        except ValueError:
            print("[ПРЕДУПРЕЖДЕНИЕ] Выбрана категория по умолчанию: Другое")
            category = "Другое"
        
        # Создание цели
        goal = Goal(name, target_amount, category)
        self.goals.append(goal)
        
        if self.storage.save(self.goals):
            print(f"\n[УСПЕХ] Цель '{name}' успешно создана")
            print(f"        Целевая сумма: {target_amount:,.2f} руб")
            print(f"        Категория: {category}")
        else:
            print("\n[ОШИБКА] Не удалось сохранить цель")
    
    def _show_all_goals(self) -> None:
        """Отображение всех целей"""
        print("\n" + "=" * 60)
        print("СПИСОК ВСЕХ ЦЕЛЕЙ")
        print("=" * 60)
        
        if not self.goals:
            print("Нет созданных целей")
            return
        
        for i, goal in enumerate(self.goals, 1):
            status_marker = "[X]" if goal.status == "Выполнена" else "[ ]"
            
            print(f"\n{i}. {status_marker} {goal.name}")
            print(f"   Категория: {goal.category}")
            print(f"   Статус: {goal.status}")
            print(f"   Сумма: {goal.current_amount:,.2f} / {goal.target_amount:,.2f} руб")
            print(f"   Прогресс: {goal.progress:.1f}%")
            print(f"   {self._get_progress_bar(goal.progress)}")
            print(f"   Осталось накопить: {goal.target_amount - goal.current_amount:,.2f} руб")
        
        print("\n" + "=" * 60)
    
    def _select_goal(self, action: str) -> int:
        """
        Выбор цели по номеру
        
        Args:
            action: Действие для отображения
            
        Returns:
            int: Индекс выбранной цели или -1
        """
        if not self.goals:
            print("[ОШИБКА] Нет созданных целей")
            return -1
        
        print("\nСписок целей:")
        for i, goal in enumerate(self.goals, 1):
            print(f" {i:2d}. {goal.name}")
        
        try:
            choice = int(input(f"\nВыберите цель для {action}: "))
            if 1 <= choice <= len(self.goals):
                return choice - 1
            print(f"[ОШИБКА] Введите число от 1 до {len(self.goals)}")
            return -1
        except ValueError:
            print("[ОШИБКА] Введите корректное число")
            return -1
    
    def _add_money(self) -> None:
        """Пополнение цели"""
        idx = self._select_goal("пополнения")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n--- ПОПОЛНЕНИЕ: {goal.name} ---")
        print(f"Текущий баланс: {goal.current_amount:,.2f} руб")
        
        try:
            amount = float(input("Сумма пополнения (руб): "))
        except ValueError:
            print("[ОШИБКА] Введите корректное число")
            return
        
        success, message = goal.add_money(amount)
        if success:
            self.storage.save(self.goals)
            print(f"[УСПЕХ] {message}")
            if goal.status == "Выполнена":
                print(f"[СОБЫТИЕ] Цель '{goal.name}' достигнута!")
        else:
            print(f"[ОШИБКА] {message}")
    
    def _withdraw_money(self) -> None:
        """Снятие средств с цели"""
        idx = self._select_goal("снятия")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n--- СНЯТИЕ: {goal.name} ---")
        print(f"Текущий баланс: {goal.current_amount:,.2f} руб")
        
        try:
            amount = float(input("Сумма снятия (руб): "))
        except ValueError:
            print("[ОШИБКА] Введите корректное число")
            return
        
        success, message = goal.withdraw_money(amount)
        if success:
            self.storage.save(self.goals)
            print(f"[УСПЕХ] {message}")
        else:
            print(f"[ОШИБКА] {message}")
    
    def _edit_goal(self) -> None:
        """Редактирование цели"""
        idx = self._select_goal("редактирования")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n--- РЕДАКТИРОВАНИЕ: {goal.name} ---")
        print("(Оставьте поле пустым, чтобы не изменять)")
        
        new_name = input(f"Новое название [{goal.name}]: ").strip()
        
        try:
            new_target = input(f"Новая целевая сумма [{goal.target_amount:,.2f}]: ").strip()
            new_target = float(new_target) if new_target else None
            if new_target and new_target <= 0:
                print("[ОШИБКА] Сумма должна быть положительной")
                return
        except ValueError:
            print("[ОШИБКА] Введите корректное число")
            return
        
        print(f"\nКатегории: {', '.join(Goal.CATEGORIES)}")
        new_category = input(f"Новая категория [{goal.category}]: ").strip()
        
        goal.edit(
            name=new_name if new_name else None,
            target_amount=new_target,
            category=new_category if new_category in Goal.CATEGORIES else None
        )
        
        if self.storage.save(self.goals):
            print("[УСПЕХ] Цель обновлена")
        else:
            print("[ОШИБКА] Не удалось сохранить изменения")
    
    def _delete_goal(self) -> None:
        """Удаление цели"""
        idx = self._select_goal("удаления")
        if idx == -1:
            return
        
        goal = self.goals[idx]
        print(f"\n--- УДАЛЕНИЕ: {goal.name} ---")
        confirm = input(f"Удалить цель '{goal.name}'? (y/n): ").strip().lower()
        
        if confirm == 'y':
            self.goals.pop(idx)
            if self.storage.save(self.goals):
                print("[УСПЕХ] Цель удалена")
            else:
                print("[ОШИБКА] Не удалось сохранить изменения")
        else:
            print("[ОТМЕНА] Удаление отменено")
    
    def _show_categories(self) -> None:
        """Отображение целей по категориям"""
        print("\n" + "=" * 60)
        print("ЦЕЛИ ПО КАТЕГОРИЯМ")
        print("=" * 60)
        
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
            
            print(f"\n[ {category} ]")
            print(f"  Количество целей: {len(goals_list)}")
            print(f"  Накоплено: {total_current:,.2f} / {total_target:,.2f} руб")
            print(f"  Прогресс: {(total_current/total_target*100) if total_target>0 else 0:.1f}%")
            print("  ---")
            
            for goal in goals_list:
                status_marker = "[X]" if goal.status == "Выполнена" else "[ ]"
                print(f"    {status_marker} {goal.name}: {goal.current_amount:,.2f}/{goal.target_amount:,.2f} руб ({goal.progress:.1f}%)")
    
    def _show_statistics(self) -> None:
        """Отображение общей статистики"""
        print("\n" + "=" * 60)
        print("ОБЩАЯ СТАТИСТИКА")
        print("=" * 60)
        
        if not self.goals:
            print("Нет созданных целей")
            return
        
        total_target = sum(g.target_amount for g in self.goals)
        total_current = sum(g.current_amount for g in self.goals)
        completed = sum(1 for g in self.goals if g.status == "Выполнена")
        active = len(self.goals) - completed
        
        total_progress = (total_current / total_target * 100) if total_target > 0 else 0
        
        print(f"\n[Сводка по целям]")
        print(f"  Всего целей: {len(self.goals)}")
        print(f"  Активных целей: {active}")
        print(f"  Выполненных целей: {completed}")
        
        print(f"\n[Финансовая сводка]")
        print(f"  Всего накоплено: {total_current:,.2f} руб")
        print(f"  Целевая сумма: {total_target:,.2f} руб")
        print(f"  Осталось накопить: {total_target - total_current:,.2f} руб")
        print(f"  Общий прогресс: {total_progress:.1f}%")
        print(f"  {self._get_progress_bar(total_progress, 40)}")
    
    def run(self) -> None:
        """Запуск основного цикла приложения"""
        print("\n" + "=" * 60)
        print(" Добро пожаловать в систему управления накоплениями 'КОПИЛКА'")
        print("=" * 60)
        
        while True:
            self._show_menu()
            choice = input("\nВведите номер команды: ").strip()
            
            if choice == "1":
                self._create_goal()
            elif choice == "2":
                self._show_all_goals()
            elif choice == "3":
                self._add_money()
            elif choice == "4":
                self._withdraw_money()
            elif choice == "5":
                self._edit_goal()
            elif choice == "6":
                self._delete_goal()
            elif choice == "7":
                self._show_categories()
            elif choice == "8":
                self._show_statistics()
            elif choice == "0":
                print("\n" + "=" * 60)
                print(" Работа завершена. До новых встреч!")
                print("=" * 60)
                break
            else:
                print("[ОШИБКА] Неверный выбор. Пожалуйста, введите число от 0 до 8")
            
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    app = PiggyBankApp()
    app.run()
