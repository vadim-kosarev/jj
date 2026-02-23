# скрипт должен искать большие каталоги на диске C:\
# нужно учитывать тот факт, что некоторые каталоги могут быть недоступны из-за прав доступа, и обрабатывать эти случаи без прерывания выполнения
# результаты должны быть сохранены в файл в формате CSV с указанием пути к каталогу и его размера в мегабайтах.
# в отчет выводить только большие каталоги - размером более 5 гигабайт
# начальный каталог - по умолчанию C:\, но может быть указан в виде аргумента командной строки
# скрипт должен быть полностью автономным - без привлечения пользователя после запуска, и должен обрабатывать все ошибки, связанные с доступом к файлам и каталогам, без прерывания выполнения
# ошибки логировать в отдельный файл с указанием пути к каталогу и описания ошибки через logger.error, logger.warn
# сканирование должно быть рекурсивным - считать размер всех подкаталогов и выводить те, которые больше threshold
# не использовать print - использовать logger.info

import os
import sys
import csv
import logging
from datetime import datetime
from tqdm import tqdm
from collections import deque

# Configure logging
log_filename = f"large_dir_tree_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

SIZE_THRESHOLD_BYTES = 5 * 1024 * 1024 * 1024  # 5 GB


def get_dir_size(path: str) -> int:
    """Recursively calculate directory size, skipping inaccessible paths."""
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file(follow_symlinks=False):
                        try:
                            total += entry.stat(follow_symlinks=False).st_size
                        except OSError as e:
                            logger.error(f"Cannot stat file {entry.path}: {e}")
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_dir_size(entry.path)
                except OSError as e:
                    logger.error(f"Cannot access entry {entry.path}: {e}")
    except PermissionError as e:
        logger.error(f"Permission denied: {path}: {e}")
    except OSError as e:
        logger.error(f"OS error accessing {path}: {e}")
    return total


def scan_dirs_recursive(root: str, results: list):
    """Scan all directories using BFS and collect those above threshold with progress bar."""
    queue = deque([root])
    pbar = tqdm(desc="Scanning directories", unit=" dir", dynamic_ncols=True)

    while queue:
        current_path = queue.popleft()
        pbar.set_description(f"Scanning: {current_path[:70]}")
        pbar.update(1)

        try:
            entries = list(os.scandir(current_path))
        except PermissionError as e:
            logger.error(f"Permission denied scanning: {current_path}: {e}")
            continue
        except OSError as e:
            logger.error(f"OS error scanning: {current_path}: {e}")
            continue

        for entry in entries:
            try:
                if entry.is_symlink():
                    continue
                if entry.is_dir(follow_symlinks=False):
                    size = get_dir_size(entry.path)
                    if size >= SIZE_THRESHOLD_BYTES:
                        results.append((entry.path, size))
                        size_gb = size / (1024 ** 3)
                        logger.info(f">> LARGE: {entry.path}  ({size_gb:.2f} GB)")
                    # Add to queue for recursive scanning
                    queue.append(entry.path)
            except OSError as e:
                logger.error(f"Cannot process entry {entry.path}: {e}")

    pbar.close()


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else r"C:\\"

    if not os.path.isdir(root):
        logger.error(f"Error: '{root}' is not a valid directory.")
        sys.exit(1)

    logger.info(f"Starting scan of: {root}")
    logger.info(f"Threshold: {SIZE_THRESHOLD_BYTES / (1024**3):.0f} GB")
    logger.info(f"Error log: {log_filename}")
    logger.info("-" * 60)

    results = []
    scan_dirs_recursive(root, results)
    logger.info("")  # newline after progress bar

    # Sort by size descending
    results.sort(key=lambda x: x[1], reverse=True)

    output_csv = f"large_dirs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['path', 'size_mb'])
        for path, size in results:
            writer.writerow([path, f"{size / (1024**2):.2f}"])

    logger.info("-" * 60)
    logger.info(f"Found {len(results)} large directories (>= 5 GB):")
    for path, size in results:
        logger.info(f"  {path:60s}  {size / (1024**3):.2f} GB")
    logger.info(f"Results saved to: {output_csv}")
    logger.info(f"Errors logged to: {log_filename}")


if __name__ == "__main__":
    main()

