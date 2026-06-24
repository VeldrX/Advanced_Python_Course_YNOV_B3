import logging
import os
import sys
import platform
from logging.handlers import RotatingFileHandler


class SafeRotatingFileHandler(RotatingFileHandler):
    """RotatingFileHandler qui capture les erreurs de rotation sur Windows."""

    def doRollover(self):
        try:
            if self.stream:
                self.stream.close()
                self.stream = None
            super().doRollover()
        except Exception as e:
            sys.stderr.write(f"Log rotation failed: {e}. Continuing with current file.\n")
            if not self.stream:
                self.stream = self._open()


def get_logger(name=__name__, log_file=None, level=logging.INFO,
               max_bytes=10485760, backup_count=5):
    """Configure et retourne un logger réutilisable avec rotation."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if platform.system() == 'Windows':
            from logging import FileHandler
            file_handler = FileHandler(log_file, encoding='utf-8')
        else:
            file_handler = SafeRotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger