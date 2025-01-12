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

## Ansible playbooks:
```bash
# main playbook
- name: main playbook project
  hosts: localhost

- ansible.builtin.import_playbook: playbooks/build_and_push_docker_image.yml
- ansible.builtin.import_playbook: playbooks/pull_and_up_docker_compose.yml

# build_and_push_docker_image
- name: Build and push docker image project
  hosts: "{{ build_and_push_docker_image_playbook_host }}"
  become: yes

  vars_files:
    - /root/wallet_project/ansible/playbook_vars/docker_vars.yml
    - /root/wallet_project/ansible/playbook_vars/retry_task_vars.yml

  tasks:
    - include_tasks: tasks/login_to_docker.yml

    - name: Down Docker compose
      community.docker.docker_compose_v2:
        project_src: "{{ project_path }}"
        state: absent

    - name: Remove
      community.docker.docker_image_remove:
        name: "{{ docker_username }}/{{ docker_image }}"
        tag: "{{ docker_image_tag }}"
      retries: "{{ retries_count }}"
      delay: "{{ delay_time }}"

    - name: Build
      community.docker.docker_image_build:
        name: "{{ docker_username }}/{{ docker_image }}"
        tag: "{{ docker_image_tag }}"
        path: "{{ dockerfile_path }}"
        platform: "{{ docker_image_platform }}"
      retries: "{{ retries_count }}"
      delay: "{{ delay_time }}"

    - name: Push
      community.docker.docker_image_push:
        name: "{{ docker_username }}/{{ docker_image }}"
        tag: "{{ docker_image_tag }}"
      retries: "{{ retries_count }}"
      delay: "{{ delay_time }}"

    - include_tasks: tasks/docker_prune.yml

# pull_and_up_docker_compose
- name: Restart docker compose images
  hosts: "{{ pull_and_up_docker_compose_playbook_host }}"
  become: yes

  vars_files:
    - /root/wallet_project/ansible/playbook_vars/docker_vars.yml
    - /root/wallet_project/ansible/playbook_vars/retry_task_vars.yml

  tasks:
    - include_tasks: tasks/login_to_docker.yml

    - name: Pull
      community.docker.docker_compose_v2_pull:
        project_src: "{{ project_path }}"
      retries: "{{ retries_count }}"
      delay: "{{ delay_time }}"

    - name: Up
      community.docker.docker_compose_v2:
        project_src: "{{ project_path }}"
      register: output
      retries: "{{ retries_count }}"
      delay: "{{ delay_time }}"

    - include_tasks: tasks/docker_prune.yml
```
