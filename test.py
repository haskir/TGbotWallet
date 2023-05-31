def __cut_big_result(strings: str, max_len: int = 4000) -> str:
    if len(strings) > max_len:
        intro = "Слишком большой результат\nпоказано только последние 30 записей\n"
        return intro + strings[-max_len:]


with open("big_result.txt", "r") as file:
    stri = file.read()

print(stri + "\n\n\n")
print(__cut_big_result(stri))