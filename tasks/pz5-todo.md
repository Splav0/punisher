# ПЗ5 - todo

## Домашнее задание

1. Понять, что такое [yield](https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do) и когда применяется.
1. Усвоить что такое итератор, итерируемый объект и генератор. Python к вершинам мастерства. Глава 14, стр 432-450
2. Определить и протестировать метод для красивого вывода в консоль тудушки.
3. Обработать случай файла тудушки неправильного формата.
4. Дописать тесты с использованием параметризации.
4. [Видео](https://www.youtube.com/watch?v=X1PQ7zzltz4) про метод super() (англ.) Также рекомендуется к просмотру и другие ролики с этого канала.
5. Отдельная мини-задача. Реализовать функцию, которая считывает построчно файл, до тех пор пока не встретит строку "Срочно", выводит ее на экран и останавливает считывание.

## План (для преподавателя)

1. Вспомнить, сделали за предыдущую пару, проверить список ошибок, которые необходимо обработать, обсудить новые.
2. Протестировать функции. Показать фикстуры. **Напоминаем механизм ишьюсов и веток.**

## Рассматриваемые вопросы

1. Продолжаем любить коммиты.
2. Разбор домашнего  задания с определением метода \_\_iter\_\_, \_\_getitem\_\_
3. Тестирование (продолжение). 

## Ход работы

1. Что хотим получить? Хотим итерироваться по списку в тудушке и чтобы, например, работал такой код:

  ```python
   for entry in todo:
       print(entry)
  ```

   Предложения?

   Необходимо определить методы \_\_iter\_\_ и  \_\_next\_\_.  \_\_iter\_\_  - возвращает объект итератор и вызывается в начале цикла. \_\_next\_\_ -  возвращает следующее значение и вызывается на каждом проходе цикла. Этот метод вызывает исключение StopIteration, когда больше нет значений для возврата, что неявно фиксируется конструкциями циклов для прекращения итерации.

   Метод \_\_iter\_\_ можно реализовать двумя способами

   ```python
   # самый простой вариант
   def __iter__(self):
       return iter(self.entries)

   # вариант через yield - более наглядный
   def __iter__(self):
       for entry in self.entries:
           yield entry
   ```

   Тут мы проходим по всем тудушкам и отдаем текущую запись.

   И на самом деле нам не нужно определять метод \_\_next\_\_. Плохая идея итерируемый объект делать еще и итератором. Подробности в домашнем задании.

2. Хотим, чтобы можно было обращаться по индексам записей в тудушке, то есть должен работать такой незамысловатый код:

   ```python
   todo = TodoJournal(...)
   print(todo[0]) # из тудушки выведется на экран запись с индексом 0
   ```

   Реализуем магический (специальный) метод \_\_getitem__:

   ```python
   def __getitem__(self, index):
       return self.entries[index]
   ```

   Давайте теперь попробуем обратиться по индексу, как хотели изначально.

   ```python
   print(todo.entries[0])
   ```

   Попробуем воспользоваться механизмом срезов:

   ```python
   print(todo.entries[0:1])
   ```

3. Чуть-чуть поговорим о динамических атрибутах

   Умозрительно, первая и последняя записи в тудушке могут быть нам более интересными и мы бы хотели вызывать их просто по имени. Вот так:

   ```python
   todo.first
   todo.last
   ```

   Как это можно сделать?

   Первый приходящий на ум вариант добавить в конструктор атрибут:

   ```python
   self.first = self.entries[0]
   self.last = self.entries[-1]
   ```

   Выглядит уже не очень, а если например захотим так легко обращаться по имени к первым пяти записям? то код будет раздуваться.

   Метод \_\_getattr\_\_ упростит нам задачу.

   Когда вызывается этот метод?

   Метод \_\_getattr\_\_ вызывается интерпретатором, если поиск атрибута завершается неудачно. То есть, он анализируя выражение todo.first python проверяет, есть ли у объекта todo атрибут с именем first. Если нет, поиск повторяется в классе (todo.\_\_class\_\_), если и тут не находит смотрит по иерархии наследования классов (все несколько сложнее, но это нам не важно). Если и там не нашлось, то вызывается метод \_\_getattr\_\_, определенный в классе todo. И на вход этому методу передается self и имя атрибута в виде строки, то есть first.

   Исходя из этих знаний определим метод \_\_getattr\_\_

   ```python
       # ниже статическое поле класса
       shortcut_names = {"first": 0, "last": -1}
   
       def __getattr__(self, item):
           index = self.shortcut_names.get(item, None)
           if index is not None:
               return self.entries[index]
   
           cls = type(self)
           raise AttributeError(f"{cls.__name__} object has no attribute {item}")
   ```

   Тут мы в том числе узнали зачем нужен raise, а также обращаю внимание на сообщение, которое передали в исключение. Оно такое же, как если бы мы попытались обратиться к несуществующему атрибуту и python сам бы сгенерировал исключение (проверьте).

   Проведем эксперимент:

   ```python
   print(todo.first)
   todo.first = "test"
   print(todo.first)
   print(todo[0])
   ```

   Не очень ожидаемое для нас поведение. При обращении к атрибуту по имени одно значение, при обращении непосредственно по индексу другое.

   Почему так?

   Напомним: python вызовет метод \_\_getattr\_\_ только в том случае, когда он не найдет среди у объекта искомого атрибута. однако строкой todo.first = "test" мы создали атрибут, поэтому \_\_getattr\_\_ не будет вызываться (проверьте в отладчике).

   Чтобы избежать такой несогласованности необходимо реализовать метод \_\_setattr\_\_ и сделать "виртуальные атрибуты" readonly.

   ```python
   def __setattr__(self, name, value):
       error_msg = ''
       if name in self.shortcut_names:
           error_msg = f"readonly attribute {name}"
       if error_msg:
           raise AttributeError(error_msg)
       super().__setattr__(name, value) # по умолчанию вызываем обычный setattr из супер класса
   ```

   Попробуем теперь выполнить изменение атрибута.

4. Начнем последовательно тестировать функции.

   Функция create. В этой функции осуществляется открытие файла.

   Воспользуемся фикстурой tmpdir и создадим тудушку. Далее необходимо создать ожидаемые данные и сверить их с тем, что получилось при создании тудушки.

   ```python
   def test_create_journal(tmpdir):
       todo_filename = "test_todo"
       todo = tmpdir.join(todo_filename)

       expected_todo = json.dumps(
           {
           "name": "test",
           "todos": []
           },
           indent=4)

       TodoJournal.create(todo, "test")
   
       assert expected_todo == todo.read()
   ```

   Протестируем функцию добавления записи в тудушку add_entry.

   ```python
   def test_add_entry(tmpdir):
       todo_filename = "test_todo"
       todo = tmpdir.join(todo_filename)

       expected_todo = json.dumps(
           {
           "name": "test",
           "todos": ["Сходить за молоком"]
           },
           indent=4,
           ensure_ascii=False,)

       TodoJournal.create(todo, "test")
       todo_jrnl = TodoJournal(todo)
       todo_jrnl.add_entry("Сходить за молоком")
   
       assert expected_todo == todo.read()
   ```

   Запустим тесты с измерением покрытия. Видим, например, что функция _parse тоже частично покрыта тестами, а также и другие функции. Хотя явно мы их не покрывали тестами. 
   Это к вопросу, что плохая идея полагаться на метрику coverage, как надежный показатель протестированности кода.

   

   Каждый раз мы создаем тудушку, готовим для нее какие-то данные и по сути это нужно будет делать во многих тестах.

   Тесты удобно писать со следующими комментариями #GIVEN #THEN #NEXT.

   Напишем свои фикстуры, которые будут подготавливать данные для тестов.

   ```python
   @pytest.fixture()
   def todo_journal_with_3_entries(tmpdir):
       todo_filename = "test_todo"
       todo_path = tmpdir.join(todo_filename)
       with open(todo_path, "w") as f:
           json.dump(
               {
                   "name": "test",
                   "todos": ["first entry", "second_entry", "third entry"]
               },
               f,
               indent=4,
               ensure_ascii=False, )
       return todo_path
   
   
   @pytest.fixture()
   def todo_json_after_remove_second_entry():
       return json.dumps(
           {
               "name": "test",
               "todos": ["first entry", "third entry"]
           },
           indent=4,
           ensure_ascii=False, )
   
   
   @pytest.fixture()
   def todo_object_with_with_3_entries(todo_journal_with_3_entries):
       return TodoJournal(todo_journal_with_3_entries)
   ```

   И протестируем функцию удаления:

   ```python
   def test_remove_entry(todo_object_with_with_3_entries, todo_json_after_remove_second_entry):
       expected_todo_json_after_remove_second_entry = todo_json_after_remove_second_entry

       todo_object_with_with_3_entries.remove_entry(1)

       assert expected_todo_json_after_remove_second_entry == todo_object_with_with_3_entries.path_todo.read()
   ```

   Проверить, что вызвалось исключение при невозможности парсинга:

   ```python
   def test_parse():
       with pytest.raises(SystemExit):
           todo_jrnl = TodoJournal("./path/without/todo")
   ```

    

