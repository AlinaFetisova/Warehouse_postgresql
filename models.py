import json
import os

# 1.Описуємо структуру одного товару
class Product:
    # __init__ — це конструктор 
    # self — вказує на конкретний об'єкт
    def __init__(self, name, price, quantity):
        self.name=name
        self.price=price
        self.quantity=quantity

    def to_dict(self): #створення словника для отримання даних окремо
        return {"name": self.name, "price": self.price, "quantity": self.quantity}

    #виведення товарів
    def info(self):
        return f"Товар: {self.name} | Ціна: {self.price} | Кількість: {self.quantity}"

    #виведення загальної ціни товару
    def get_total_price(self):
        return self.price*self.quantity
    
# 2. Описуємо логіку складу (керування списком об'єктів Product)
class Warehouse:
    def __init__(self):
        # 1. Знаходимо абсолютний шлях до папки, де лежить скрипт
        base_path=os.path.dirname(os.path.abspath(__file__))

        # 2. Створюємо повний шлях до файлу JSON у цій же папці
        self._db_path=os.path.join(base_path, "warehouse.json")

        # 3. Шлях для майбутнього звіту
        self._report_path=os.path.join(base_path, "report.txt")
        self._items=[]
        self.load_from_file()


    @property
    def report_path(self): # Дозволяємо Flask знати шлях до звіту, не міняючи його
        return self._report_path
        
    @property
    def items(self):
        return self._items
        
    def save_to_file(self):
        data=[item.to_dict() for item in self._items]
        with open(self._db_path, "w", encoding="utf-8") as f:
            # dump записує дані
            json.dump(data, f, indent=4, ensure_ascii=False)
        return "Дані збережено!"
    
    def load_from_file(self, filename="warehouse.json"):
        if not os.path.exists(self._db_path):
            return False
        try:
            with open(self._db_path, "r", encoding="utf-8") as f:
                data=json.load(f) # читаємо список словників
                self._items=[Product(d["name"], d["price"], d["quantity"]) for d in data]
            return True
        except:  
            return False
        
    # метод для звіту
    def generate_txt_report(self):
        if not self._items:
            return "Склад порожній."
        
        with open(self._report_path, "w", encoding="utf-8") as f:
            f.write("=== ОФІЦІЙНИЙ ЗВІТ СКЛАДУ ===\n")
            f.write(f"{'Назва товару':<20} | {'Ціна':<10} | {'Кількість':<10} | {'Сума':<10}\n")
            f.write("-"*60+"\n")
            
            for item in self.items:
                item_sum=item.get_total_price()
                #вирівнювання вліво
                f.write(f"{item.name:<20} | {item.price:<10} | {item.quantity:<10} | {item_sum:<10}\n")
            f.write("-"*60+"\n")
            total_all=sum(item.get_total_price() for item in self._items)
            f.write(f"ЗАГАЛЬНА ВАРТІСТЬ СКЛАДУ: {total_all} грн\n")
        
        return f"Звіт створено: {self.report_path}"

    #додавання товару
    def add_product(self, name, price, quantity):
        exist_product=self.find_product(name)
        if exist_product:
            exist_product.quantity+=quantity
            exist_product.price=price
            self.save_to_file()
            return f"Товар {name} оновлено: нова ціна {price} грн, кількість збільшена!"
        
        # 1. Валідація: перевірка на порожнє ім'я або від'ємні числа
        if not name.strip() or price<=0 or quantity<0:
            return "Помилка: некоректні дані"
            
        # Створюємо новий об'єкт класу Product і додаємо в список
        self._items.append(Product(name, price, quantity))
        self.save_to_file()
        return f"Товар {name} додано!"
            

    #знаходження певного товару
    def find_product(self, target_name):
        for item in self._items:
            if item.name.lower()==target_name.lower():
                return item
        return None
            

    #оновлення кількості товару
    def update_quantity(self, name, new_qty):
        product=self.find_product(name)
        if product and new_qty>=0:
            product.quantity=new_qty
            self.save_to_file()
            return f"Кількість {name} оновлена"
        return "Помилка оновлення"
    

    #видалення товару
    def delete_item(self, name):
        product=self.find_product(name)
        if product:
            self._items.remove(product)
            self.save_to_file()
            return f"Товар {name} видалено"
        return "Товар не знайдено"
        