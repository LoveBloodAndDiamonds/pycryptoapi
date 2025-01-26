
# pycryptoapi

## Установка:

### Без дополнительных зависимостей:

#### Через pip:
```bash
pip install git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git@main
```

#### Через poetry:
```bash
poetry add git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git
```

---

### С дополнительной поддержкой Redis:

Если вам нужен функционал, связанный с Redis, установите библиотеку с опциональной зависимостью `redis`.

#### Через pip:
```bash
pip install git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git@main#egg=pycryptoapi[redis]
```

#### Через poetry:
```bash
poetry add git+https://github.com/LoveBloodAndDiamonds/pycryptoapi.git[redis]
```

---

### Примечания:
- Опциональные зависимости позволяют избежать установки ненужных библиотек, если вы не используете их функционал.
- Для использования Redis необходимо дополнительно установить его сервер на вашей машине или подключиться к удаленному серверу Redis.
