class TxtFileWorker:
    @staticmethod
    def upload_to_file(data: list, file_path: str = "./users_database") -> None:
        from os.path import exists as file_exists

        args = "a" if file_exists(file_path) else "w"

        with open(file_path, args) as file:
            for item in data:
                file.write(str(item) + '\n')

    @staticmethod
    def load_file(file_path: str = "./users_database") -> list:
        from os.path import exists as file_exists

        if not file_exists(file_path):
            raise FileNotFoundError

        with open(file_path, "r") as file:
            return file.readlines()

