import argparse
import datetime
import pathlib
import zipfile
import logging
import yaml


# КОНФИГУРАЦИЮ СКРИПТА РОТАЦИИ ФАЙЛОВ
# Скрипт предназначен для автоматической архивации файлов по заданным условиям
# 
# ОПИСАНИЕ ПАРАМЕТРОВ
# log - путь к лог-файлу скрипта ротации
# adamas_1 - название группы конфигурации 
# root_path - путь к директории с файлами
# archive_dir - путь к директории в которой будет создан архив
# 
# АРХИВАЦИЯ ПО ДАТЕ СОЗДАНИЯ
# files_left - количество наиболее ранних файлов, остающихся после архивации
# max_files_count - количество файлов, при достижении которого запускается архивация
# 
# АРХИВАЦИЯ ПО РАЗМЕРУ
# max_size - максимальный размер файла, не подлежащего архивации



def init_logger(log_path: pathlib.Path) -> logging.Logger:
    """
    Инициализация логгера
    :param log_path: обьект типа Path с указанием полного пути к файлу лога:
    :return: обьект логгера для создания записей
    """
    logging.basicConfig(filename=log_path, filemode="w",
                        format="[%(asctime)s: %(levelname)s] %(message)s", level=logging.DEBUG)
    logger_instance = logging.getLogger(__name__)
    return logger_instance


def file_time_stamp_key(file_path: pathlib.Path) -> tuple:
    """
    Функция для извлечения даты создания файла. Формирует кортеж для функции сортировки
    :param file_path: обьект типа Path с указанием пути к файлу
    :return: возвращает кортеж с датой создания файла в формате (year, month, day)
    """
    time_stamp = file_path.stat().st_mtime
    creation_date = datetime.datetime.fromtimestamp(time_stamp).strftime("%Y/%m/%d")
    return tuple(creation_date.split("/"))


def zip_files(root_dir: pathlib.Path, arch_dir: pathlib.Path, arch_name: pathlib.Path, 
                 files:list, files_left=10, by_size=False):
    """
    Функция для архивации списка файлов. Создает директорию и добавляет файлы из списка в архив zip, 
    затем удаляет их из исходной директории.
    Оставляет последние n файлов в соответсвии с параметром left_files.
    :param root_dir: Обьект типа Path с указанием пути к директории файлов с логами для архивации
    :param arch_dir: Обьект типа Path с указанием пути к директории с zip архивами логов
    :param arch_name: Обьект типа Path с указанием имени архива
    :param files: Список обьектов типа Path с указанием путей к файлам подлежащим архивации
    :param files_left: Количество файлов в списке не подлежащих архивации
    :param by_size: Архивация файлов по размеру, а не по дате создания
    """
    if not by_size:
        files = sorted(files, key=file_time_stamp_key)
    archive_dir_path = arch_dir
    archive_dir_path.mkdir(exist_ok=True)
    archive_full_path = archive_dir_path / arch_name
    with zipfile.ZipFile(archive_full_path, "w", zipfile.ZIP_DEFLATED) as zip_archive:
        for file_path in files[:len(files) - files_left]:
            zip_archive.write(file_path)
            file_path.unlink()


def get_files_list(root_dir: pathlib.Path) -> list:
    """
    Функция извлекает именна всех файлов в указанной директории
    :param root_dir: обьект типа Path с указанием пути к каталогу
    :return: список обьектов типа Path в указанной директории
    """
    return [file for file in root_dir.iterdir() if file.is_file()]


def open_config_file(path: pathlib.Path) -> dict:
    """
    Чтение конфигурации из файла с .yaml
    :param path: обьект типа Path с указанием полного пути к файлу конфигурации
    :return: возвращает словарь с конфигурацией архивирования
    """
    with open(path) as config_file:
        configuration = yaml.safe_load(config_file)
    return configuration


def size_to_bytes(size: str) -> int:
    """
    Функция преобразования размеров файла из параметра конфигурации в размер в байтах
    :param size: строка с указанием размера из файла конфигурации
    :return: размер файла в байтах
    """
    conversion_value = {"Mb": 1048576, "Kb": 1024, "Gb": 1073741824}
    return int(size[:-2]) * conversion_value.get(size[-2:], 1)


def check_config_file(path: pathlib.Path):
    """
    Проверка файла конфигурации на правильность заполнения
    :param path: обьект типа Path с указанием полного пути к файлу конфигурации
    """
    try:
        _config = open_config_file(path)
        print(f"Синтаксис файла {path} корректен. Нажмите Enter для выхода")
        input()
    except Exception as error:
        print(f"Ошибка файла конфигурации {error} Нажмите Enter для выхода")
        input()


def archiving_files(config_file_path:pathlib.Path):
    """
    Основная функция ротации логов. Проверяет файлы в соответсвии с конфигурацией
    и при соответсвии критериям упаковывает их в архив. При наличии ошибок
    производится запись в лог файл приложения
    :param path: обьект типа Path с указанием полного пути к файлу конфигурации
    """
    config = open_config_file(config_file_path)
    logger = init_logger(config.pop("log", "logs_rotation.log"))

    for entry in config.keys():
        try:
            archive_parameters = config.get(entry)
            if archive_parameters is not None:

                root_path = pathlib.Path(archive_parameters.get("root_path"))
                archive_dir = pathlib.Path(archive_parameters.get("archive_dir"))
                current_date = datetime.datetime.now().strftime("%Y_%m_%d")
                archive_name = pathlib.Path(f"{entry}_{current_date}.zip")
                files_left = archive_parameters.get("files_left")
                max_files_count = archive_parameters.get("max_files_count")
                max_size = archive_parameters.get("max_size")
                files_paths = get_files_list(root_path)

                if max_files_count is not None:
                    if len(files_paths) > max_files_count:
                        zip_files(root_path, archive_dir, archive_name, files_paths, files_left, by_size=False)
                    else:
                        continue
                elif max_size is not None:
                    max_size_files = [file for file in files_paths if file.stat().st_size >= size_to_bytes(max_size)]
                    if len(max_size_files) > 0:
                        zip_files(root_path, archive_dir, archive_name, max_size_files, 0, by_size=True)
                else:
                    logger.error(f"Ошибка конфигурации {entry}")
                    continue   
            else:
                continue
        except Exception as error:
            logger.error(f"Ошибка {error} при обработке параметров {entry}")
            continue   


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--config_path", help="Путь к файлу конфигурации yaml", default="/")
    parser.add_argument("-c", "--check_config", help="Проверка синтаксиса файла конфигурации yaml", action="store_true", default=False)
    args = parser.parse_args()
    config_file_path = pathlib.Path(args.config_path)

    if not config_file_path.exists() or not config_file_path.is_file() :
        raise FileNotFoundError(f"Файл {args.config_path} не является файлом конфигурации")

    if args.check_config:
        check_config_file(config_file_path)
    else:
        archiving_files(config_file_path)




    
