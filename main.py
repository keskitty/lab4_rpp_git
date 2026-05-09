import os
import csv


class Post:
    """Класс, описывающий один пост."""

    def __init__(self, post_id, author, text, likes):
        self.__dict__['_Post__data'] = {}
        self.id = post_id
        self.author = author
        self.text = text
        self.likes = likes

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
            return

        if key == 'id':
            self.__data["№"] = int(value)
        elif key == 'author':
            self.__data["Ник автора"] = value
        elif key == 'text':
            self.__data["Текст поста"] = value
        elif key == 'likes':
            self.__data["Кол-во лайков"] = int(value)
        else:
            raise AttributeError(f"Нельзя задать свойство '{key}'")

    def __getattr__(self, key):
        if key == 'id':
            return self.__data.get("№")
        elif key == 'author':
            return self.__data.get("Ник автора")
        elif key == 'text':
            return self.__data.get("Текст поста")
        elif key == 'likes':
            return self.__data.get("Кол-во лайков")
        raise AttributeError(f"Свойство '{key}' не найдено")

    def __repr__(self):
        return str(self.__data)

    def to_dict(self):
        return self.__data.copy()

    @staticmethod
    def from_dict(data):
        return Post(
            post_id=int(data["№"]),
            author=data["Ник автора"],
            text=data["Текст поста"],
            likes=int(data["Кол-во лайков"])
        )


class PostCollection:
    """Коллекция постов с итератором и доступом по индексу."""

    def __init__(self, posts=None):
        self._posts = posts if posts is not None else []

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._posts):
            post = self._posts[self._index]
            self._index += 1
            return post
        else:
            raise StopIteration

    def __getitem__(self, index):
        return self._posts[index]

    def __len__(self):
        return len(self._posts)

    def append(self, post):
        self._posts.append(post)

    def get_all(self):
        return self._posts

    @staticmethod
    def count_likes_above(posts, threshold):
        count = 0
        for p in posts:
            if p.likes > threshold:
                count += 1
        return count


class PostManager(PostCollection):
    """Наследование от PostCollection."""

    def sort_byname(self):
        result = sorted(self._posts, key=lambda x: x.author)
        return PostManager(result)

    def sort_bylike(self):
        result = sorted(self._posts, key=lambda x: x.likes, reverse=True)
        return PostManager(result)

    def filter_like(self):
        result = [x for x in self._posts if x.likes > 10000]
        return PostManager(result)


def get_files():
    folder_path = input("Введите путь к директории: ")

    if os.path.exists(folder_path):
        print(f"Директория: {folder_path}")
        result = sorted(os.listdir(folder_path))
        for i, item in enumerate(result):
            print(i + 1, item)

        print(f"Всего файлов в директории: {len(result)}")
    else:
        print("Попробуйте еще раз. Указанный путь не найден.")
        get_files()


def create_csv():
    rows = [
        {"№": 1, "Ник автора": "mzllf", "Текст поста": "Коли нет дыма без огня, может быть, виноват я сам?",
         "Кол-во лайков": 24567},
        {"№": 2, "Ник автора": "Слава КПСС", "Текст поста": "Это лето в Кайфограде никогда нам не забыть "
                                                            "Лето в Кайфограде, это маленькая жизнь Лето в "
                                                            "Кайфограде, это лето в Кайфограде "
                                                            "И мы курим сигарету на двоих одну и знаем",
         "Кол-во лайков": 390000},
        {"№": 3, "Ник автора": "Лариска Долина", "Текст поста": "I'm the best", "Кол-во лайков": 0},
        {"№": 4, "Ник автора": "Жириновский В.В.",
         "Текст поста": "Жизнь человеку дана один раз, и прожить её нужно в городе Сочи", "Кол-во лайков": 120000},
        {"№": 5, "Ник автора": "pupunya", "Текст поста": "love STANDOF2", "Кол-во лайков": 15},
        {"№": 6, "Ник автора": "Пушкин А.С.", "Текст поста": "Подруга дней моих суровых, Голубка дряхлая моя! "
                                                             "Одна в глуши лесов сосновых Давно, давно ты ждешь меня. "
                                                             "Ты под окном своей светлицы",
         "Кол-во лайков": 1000000},
        {"№": 7, "Ник автора": "Кто-то великий", "Текст поста": "В Риме был, а папы не видал.",
         "Кол-во лайков": 100234},
        {"№": 8, "Ник автора": "Стэтхем", "Текст поста": "Если жизнь - это вызов, то я перезвоню",
         "Кол-во лайков": 2141},
        {"№": 9, "Ник автора": "Путин В.В.", "Текст поста": "Ясно.", "Кол-во лайков": 2322},
        {"№": 10, "Ник автора": "Медведев", "Текст поста": "С Рождеством Христовым!", "Кол-во лайков": 2100232},
    ]

    with open("data.csv", "w", encoding="utf-8", newline='') as f:
        fieldnames = ["№", "Ник автора", "Текст поста", "Кол-во лайков"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_posts():
    pm = PostManager()
    with open("data.csv", "r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            post = Post.from_dict(row)
            pm.append(post)
    return pm


def save_posts(pm):
    with open("data.csv", "w", encoding="utf-8", newline='') as f:
        fieldnames = ["№", "Ник автора", "Текст поста", "Кол-во лайков"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for post in pm:
            writer.writerow(post.to_dict())
    print("Данные сохранены в файл.")


def add_post(pm):
    new_id = len(pm) + 1
    nick = input("Введите ник автора: ")
    text = input("Введите текст поста: ")
    likes = input("Введите количество лайков: ")

    new_post = Post(post_id=new_id, author=nick, text=text, likes=likes)
    pm.append(new_post)
    print(f"Добавлен пост: {new_post}")


def main():
    fl_prog = True
    while fl_prog:
        print("Выберите пункт.")
        print("Пункт 1. Количество файлов в директории")
        print("Пункт 2. Информация о постах")
        print("Пункт 3. Информация о постах, отсортировав по нику автора")
        print("Пункт 4. Информация о постах, отсортировав по кол-ву лайков")
        print("Пункт 5. Информация о постах, кол-во лайков которых >10000")
        print("Пункт 6. Добавить новый пост в файл")
        print("Пункт 7. Выйти из программы")
        choice = int(input("Введите число от 1 до 7: "))
        match choice:
            case 1:
                ("Пункт 1. Количество файлов в директории")
                get_files()
            case 2:
                print("Пункт 2. Информация о постах")
                if not os.path.exists("data.csv"):
                    create_csv()
                pm = load_posts()
                for post in pm:
                    print(post)
            case 3:
                print("Пункт 3. Информация о постах, отсортировав по нику автора")
                if not os.path.exists("data.csv"):
                    create_csv()
                pm = load_posts()
                sorted_pm = pm.sort_byname()
                for post in sorted_pm:
                    print(post)
            case 4:
                print("Пункт 4. Информация о постах, отсортировав по кол-ву лайков")
                if not os.path.exists("data.csv"):
                    create_csv()
                pm = load_posts()
                sorted_pm = pm.sort_bylike()
                for post in sorted_pm:
                    print(post)
            case 5:
                print("Пункт 5. Информация о постах, кол-во лайков которых >10000")
                if not os.path.exists("data.csv"):
                    create_csv()
                pm = load_posts()
                filtered_pm = pm.filter_like()
                for post in filtered_pm:
                    print(post)
            case 6:
                print("Пункт 6. Добавить новый пост в файл")
                if not os.path.exists("data.csv"):
                    create_csv()
                pm = load_posts()
                add_post(pm)
                save_posts(pm)
            case 7:
                fl_prog = False


if __name__ == "__main__":
    main()
