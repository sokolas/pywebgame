# pywebgame
pygame + fastapi test

# перед установкой
* создать venv
* активировать
* установить зависимости: `python3 -m pip install -U fastapi websockets uvicorn pygame`

# запуск
Из каталога src
Для сервера: `python3 main.py server`
Для клиента: `python3 main.py client`

После запуска игры можно открыть `web/index.html` в браузере, и туда будут приходить сообщения обо всех перемещениях игроков.
