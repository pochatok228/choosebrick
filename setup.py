from cx_Freeze import setup, Executable

setup(
    name = "ChooseBrick",
    version = "0.3.0",
    description = "описание - необязательно",
    executables = [Executable("main.py")]
)