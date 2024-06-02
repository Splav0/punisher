## Использование фикстур pytest при тестировании

Важной частью тракта разработки программного обеспечения является тестирование. В современных условиях при разработке с использованием языка программирования Python стандартном де-факто является модуль **pytest**. Подробное переведённое руководство по использованию этого модуля в ходе тестирования - однако заметим, что [оригинальный pdf-файл][pytest-manual-in-pdf] в некоторых ситуациях добавляет ясности с учётом корректной вёрстки и иллюстраций - можно отыскать в [цикле статей][pytest-manual-in-md] на habr'е.

Далее договоримся приводить все кусочки тестов с использованием pytest.

Писать тесты в ходе разработки на Python не так сложно, при этом необходимо  
Да, на первых порах Вы будете сталкиваться с ситуациями, когда в очередной раз в ходе выполнения домашнего задания, контрольной или курсовой работ будете доходить до момента, когда нужно выполнить тестирование написанного шедевра, тяжело вздыхать и из-под палки сёрфить статьи на stackoverflow или habr в поисках похожих кусочков кода..  
Но поверьте, Вы вырастете, станете взрослыми людьми, будете являться важной частью большой команды, разрабатывающей действительно что-то важное и нужное человечеству, - ну или Вам самим, - и вспомните тех гадких преподавателей да и просто старших товарищей, которые в юности заставляли Вас тратить время на понимании философии тестирования. Уверен, Вы будете очень рады тому, что привитое умение не забывать про тесты не раз спасло Вас от проблем, связанных с вносимыми ошибками в новые версии Вашего ПО. Да что там: Вы точно будете искренне хохотать, вспоминая, как когда-т плевались, видя в задании страшные словосочетания "написать тесты", "протестировать функции" и т.д.

### Простой пример тестов

Давайте для демонстрации принципов тестирования приведём простой пример функции, которую требуется протестировать - мы с Вами взрослые люди, поэтому будем сразу модульно разбивать исходный код и тесты (считаем, что 2 указанных модуля находятся в Вашем текущем каталоге):

```python
"""модуль 'math_functions.py'"""

def sum_integers(a: int, b: int) -> int:
    """
    Получение суммы двух целых чисел
    @param a: int, - первое слагаемое
    @param b: int, - второе слагаемое
    @return: int, - сумма приведённых слагаемых
    """
    return a + b
```

Ну и разумеется, с ходу составим парочку тестов, подтверждающих корректность выполнения написанной функции - договоримся, что будем писать тесты по принципу [**AAA**][aaa-notation] ("Arrange, Act, Assert", или "Подготовь, Выполни, Проверь"):

```python
"""модуль 'math_tests.py'"""

import pytest

import math_functions

def test_sum_integers_with_positive_integers():
    """
    Тестирование функции 'sum_integers' для двух положительных целых чисел
    """
    a = 5
    b = 7
    expected_result = 12

    real_result = math_functions.sum_integers(a, b)

    assert expected_result == real_result

def test_sum_integers_with_negative_integers():
    """
    Тестирование функции 'sum_integers' для двух отрицательных целых чисел
    """
    a = -5
    b = -7
    expected_result = -12

    real_result = math_functions.sum_integers(a, b)

    assert expected_result == real_result

def test_sum_integers_with_different_integers():
    """
    Тестирование функции 'sum_integers' для положительного и отрицательного целых чисел
    """
    a = 5
    b = -7
    expected_result = -2

    real_result = math_functions.sum_integers(a, b)

    assert expected_result == real_result
```

При наличии загруженного модуля pytest и 2-х представленных python-файлов запуск из текущего каталога тестов осуществляется с использованием инструкции:

```console
$ python3 -m pytest math_tests.py
```

Если для Вас не является загадкой использование модуля pylint, во-первых, Вы большой молодец, а во-вторых, у Вас может возникнуть справедливое замечание: "А зачем мы вообще импортировали модуль pytest, если нигде его не используем?" Подождите минутку, впереди всё самое интересное..

### Усложнение примера

Давайте расширим наш набор функций, добавив обработку целочисленного деления, стараясь учесть при этом случай деления на ноль:

```python
"""модуль 'math_functions.py'"""

...

def div_integers(a: int, b: int) -> int:
    """
    Получение частного двух целых чисел
    @param a: int, - делимое
    @param b: int, - делитель
    @raises ZeroDivision при делении на 0
    @return: int, - частное приведённых целых чисел
    """
    return a // b
```

Обработать деление корректных чисел не составляет труда, наибольший интерес составляет ситуация запрещённого во всех государствах всех планет деление на 0:

```python
"""модуль 'math_tests.py'"""

...

def test_div_integers_for_positive_integers():
    """
    Тестирование функции 'div_integers' для положительных целых чисел
    """
    a = 14
    b = 3
    expected_result = 4

    real_result = math_functions.div_integers(a, b)

    assert expected_result == real_result

def test_div_integers_for_negative_integers():
    """
    Тестирование функции 'div_integers' для отрицательных целых чисел
    """
    a = -14
    b = -3
    expected_result = 4

    real_result = math_functions.div_integers(a, b)

    assert expected_result == real_result

def test_div_integers_for_different_integers():
    """
    Тестирование функции 'div_integers' для положительного и отрицательного целых чисел
    """
    a = 14
    b = -3
    expected_result = -5    # ничего не поделать, округляем до меньшего..

    real_result = math_functions.div_integers(a, b)

    assert expected_result == real_result

def test_div_integers_for_zerodivision():
    """
    Тестирование функции 'div_integers' для положительного и отрицательного целых чисел
    """
    a = 14
    b = 0

    with pytest.raises(ZeroDivisionError):
        math_functions.div_integers(a, b)
```

Вот наконец мы и затронули сам модуль pytest: с помощью элегантного контекстного менеджера умудрились успешно отловить исключение!

### Знакомство с фикстурами

Однако в ходе разработки функции не всегда выходят такими "гладкими": не вызывают никаких внешних эффектов. На деле можно встретиться с тем, что где-то что-то создаёт временные файлы, где-то что-то "дёргает" внешний API для доступа к удалённому ресурсу или же вообще требует ввод строки от пользователя. На выручку при тестировании таких примеров тоже приходит уже любимый нами pytest

#### Работа с временными файлами

На текущий момент у нас уже имеется подготовленный на одном из [предыдущих][link-to-pz3-todo] занятий заготовленный кусочек кода для работы с классов TodoJournal. Немножко подшаманив, получим следующее:

```python
"""модуль functions.py"""

import sys
import json

class TodoJournal:
    """
    Класс для реализации todo-списка
    """

    def __init__(self,
                 path_todo: str):
        self.path_todo = path_todo

        self.name = self._parse()['name']
        self.tasks = self._parse()['tasks']

    def _parse(self):
        """
        Разбор входного json-файла
        @return: dict, - словарь с данными todo-списка
        """
        try:
            with open(self.path_todo, 'r', encoding='utf-8') as todo_file:
                data = json.load(todo_file)
            return data
        except FileNotFoundError:
            sys.exit(1)

    def _update(self, new_data: dict):
        """
        Обновление данных в todo-списке
        @param new_data: dict, - словарь с новыми данными todo-списка
        """
        with open(self.path_todo, 'w', encoding='utf-8') as todo_file:
            json.dump(
                new_data,
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    @classmethod
    def create(cls, filename: str, name: str):
        """
        Создание нового пустого todo-списка
        @param filename: str, - путь до создаваемого todo-списка
        @param name: str, - название создаваемого todo-списка
        """
        with open(filename, 'w', encoding='utf-8') as todo_file:
            json.dump(
                {'name': name, 'tasks': []},
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def add_entry(self, new_entry: str):
        """
        Добавление новой задачи
        @param new_entry: str, - новая задача
        """
        self.tasks.append(new_entry)

        new_data = {
            "name": self.name,
            "tasks": self.tasks,
        }

        self._update(new_data)

    def get_name(self):
        """
        Получение названия todo-списка
        @return: str, - название списка задач
        """
        return self.name

    def get_tasks(self):
        """
        Получение текущих задач
        @return: list, - текущий список задач
        """
        return self.tasks
```

В такой редакции мы имеем возможность:
* создавать пустой todo-список
* открывать уже созданный todo-список
* добавлять задачи в todo-список
* смотреть задачи в todo-списке

Давайте для порядочности протестируем методы приведённого класса

Но для начала заметим, что в ходе работы с сущностью TodoJournal нам приходится работать с реальными файлами. Этот факт заставляет нас думать, каким образом подсовывать каждому пользователю, получившему доступ к настоящему коду с использованием, например, СКВ git файлы с таким содержимым, которое нам и требуется? И тут на помощь нам приходит pytest с его фикстурами для работы с каталогом для обработки временных файлов.

Без ограничений общности покажем работу с одной из таких фикстур: **tmpdir**

Чтобы полнообъёмно проверить корректность написанного кода, нам необходимо покрыть тестами следующие ситуации:
* [ ] создание нового пустого todo-списка без задач
* [ ] открытие уже существующего todo-списка с задачами
* [ ] добавление в имеющийся todo-лист новых задач

Напомним, что простым языком страшным словом "фикстура" в pytest называется некоторая функция, результат которой будет использоваться в тестовых функциях. Прикинем, что для решения описания каждой из ситуаций выше нам требуется сформировать следующие объекты:
* пустой файл с определённым именем
* список задач для непустого начального файла
* сам непустой начальный файл, который мы читаем
* файл с добавленной задачей для сравнения внесённых изменений

Именно эти объекты мы и будем оборачивать в фикстуры  
Кстати, высшим пилотажем считается выделение фикстур из модулей с тестовыми функциями: все они иерархично помещаются в файлы-модули с именем 'conftest'. Создадим и мы такой же агрегирующий фикстуры файл.

##### Тестирование создания пустого json-файла

Начнём с формирования пустого файла и его названия:

```python
"""модуль 'conftest.py'"""

import os
import json

import pytest

@pytest.fixture()
def content_of_empty_todo() -> str:
    """
    Формирование пустого json-файла для todo-списка
    @return: str, - содержимое json-файла
    """
    name = 'empty_todo'
    tasks = []

    return json.dumps(
        {'name': name, 'tasks': tasks},
        indent=4,
        ensure_ascii=False,
    )

@pytest.fixture()
def attributes_of_empty_todo(tmpdir: pytest.fixture) -> tuple:
    """
    Атрибуты пустого формируемого json-файла
    @param tmpdir: pytest.fixture, - каталог для временных файлов
    @return: tuple, -
        todo_path: str, - путь до пустого формируемого json-файла,
        todo_name: str, - название пустого формируемого todo-списка
    """
    filename = 'empty_todo'
    path_to_file = os.path.join(tmpdir, filename)

    return path_to_file, filename
```

А теперь попытаемся протестировать функцию создания пустого todo-списка. Создадим тест, в котором сымитируем создание пустого json-файла для нового todo-списка, а далее проверим реальное содержимое созданного файла с ожидаемым:

```python
"""модуль 'tests.py'"""

import pytest

import functions

def test_create_empty_todo(attributes_of_empty_todo: tuple,
                           content_of_empty_todo: dict):
    """
    Тестирование метода create класса TodoJournal
    @param attributes_of_empty_todo: tuple, - кортеж с атрибутами пустого todo-списка
    @param content_of_empty_todo: str, - содержимое json-файла
    """
    empty_todo_path, _ = attributes_of_empty_todo
    expected_todo_content = content_of_empty_todo

    functions.TodoJournal.create(*attributes_of_empty_todo)
    with open(empty_todo_path, 'r', encoding='utf-8') as real_todo:
        real_todo_content = real_todo.read()

    assert expected_todo_content == real_todo_content
```

##### Тестирование чтения непустого json-файла

Проделаем то же самое для случая, когда необходимый файл уже существует и нам требуется лишь прочесть его содержимое. Для этого сформируем ожидаемый список задач, часть из которых сразу внесём в наш непустой json-файл, а часть добавим после для тестирования других методов:

```python
"""модуль 'conftest.py'"""

...

@pytest.fixture()
def tasks_for_todo() -> list:
    """
    Формирование задач для todo-списка
    @return: list, - список задач
    """
    tasks = [
        'task 1',
        'task 2',
        'task 3',
    ]

    return tasks

@pytest.fixture()
def attributes_of_todo_with_two_tasks(tmpdir: pytest.fixture,
                                      tasks_for_todo: list) -> str:
    """
    Формирование пустого json-файла для todo-списка и получение его атрибутов
    @param tmpdir: pytest.fixture, - каталог для временных файлов
    @param tasks_for_todo: list, - список из 3-х задач
    @return: tuple, -
        todo_path: str, - путь до пустого формируемого json-файла,
        todo_name: str, - название сформированного todo-списка,
        todo_tasks: list, - список задач в сформированном json-файла
    """
    filename = 'todo_with_two_tasks'
    path_to_file = os.path.join(tmpdir, filename)
    tasks = tasks_for_todo[:2]

    with open(path_to_file, 'w', encoding='utf-8') as todo_file:
        json.dump(
            {'name': filename, 'tasks': tasks},
            todo_file,
            indent=4,
            ensure_ascii=False,
        )

    return path_to_file, filename, tasks
```

Ну и далее сымитируем ситуацию чтения уже сформированного json-файла с 2-мя заданиями, т.е. протестируем конструктор нашего класса TodoJournal:

```python
"""модуль 'tests.py'"""

...

def test_init_for_todo_with_two_tasks(attributes_of_todo_with_two_tasks: tuple):
    """
    Тестирование конструктора и методов get_name и get_tasks класса TodoJournal
    @param attributes_of_todo_with_two_tasks: tuple, - кортеж атрибутов json-файла
    """
    path_to_todo, expected_name, expected_tasks = attributes_of_todo_with_two_tasks

    real_todo = functions.TodoJournal(path_to_todo)

    assert expected_name == real_todo.get_name()
    assert expected_tasks == real_todo.get_tasks()
```

##### Тестирование добавления новых задач

Фикстуру для настоящего теста будем строить на базе уже имеющегося списка из 3-х задач:

```python
"""модуль 'conftest.py'"""

...

@pytest.fixture()
def attributes_of_todo_with_three_tasks(tmpdir: pytest.fixture,
                                        tasks_for_todo: list) -> str:
    """
    Формирование json-файла с 3-мя заданиями для todo-списка и получение его атрибутов
    @param tmpdir: pytest.fixture, - каталог для временных файлов
    @param tasks_for_todo: list, - список из 3-х задач
    @return: tuple, -
        todo_path: str, - путь до пустого формируемого json-файла,
        todo_name: str, - название сформированного todo-списка,
        todo_tasks: list, - список задач в сформированном json-файла
    """
    filename = 'todo_with_three_tasks'
    path_to_file = os.path.join(tmpdir, filename)
    tasks = tasks_for_todo

    with open(path_to_file, 'w', encoding='utf-8') as todo_file:
        json.dump(
            {'name': filename, 'tasks': tasks},
            todo_file,
            indent=4,
            ensure_ascii=False,
        )

    return path_to_file, filename, tasks
```

Сам же тест пусть расширяет аналогичный для предыдущего случая:

Ну и далее сымитируем ситуацию чтения уже сформированного json-файла с 2-мя заданиями, т.е. протестируем конструктор нашего класса TodoJournal:

```python
"""модуль 'tests.py'"""

...

def test_add_entry_for_todo(attributes_of_todo_with_two_tasks: tuple,
                            attributes_of_todo_with_three_tasks: tuple,
                            tasks_for_todo: list):
    """
    Тестирование метода add_entry класса TodoJournal
    @param attributes_of_todo_with_two_tasks: tuple, - кортеж атрибутов json-файла c 2-мя заданиями
    @param attributes_of_todo_with_three_tasks: tuple, - кортеж атрибутов json-файла с 3-мя -//-
    @param tasks_for_todo: list, - список из 3-х задач
    """
    # работа с todo-списком с 2-мя задачами
    path_to_todo, _, expected_tasks = attributes_of_todo_with_two_tasks

    real_todo = functions.TodoJournal(path_to_todo)

    assert expected_tasks == real_todo.get_tasks()

    # добавление новой задачи в todo-список
    new_task = tasks_for_todo[2]

    real_todo.add_entry(new_task)

    # работа с todo-списком с 3-мя задачами
    path_to_todo, _, expected_tasks = attributes_of_todo_with_three_tasks

    assert expected_tasks == real_todo.get_tasks()
```

##### Тестирование попытки прочитать несуществующий todo-список

В качестве вишенки на торте закрепим полученные выше знания, относящиеся к обработке исключительных ситуаций с использованием модуля pytest. В случае несуществующего файла при попытке открытия должно быть сгенерирована системная ошибка:

```python
"""модуль 'tests.py'"""

...

def test_init_with_systemexit(path_to_non_existed_todo: str):
    """
    Тестирование генерации системной ошибки при отсутствии файла
    @param path_to_non_existed_todo: str, - путь до несуществующего файла
    """
    with pytest.raises(SystemExit):
        functions.TodoJournal(path_to_non_existed_todo)
```

Для реализации настоящего теста сформируем простую фикстуру:

```python
"""модуль 'conftest.py'"""

...

@pytest.fixture()
def path_to_non_existed_todo(tmpdir: pytest.fixture) -> str:
    """
    Формирование пути до несуществующего json-файла с todo-списком
    @param tmpdir: pytest.fixture, - каталог для временных файлов
    @return: str, - путь до несуществующего файла
    """
    filename = 'non_existed_todo'
    path_to_file = os.path.join(tmpdir, filename)

    return path_to_file
```

#### Покрытие кода тестами

В настоящий момент настало время оценить, насколько же хорошо было выполнено тестирование представленного фрагмента кода! Для этого воспользуемся плагином pytest'а под названием pytest-cov или же модулем самого python с названием coverage, на базе которого, к слову, построен выше упомянутый плагин..

Для того, чтобы проверить, сколько строчек покрыто тестами с помощью модуля **coverage**, требуется выполнить следующие команды:

```console
$ python3 -m coverage run -m pytest *tests.py
$ python3 -m coverage report -m
```

На экран Вам будет выведена таблица некоторого формата с предоставлением информации о том:
* какой модуль оценивается
* сколько строчек именно кода в этом модуле
* сколько строчек кода в этом модуле не покрыто тестами
* процент покрытия кода модуля тестами
* строки, которые не были покрыты тестами

Удобно? Да не то слово! Правда, модулей многовато: полно служебных, которые Вы явно даже не дёргали в ходе работы.. Проблема кроется в том, что мы не настроили конфигурационный файл для модуля coverage. Давайте же сделаем это.

Сформируем файл с названием **.coveragerc** со следующим содержимым:

```bash
[run]
include =
    ./*.py
omit =
    *tests.py
    conftest.py

[report]
exclude_lines =
    if __name__ == '__main__':
```

В секции `[run]` мы укажем, что хотим анализировать все python-файлы в текущем каталоге, кроме файлов, относящихся к тестам с названиями, включающими 'tests.py', и фикстурам с названием 'conftest.py'. В секции `[report]` мы отметим, что не хотим учитывать в отчёте строки кода в блоке выполнения python-файла как самостоятельного модуля

Однако заметим, что всё выше перечисленное можно было сделать чуть элегантнее с использованием упомянутого плагина **pytest-cov**, выполнив следующую инструкцию в терминале (если Вы выполняете это так же последовательно, как представлено здесь, убедительная просьба удалить сформированный конфигурационный файл .coveragerc во избежание испуга от предупреждения в выводе отработки плагина):

```console
$ python3 -m pytest --cov=. *tests.py
```

Мы видим ту же статистику, решая поставленную задачу анализа покрытия нашего кода тестами! Вуаля)

#### Структура учебного репозитория

Согласуем нашу работу для удобства в дальнейшем  
В текущий момент у Вас должна быть следующая структура репозитория:
* .coveragerc - конфигурационный файл для модуля coverage
* conftest.py - модуль с фикстурами для тестов
* math_functions.py - модуль с самописными математическими функциями целочисленных сложения и деления
* math_tests.py - тесты для модуля с самописными математическими функциями
* functions.py - модуль с реализацией класса TodoJournal
* tests.py - тесты для методом класса TodoJournal

При выполнении тестирования должна быть примерно такая картина:

```console
$ python3 -m coverage run -m pytest *tests.py

math_tests.py .......                   [ 63%]
tests.py ....                           [100%]
============= 11 passed in 0.03s =============


$ python3 -m coverage report -m

Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
functions.py           29      0   100%
math_functions.py       4      0   100%
-------------------------------------------------
TOTAL                  33      0   100%
```

Если перенимать лучшие практики разработки, стоит чуть пересмотреть структуру нашего рабочего репозитория: давайте вынесем модули, содержащие исходный код, и модули, содержащие тестовые файлы, в отдельные каталоги **src/** и **tests/** соответственно. Для того, чтобы не мудрить с относительными путями при импортировании модулей, обернём все наши модули в python-пакет: для этого в каждом из вновь созданных каталогах добавим пустой файл \_\_init\_\_.py

Для совсем хорошей картины сформируем ещё и файл .gitignore - мы же всё-таки работаем с СКВ git, Вы же ещё про это не забыли!? - со следующим содержимым:

```
**/__pycache__/
.coverage
```


В итоге структура проекта будет следующей:
* .gitignore - конфигурационный файл СКВ git, включающий игнорируемые объекты
* .coveragerc - конфигурационный файл для модуля coverage
* каталог src, содержащий исходный код
   * \_\_init\_\_.py
   * math_functions.py - модуль с самописными математическими функциями целочисленных сложения и деления
   * functions.py - модуль с реализацией класса TodoJournal
* каталог tests, содержащий тесты
   * \_\_init\_\_.py
   * conftest.py - модуль с фикстурами для тестов
   * math_tests.py - тесты для модуля с самописными математическими функциями
   * tests.py - тесты для методом класса TodoJournal

Конфигурационный файл .coveragerc должен быть изменён до следующего вида:

```bash
[run]
include =
    src/*
omit =
    tests/*
    **/__init__.py

[report]
exclude_lines =
    if __name__ == '__main__':
```

Запуск модуля pytest для тестирования написанного должно осуществляться из корня проекта следующим образом:

```console
$ python3 -m coverage run -m pytest tests/*
$ python3 -m coverage report -m
```

#### Работа с подменой данных в ходе тестирования

Рассмотрим другой пример встроенной фикстуры, относящийся к подмене результатов выполнения некоторых функций заведомо определёнными значениями, - **monkeypatch**. Как говорилось ранее, эта фикстура может быть использована для реализации, например, следующих целей:
* [ ] ожидание интерактивного ввода значения от пользователя
* [ ] использование внешнего API, обращающегося к некоторым ресурсам
* [ ] ускорение времени выполнения некоторых функций

Без ограничений общности рассмотрим первые 2 ситуации

##### Работа с пользовательским вводом

Давайте дополним работу с классом возможностью добавления задачи, введённой пользователем. Пусть при вызове соответствующего метода класса TodoJournal пользователю в командной строке предлагается некоторое сообщение-приглашение для ввода данных, а после такового указанное задание добавляется в список задач и отражается в файле:

```python
"""модуль 'src/functions.py'"""

...

class TodoJournal:
    ...

    def add_entry_by_user(self):
    """
    Добавление новой задачи пользователем
    """
    self.tasks.append(input('Введите задачу: '))

    new_data = {
        "name": self.name,
        "tasks": self.tasks,
    }

    self._update(new_data)
```

Видоизменим уже написанный тест для проверки добавления задачи в список для нового описанного выше метода:

```python
"""модуль 'tests/tests.py'"""

from io import StringIO

...

def test_add_entry_by_user_for_todo(attributes_of_todo_with_two_tasks: tuple,
                                    attributes_of_todo_with_three_tasks: tuple,
                                    tasks_for_todo: list,
                                    monkeypatch: pytest.fixture):
    """
    Тестирование методов add_entry_by_user класса TodoJournal
    @param attributes_of_todo_with_two_tasks: tuple, - кортеж атрибутов json-файла c 2-мя заданиями
    @param attributes_of_todo_with_three_tasks: tuple, - кортеж атрибутов json-файла с 3-мя -//-
    @param tasks_for_todo: list, - список из 3-х задач
    @param monkeypatch: pytest.fixture, - механизм подмены данных
    """
    # работа с todo-списком с 2-мя задачами
    path_to_todo, _, expected_tasks = attributes_of_todo_with_two_tasks

    real_todo = functions.TodoJournal(path_to_todo)

    assert expected_tasks == real_todo.get_tasks()

    # добавление новой задачи в todo-список
    new_task = StringIO(f'{tasks_for_todo[2]}\n')

    monkeypatch.setattr('sys.stdin', new_task)

    real_todo.add_entry_by_user()

    # работа с todo-списком с 3-мя задачами
    path_to_todo, _, expected_tasks = attributes_of_todo_with_three_tasks

    assert expected_tasks == real_todo.get_tasks()
```

В примере выше следует обратить внимание на то, как изменился фрагмент во втором блоке теста - `Act` в нотации AAA: мы в качестве программиста явно указали модулю pytest на то, что в случае встречи с вводом данных из стандартного потока ввода необходимо возвращать сформированное определённым образом значение, т.е. мы ставим в однозначное соответствие каждый запрос на ввод данных с клавиатуры и заранее подготовленное значениезаведомо

##### Работа с внешним API

Поставим следующую задачу: в рамках локально развёрнутого на кафедре экземпляра Gitlab с доменным именем gitwork.ru создать проект или же продолжить работу в Вашем репозитории для выполнения заданий по текущей дисциплине, создать - если таковые отсутствуют - несколько issues в Вашем проекте, а далее транслировать это в новый todo-список

Давайте потихоньку - делая поправку на то, что с библиотекой для работы с API Gitlab Вы ещё не работали, - начнём осваиваться. Для начала обсудим, что нам требуется сделать для того, чтобы получить список задач с удалённого экземпляра Gitlab:
1. сгенерировать access-токен для работы с Gitlab с помощью скриптов 
2. подключиться к экземпляру Gitlab с использованием сгенерированного access-токена
3. получить доступ к конкретному проекту экземпляра Gitlab
4. получить отсортированный некоторым образом список всех issues рабочего проекта экземпляра Gitlab
5. сформировать todo-список из полученных задач

Пункт №1 выполняется без единой строчки кода: Вам необходимо отыскать вкладку со свойствами своего профиля (нажатие ЛКМ на Вашем аватаре в правом верхнем углу экрана, далее ЛКМ на вкладке preferences, или свойства), в свойствах отыскать вкладку Access Tokens (ЛКМ на вкладке с соответствующим именем в левой части экрана) и сгенерировать api-токен

Ниже приведём фрагмент кода, необходимого для решения задач 2-4:

```python
"""модуль 'src/gitlab_functions.py'"""

import gitlab

class IssuesHandler:
    """
    Класс для работы с экземпляром Gitlab
    """

    def __init__(self,
                 url: str,
                 token: str,
                 project_namespace: str):
        """
        Конструктор класса 'GitlabControl'
        @param url: str, - URL-адрес экземпляра Gitlab
        @param token: str, - api-токен пользователя
        @param project_namespace: str, - пространство видимости и название проекта
        """
        self.url = url
        self.token = token
        self.project_namespace = project_namespace

        # получение доступа к экземпляру Gitlab
        self.gitlab = gitlab.Gitlab(url=self.url, private_token=self.token, ssl_verify=False)

        # поиск нужного проекта экземпляра Gitlab
        self.project = self.gitlab.projects.get(self.project_namespace)

        # обращение к задачам нужного проекта экземпляра Gitlab
        self.issues = self.project.issues.list(order_by='created_at', sort='asc')

    def get_tasks(self):
        """
        Получение списка задач
        """
        tasks = []

        for issue in self.issues:
            tasks.append(issue.title)

        return tasks
```

Разберём, что же за волшебство представлено выше: обращая внимание на конструктор предложенного класса, можем заметить, что, используя 2 из 3 указанных входных параметра, удаётся получить доступ к указанному экземпляру Gitlab; 3-ий параметр необходим для того, чтобы отсеять ненужные проекты, получив искомый; после получения проекта с лёгкостью удаётся обратиться к каждой из задач, сортируя их, как нам удобно

Давайте теперь предложим вариант для того, чтобы на базе полученных данных сформировать нужный нам todo-лист:

```python
"""модуль 'src/functions.py'"""

...

from src import gitlab_functions

class TodoJournal:
    ...

    @classmethod
    def create_from_gitlab(cls, filename: str, url: str, token: str, project_namespace: str):
        """
        Создание нового пустого todo-списка на основе задач проекта экземпляра Gitlab
        @param filename: str, - путь до создаваемого todo-списка
        @param url: str, - URL-адрес экземпляра Gitlab
        @param token: str, - api-токен пользователя
        @param project_namespace: str, - пространство видимости и название проекта
        """
        _, name = project_namespace.split('/')

        issues_handler = gitlab_functions.IssuesHandler(url, token, project_namespace)
        tasks = issues_handler.get_tasks()

        with open(filename, 'w', encoding='utf-8') as todo_file:
            json.dump(
                {'name': name, 'tasks': tasks},
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )
```

Приведённый выше метод позволяет создать новый todo-список, опираясь на его название и аутентификационные данные пользователя экземпляра Gitlab

Для проверки корректности представленного кода добавьте следующий блок обработки, подставив в соответствующие места свои API-токен и название Вашего исследуемого проекта - например, `user/project` для проекта с названием 'project' пользователя с логином 'user':

```python
"""модуль 'src/functions.py'"""

...

import urllib3

if __name__ == '__main__':
    # добавление инструкций для игнорирования несущественных предупреждений SSL
    urllib3.disable_warnings()
    
    # определение значений необходимых параметров
    NAME = 'test'
    URL = 'https://gitwork.ru/'
    TOKEN = 'место-для-Вашего-токена'
    PROJECT_NAMESPACE = 'место-для-Вашего-проекта'

    TodoJournal.create_from_gitlab(f'{NAME}.todo', URL, TOKEN, PROJECT_NAMESPACE)
    TODO_LIST = TodoJournal(f'{NAME}.todo')
    print(TODO_LIST.get_tasks())
```

Однако как же теперь всё это тестировать?  
В таком варианте не получается с лёгкой руки взять и, например, подставить вместо значения функции get_tasks класса IssuesHandler нужное нам значение: нам предлагается подменить целый объект, который мы и будем использовать для имитации работы этой функции - никакого мошенничества: только знания, умения и щепотка внимательности

Обратим внимание на то, что заменять в таких ситуациях нам требуется самый крупный объект: это логично, ведь всего его составные части и так будут имитировать заведомо заложенное нами поведение. Выделим же его: что это может быть?

* [ ] конкретная задача, воспроизводящая атомарное issue
* [ ] список задач, воспроизводящий результата выполнения функции list для проекта
* [ ] сам проект экземпляра Gitlab
* [x] непосредственно экземпляр Gitlab

Теперь следует разобраться с тем, какое поведение ожидается от имитируемого нами экземпляра Gitlab?
1. объект должен иметь конструктор, т.е. должна быть реализована возможность создать объект, причём создать его можно, указав в нашем случае 3 параметра:
   * URL-адрес с доменным адресом экземпляра Gitlab
   * access-токен пользователя, выполняющего работу с Gitlab
   * индикатор игнорирования проверки SSL-сертификата экземпляра Gitlab
2. у объекта должен быть атрибут **projects**, имитирующий работу объекта класса ProjectManager - тип можно выявить, если чуть "поиграть" в отладке, который в свою очередь сам является объектом, который способен вызвать метод get
3. ну и разумеется, сам объект, полученный с помощью метода get, должен иметь атрибут **issues**, имитирующий работу объекта класса ProjectIssuesManager, который в свою очередь - так же, как и **projects** является объектом, который имеет, правда, другой ценный для нас метод list
4. объект, полученный с помощью метода list, есть ни что иное как список конкретных задач, которые тоже представляются в виде объектов, у которых есть атрибут title - название конкретной issue - ключевой для нас параметр!

Хух.. Структура действительно сложная, но не сказать, что неподъёмная. Давайте разбираться!

Для начала наметим в модуле с фикстурами классы-заглушки (сленг для mock-объектов) для каждой из 4-х позиций, начиная с самой мелкой:

```python
"""модуль 'tests/conftest.py'"""

...

class MockIssue:
    """
    Класс для имитации объекта-задачи
    """

    def __init__(self, title: str):
        self.title = title

class MockProjectIssuesManager:
    """
    Класс для имитации менеджера обработки списка задач
    """

    def __init__(self):
        self.issues = []
    
    def append(self, task: str):
        """
        Добавление новой задачи в список
        @param task: str, - новая задача
        """
        self.issues.append(MockIssue(task))

    def list(self, order_by: str = 'created_at', sort: str = 'asc') -> list:
        """
        Получение списка всех задач
        @return: list, - список всех задач
        """
        return self.issues

class MockProject:
    """
    Класс для имитации объекта-проекта экземпляра Gitlab
    """

    def __init__(self, project_tasks: list):
        self.issues = MockProjectIssuesManager()

        for task in project_tasks:
            self.issues.append(task)

class MockProjectManager:
    """
    Класс для имитации менеджера обработки проектов экземпляра Gitlab
    """

    def __init__(self):
        self.projects = []
    
    def append(self, project_tasks: list):
        """
        Добавление нового проекта в список
        @param project_tasks: list, - список issues проекта
        """
        self.projects.append(MockProject(project_tasks))

    def get(self, project_namespace: str) -> MockProject:
        """
        Получение конкретного проекта (последнего в списке)
        @param project_namespace: str, - пространство проекта экземпляра Gitlab
        @return: MockProject, - проект экземпляра Gitlab
        """
        return self.projects[-1]

class MockGitlab:
    """
    Класс для имитации экземпляра Gitlab
    """

    def __init__(self):
        self.projects = MockProjectManager()
```

Также стоит создать фикстуру для того, чтобы понимать, где искать создаваемый файл со списком задач проекта экземпляра Gitlab: разумеется, делать мы это будем во временном каталоге

```python
"""модуль 'tests/conftest.py'"""

...

@pytest.fixture()
def path_to_todo_created_from_gitlab(tmpdir: pytest.fixture) -> str:
    """
    Формирование пути до json-файла с todo-списком задач из Gitlab-проекта
    @param tmpdir: pytest.fixture, - каталог для временных файлов
    @return: str, - путь до json-файла
    """
    filename = 'todo_from_gitlab'
    path_to_file = os.path.join(tmpdir, filename)

    return path_to_file
```

Теперь создадим дополнительную фикстуру, которая будет возвращать нам объект класса MockGitlab, наполнив её нужными нам задачами из предыдущих примеров:

```python
"""модуль 'tests/conftest.py'"""

...

@pytest.fixture()
def mocked_issues_handler_with_three_tasks(tasks_for_todo: list) -> MockGitlab:
    """
    Подмена конструктора класса gitlab.Gitlab
    @param tasks_for_todo: list, - список из 3-х задач
    """
    mocked_issued_handler = MockGitlab()

    mocked_issued_handler.projects.append(tasks_for_todo)

    return mocked_issued_handler
```

Ну а теперь настало время самих тестов! Опираясь на чудесное [руководство][monkeypatch-examples], сформируем следующую тестовую функцию:

```python
"""модуль 'tests/tests.py'"""

...

def test_create_from_gitlab(monkeypatch: pytest.fixture,
                            path_to_todo_created_from_gitlab: str,
                            tasks_for_todo: list,
                            mocked_issues_handler_with_three_tasks: MockGitlab):
    """
    Тестирование работы конструктора класса 'SlushListsHandler'
    @param monkeypatch: pytest.fixture, - модуль для формирования заглушек
    @param path_to_todo_created_from_gitlab: str, - путь до json-файла с задачами Gitlab-проекта
    @param @param tasks_for_todo: list, - список из 3-х задач
    @param mocked_issues_handler_with_three_tasks: MockGitlab, - объект класса-заглушки для экземпляра Gitlab
    """
    url = 'https://non-existed-gitlab.test/'
    token = 'private-token'
    project = 'namespace/project'

    _, expected_name = project.split('/')
    expected_tasks = tasks_for_todo

    # pylint: disable=unused-argument
    def mocked_gitlab_init(url: str,
                           private_token: str,
                           ssl_verify: bool = True) -> MockGitlab:
        """
        Конструктор-заглушка для экземпляра Gitlab
        @param url: str, - URL-адрес экземпляра Gitlab
        @param private_token: str, - приватный токен пользователя экземпляра Gitlab
        @param ssl_verify: bool, - индикатор проверки SSL-сертификатов экземпляра Gitlab (по умолчанию: True)
        @return: MockGitlab, - объект класса-заглушки для экземпляра Gitlab
        """
        return mocked_issues_handler_with_three_tasks
    # pylint: enable=unused-argument

    monkeypatch.setattr(gitlab_functions.gitlab, 'Gitlab', mocked_gitlab_init)

    functions.TodoJournal.create_from_gitlab(path_to_todo_created_from_gitlab, url, token, project)
    real_todo = functions.TodoJournal(path_to_todo_created_from_gitlab)

    assert expected_name == real_todo.get_name()
    assert expected_tasks == real_todo.get_tasks()
```

В тесте выше мы вырождаем URL-адрес экземпляра Gitlab и приватный токен пользователя, а также название проекта. Используя небольшие изощрения подменяем конструктор класса Gitlab модуля gitlab на самописный аналог. Далее создаём во временном каталоге нужный нам файл и проверяем, что заглушённый объект правильно себя повёл.

Если всё сделано правильно, Вы следили за ходом обработки и ничего не упустили, после запуска тестирования Вы должны получить примерно следующий результат:

```console
$ python3 -m coverage run -m pytest tests/*

math_tests.py .......                   [ 53%]
tests.py ......                         [100%]
============= 13 passed in 0.21s =============


$ python3 -m coverage report -m

Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/functions.py             42      0   100%
src/gitlab_functions.py      15      0   100%
src/math_functions.py         4      0   100%
-------------------------------------------------------
TOTAL                        61      0   100%
```

#### В качестве комплимента

Кстати, можно было использовать ещё больше фикстур: это было бы более элегантно и гибко. На мой взгляд, создавать сущности, скрываемые за monkeypatch нужно с умом, осмысленно: каждая сущность должна показывать, как на самом деле она выглядит

Так, например, последний тест можно было бы сымитировать ещё лучше, разбавив код всё новыми фикстурами:

```python
"""модуль 'conftest.py'"""

...

import string
import secrets

...

@pytest.fixture()
def gitlab_url() -> str:
    """
    Формирование URL-адреса тестового экземпляра Gitlab
    @return: str, - пример URL-адреса тестового экземпляра Gitlab
    """
    return 'https://non-existed-gitlab.local.temp'


@pytest.fixture()
def gitlab_private_token() -> str:
    """
    Формирование приватного токена для работы с тестовым экземпляром Gitlab
    @return: str, - пример приватного токена тестового экземпляра Gitlab
    """
    lower_letters = string.ascii_lowercase
    upper_letters = string.ascii_uppercase
    digits = string.digits

    token_length = 20
    token = ''.join(secrets.choice(secrets.choice([lower_letters, upper_letters, digits])) for _ in range(token_length))
    token = f'glpat-{token}'

    return token
```


[pytest-manual-in-pdf]: http://library.sadjad.ac.ir/opac/temp/18467.pdf
[pytest-manual-in-md]: https://habr.com/ru/post/448782/

[aaa-notation]: https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html

[link-to-pz3-todo]: ./pz3-todo.md

[monkeypatch-examples]: https://www.patricksoftwareblog.com/monkeypatching-with-pytest/
