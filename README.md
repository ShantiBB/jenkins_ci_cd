# Этот проект добавляет и запускает в jenkins ansible playbook.

- Сначала идет проверка линтером ruff и тестируются эндпоинты проекта через pytest.  
- Затем идет деплой проекта на удаленный сервер.  

В проект вндерен webhook github, который при коммите запускает job с тестами, затем после успешного завершения запускается job с деплоем.

## Скрипт первой job:
```bash
#!/bin/bash
echo "Перенос .env файла в репозиторий"
cp src_path dest_path

echo "Запуск  docker"
sudo systemctl start docker

echo "Запуск docker compose"
sudo docker compose -f docker/docker-compose.yml up --build -d

echo "Установка и активация окружения poetry"
python3.12 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --no-root

echo "Тест линтером ruff"
ruff check

echo "Тест эндпоинтов через pytest"
pytest -v

echo "Отключение docker"
sudo systemctl stop docker
sudo systemctl stop docker.socket
```
## Скрипт второй job:
```bash
echo "Активация ansible playbook"
cd ansible
ansible-playbook playbook.yml
```
