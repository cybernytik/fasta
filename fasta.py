class Seq:
    """Класс для представления одной биологической последовательности"""

    def __init__(self, header:str, sequence: str):
        """
        Инициализация последовательности

        :param header: заголовок FASTA-записи (без символа '>')
        :param sequence: последовательность (строка букв)
        """
        self.header = header
        self.sequence = sequence.upper()

    def __str__(self) -> str:
        """Красивое строковое представление: заголовок и последовательность"""
        lines = [self.sequence[i:i+80] for i in range(0,len(self.sequence),80)]
        return f">{self.header}\n" + "\n".join(lines)

    def __len__(self) -> int:
        """Длина последовательности"""
        return len(self.sequence)

    def alphabet(self) -> str:
        """
        Определяет алфавит: 'nucleotide' или 'protein'.

        Нуклеотидный алфавит: A, T, G, C, U (и иногда N).
        Если в последовательности есть буквы, не входящие в этот набор,
        считаем её белковой.
        """
        nucl = set("ATGCUN")
        if set(self.sequence).issubset(nucl):
            return "nucleotide"
        return "protein"


class FastaReader:

    """Класс для чтения FASTA-файлов по одной записи (генератор)."""
    def is_fasta(filename:str) -> bool:
        """
        Проверяет, похож ли файл на FASTA.

        :param filename: путь к файлу
        :return: True, если первая непустая строка начинается с '>'
        """
        with open(filename,"r") as f:
            for line in f:
                line = line.strip()
                if line:
                    return line.startswith(">")
        return False

    def read(filename: str):
        """
        Генератор, который выдаёт объекты Seq по одному.

        :param filename: путь к FASTA-файлу
        :yield: объект Seq
        """
        if not FastaReader.is_fasta(filename):
            raise ValueError(f"Файл {filename} не является FASTA")

        header = None
        seq_parts = []

        with open(filename, "r") as f:
            for line in f:
                line = line.rstrip()

                if line.startswith(">"):
                    if header is not None:
                        yield Seq(header, "".join(seq_parts))

                    header = line[1:]
                    seq_parts = []
                else:
                    if header is not None:
                        seq_parts.append(line)

        if header is not None:
            yield Seq(header, "".join(seq_parts))