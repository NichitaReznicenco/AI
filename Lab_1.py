class World:
    WIDTH = 5
    HEIGHT = 5

    def __init__(self):
        self.grid = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.next_block_number = 1
        self.log = []
        self.hook_position = None  # Позиция крюка
        self.hooked_block = None    # Захваченный блок
        self.grap_used = False      # Флаг использования команды grap

    def display(self):
        for row in self.grid:
            modified_row = ['-' if element == 0 else str(element) for element in row]
            print('[' + ', '.join(modified_row) + ']')

    def add_block(self, x):
        if self.grid[0][x] != 0:  # Если потолок занят, не добавляем блок
            self.log.append(f"Не удалось добавить блок в позицию X={x}, потому что потолок занят.")
            return
        y = 0
        while y < self.HEIGHT - 1 and self.grid[y + 1][x] == 0:
            y += 1
        self.grid[y][x] = self.next_block_number
        self.next_block_number += 1
        self.log.append(f"Блок {self.next_block_number - 1} добавлен в позицию X={x}, Y={y}.")

    def is_within_bounds(self, x):
        return 0 <= x < self.WIDTH

    def grap(self, block_number):
        if self.grap_used:
            print("Ошибка: команда grap уже использована.")
            return

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.grid[y][x] == block_number:
                    if y == 0 or self.grid[y - 1][x] == 0:
                        self.hook_position = (x, y)
                        self.hooked_block = block_number  # Сохраняем информацию о захваченном блоке
                        self.log.append(f"Крюк захватил блок {block_number} в позиции X={x}, Y={y}.")
                        print(f"Блок {block_number} успешно захвачен.")
                        self.grid[y][x] = 0  # Удаляем блок из предыдущей позиции
                        self.grap_used = True
                        return
                    else:
                        self.log.append(f"Ошибка: Не удалось захватить блок {block_number}, так как над ним находится другой блок.")
                        print(f"Ошибка: Не удалось захватить блок {block_number}, так как над ним находится другой блок.")
                        return
        self.log.append(f"Ошибка: Не удалось захватить блок {block_number}, так как он не найден.")

    def move(self, x):
        if self.hook_position:
            x_old, y_old = self.hook_position
            self.hook_position = (x, y_old)
            self.log.append(f"Крюк перемещен над столбцом X={x}.")
        else:
            self.log.append("Ошибка: Крюк не захватил ни один блок.")


    def put_on(self):
        if self.hook_position:
            x, y = self.hook_position
            # Находим первое пустое место в столбце, начиная снизу
            while y < self.HEIGHT - 1 and self.grid[y + 1][x] == 0:
                y += 1
            # Помещаем захваченный блок на найденное пустое место
            while y >= 0 and self.grid[y][x] != 0:
                y -= 1
            if y >= 0:
                self.log.append(f"Блок {self.hooked_block} брошен на блок в позиции X={x}, Y={y}.")
                print(f"Блок {self.hooked_block} брошен на блок в позиции X={x}, Y={y}.")
                self.grid[y][x] = self.hooked_block  # Используем захваченный блок
                self.hook_position = None
                self.hooked_block = None  # Сбрасываем информацию о захваченном блоке
                self.grap_used = False   # Сбрасываем флаг использования команды grap
            else:
                self.log.append("Ошибка: В этом столбце нет свободного места.")
                print("Ошибка: В этом столбце нет свободного места.")
        else:
            self.log.append("Ошибка: Крюк не захватил ни один блок.")
            print("Ошибка: Крюк не захватил ни один блок.")


    def find_last_entry(self, keyword):
        for entry in reversed(self.log):
            if keyword in entry:
                return entry
        return None

    def extract_block_numbers(self, question):
        block_numbers = []
        start_index = question.find("(")
        end_index = question.find(")")
        if start_index != -1 and end_index != -1:
            numbers_str = question[start_index + 1:end_index]
            block_numbers = [int(number) for number in numbers_str.split(",")]
        return block_numbers

    def cmd_handler(self, question):
        try:
            if "Куда добавлен блок" in question:
                block_numbers = self.extract_block_numbers(question)
                if len(block_numbers) > 0:
                    answers = []
                    for block_number in block_numbers:
                        entry = self.find_last_entry(f"Блок {block_number} добавлен")
                        if entry:
                            answers.append(entry)
                        else:
                            answers.append("Нет информации о добавлении блока.")
                    return answers[:2]  # Возвращаем только первые две записи (если они есть)
                else:
                    return "Некорректный формат вопроса."

            elif "Как крюк захватил блок" in question:
                block_numbers = self.extract_block_numbers(question)
                if len(block_numbers) > 0:
                    answers = []
                    for block_number in block_numbers:
                        entry = self.find_last_entry(f"Крюк захватил блок {block_number}")
                        if entry:
                            answers.append(entry)
                        else:
                            answers.append("Крюк не захватывал этот блок")
                    return answers[:2]  # Возвращаем только первые две записи (если они есть)
                else:
                    return "Некорректный формат вопроса."
            
            elif "Куда перемещался крюк" in question:
                entries = [entry for entry in self.log if "Крюк перемещен" in entry]
                if entries:
                    return entries
                else:
                    return "Нет информации о перемещениях крюка."

            elif "Куда брошен блок" in question:
                block_numbers = self.extract_block_numbers(question)
                if block_numbers:
                    block_number = block_numbers[0]  # Берем первый номер блока из вопроса
                    entries = [entry for entry in self.log if f"Блок {block_number} брошен на блок" in entry]
                    if entries:
                        return entries[:2]  # Возвращаем первые две записи о броске блока
                    else:
                        return f"Нет информации о броске блока {block_number}."
                else:
                    return "Некорректный формат вопроса."

            elif "Почему не удалось захватить блок" in question:
                block_numbers = self.extract_block_numbers(question)
                if block_numbers:
                    answers = []
                    for block_number in block_numbers:
                        for entry in reversed(self.log):
                            if f"Ошибка: Не удалось захватить блок {block_number}, так как над ним находится другой блок" in entry:
                                answers.append(entry)
                                break
                        else:
                            answers.append(f"Нет информации о причине неудачного захвата блока {block_number}.")
                    return answers
                else:
                    return "Некорректный формат вопроса."
            else:
                return "Вопрос не распознан."
        except Exception as e:
            return f"Ошибка, не правильный вопрос: {str(e)}"

# Создаем мир
world = World()

# Запрашиваем у пользователя координаты блоков и помещаем их в матрицу
while True:
    world.display()
    x_str = input("Введите номер блока (для выхода введите 'q'): ")
    if x_str.lower() == 'q':
        break
    try:
        block_number = int(x_str)
        if 0 <= block_number < world.WIDTH:
            world.add_block(block_number)
        else:
            world.log.append("Попытка добавить блок в недопустимую позицию.")
            print("Некорректный номер блока. Допустимый диапазон от 0 до", world.WIDTH - 1)
    except ValueError:
        world.log.append("Некорректный ввод номера блока.")
        print("Некорректный ввод. Попробуйте еще раз.")

# Отображаем состояние мира
world.display()

# Выводим журнал действий
print("\nЖурнал действий:")
for entry in world.log:
    print(entry)

# Цикл для выполнения действий с крюком
while True:
    world.display()
    action = input("\nВыберите действие: (grap, move, put_on, exit): ")
    
    if action == 'grap':
        block_str = input("Введите номер блока для захвата: ")
        try:
            block_number = int(block_str)
            world.grap(block_number)
        except ValueError:
            print("Некорректный ввод номера блока.")

    elif action == 'move':
        x_str = input("Введите координату X для перемещения крюка: ")
        try:
            x = int(x_str)
            if world.is_within_bounds(x):
                world.move(x)
                print(f"Крюк успешно перемещен над столбцом X={x}.")
            else:
                print("Некорректные координаты X. Допустимый диапазон от 0 до", world.WIDTH - 1)
        except ValueError:
            print("Некорректный ввод координаты X.")
    
    elif action == 'put_on':
        world.put_on()

    elif action == 'exit':
        break
    
    else:
        print("Некорректное действие. Попробуйте снова.")

# Отображаем состояние мира
world.display()

# Выводим журнал действий
print("\nЖурнал действий:")
for entry in world.log:
    print(entry)

# Отображаем состояние мира
world.display()

# Цикл для вопросов
while True:
    user_question = input("Введите ваш вопрос (для выхода введите 'exit'): ")
    if user_question.lower() == "exit":
        break
    answer = world.cmd_handler(user_question)  # Передаем только вопрос
    if isinstance(answer, list) and len(answer) > 0:
        print(answer[0])  # Выводим первый элемент списка
    else:
        print(answer)
