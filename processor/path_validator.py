from pathlib import Path

class PathValidator:
    @staticmethod
    def validate_filepath(filepath: Path) -> bool:
        try:
            Path(filepath)
            return True
        except ValueError:
            return False

    @staticmethod
    def does_file_exist(filepath: Path) -> bool:
        return filepath.exists() and filepath.is_file()