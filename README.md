# REST API для управления обменными курсами валют

В данном проекте реализован `REST API` на `FastAPI` для управления обменным курсом валют.

Стэк: `Python`, `FastAPI`, `SQLAlchemy`, `Pydantic`, `PostgreSQL`, `Alembic`, `BeautifulSoup`, `Poetry`

Скриншот из автосгенерировнного `OpenAPI` (ПЕРЕПИСАТЬ) через `FastAPI`:

![rest.png](docs/rest.png)

## База данных

### Таблица currencies

| Колонка | Тип     | Описание          |
|---------|---------|-------------------|
| id      | int     | ID валюты         |
| code    | varchar | Код валюты        |
| name    | varchar | Полное имя валюты |

### Таблица exchange_rates

| Колонка            | Тип   | Описание                                                    |
|--------------------|-------|-------------------------------------------------------------|
| id                 | int   | ID обменного курса                                          |
| base_currency_id   | int   | ID базовой валюты                                           |
| target_currency_id | int   | ID целевой валюты                                           |
| rate               | float | Курс обмена единицы базовой валюты к единице целевой валюты |

## Реализованные API

### `/currencies`

API для создания валют в базе данных валют. Реализован CRUD для создания валют в базе данных `currancies`.

Пример выполнения GET запроса `/currencies`:

```json
[
  {
    "id": 32,
    "code": "HKD",
    "name": "Hong Kong dollar"
  },
  {
    "id": 33,
    "code": "IDR",
    "name": "Indonesian rupiah"
  }
]
```

### `/exchange_rates`

API для создания обменного курса мужд двумя валютами. Реализован CRUD для создания обменного курса между валютами в базе
данных `exchange_rates`.

Пример выполнения GET запроса `/exchange_rates`:

```json
[
  {
    "id": 11,
    "base_currency": {
      "id": 16,
      "code": "BGN",
      "name": "Bulgarian lev"
    },
    "target_currency": {
      "id": 11,
      "code": "EUR",
      "name": "Euro"
    },
    "rate": 1.9558
  }
]
```

### `/exchange`

API для расчета обменного курса между валютами A и B. 

Получение курса для обмена может пройти по одному из трёх сценариев. Допустим, совершаем перевод из валюты A в валюту B:
- В таблице `exchange_rates` существует валютная пара A-B => берём её курс
- В таблице `exchange_rates` существует валютная пара B-A => берем её курс, и считаем обратный, чтобы получить A-B
- В таблице `exchange_rates` существуют валютные пары A-EUR и B-EUR => вычисляем из этих курсов курс A-B

Пример выполнения GET запроса `/exchange`:

```json
{
  "base_currency": {
    "id": 41,
    "code": "SGD",
    "name": "Singapore dollar"
  },
  "target_currency": {
    "id": 43,
    "code": "ZAR",
    "name": "South African rand"
  },
  "rate": 0.07201245814530854,
  "amount": 2,
  "converted_amount": 0.1440249163
}
```

### `/parse`

API для заполнения баз данных `currencies` и `exchange_rates`. Валюты и обменные курсы парсятся через `BeautifulSoup` с
сайта https://www.iban.com/exchange-rates

## Установка и запуск

### Установка через виртуальное окружение

```bash
# Клонируйте репозиторий:
git clone https://github.com/kudrmax/exchange-rates
cd exchange-rates

# Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate

# Установите зависимости:
pip install -r requirements.txt

# Запустить PostgreSQL через Docker
# ДОПИСАТЬ

# Запустить миграции через Alembic
# ДОПИСАТЬ

# Запустите приложение:
python main.py  # python3 для UNIX-систем
```

Откройте браузер и перейдите по адресу [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Установка через Poetry

```bash
# Клонируйте репозиторий:
git clone https://github.com/kudrmax/exchange-rates
cd exchange-rates

# Установите Poetry, если он не установлен

# Создайте виртуальное окружение и установите зависимости:
poetry install

# Активируйте виртуальное окружение:
poetry shell

# Запустить PostgreSQL через Docker
# ДОПИСАТЬ

# Запустить миграции через Alembic
# ДОПИСАТЬ

# Запустите приложение:
python main.py  # python3 для UNIX-систем
```

Откройте браузер и перейдите по адресу [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Автор

- **Макс Кудряшов**: студент 4 курса «Прикладной математики» НИУ ВШЭ.
- Другие проекты: [GitHub](https://github.com/kudrmax/)
- Связаться: [Telegram](https://t.me/kudrmax)
