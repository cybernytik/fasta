import sys
from fasta import FastaReader, Seq

filename = "test_data/sequence.fasta"
if not FastaReader.is_fasta(filename):
    print(f"Файл {filename} не является FASTA")
    sys.exit()
for i, seq in enumerate(FastaReader.read(filename), 1):
    print(f"--- Запись {i} ---")
    print(f"Заголовок: {seq.header}")
    print(f"Длина: {len(seq)}")
    print(f"Алфавит: {seq.alphabet()}")
    print(f"Первые 50 символов: {seq.sequence[:50]}")
    print()