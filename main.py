import sys
from typing import List


def verification(input_file):
    unique_ort_word = {}
    unique_and_duplicates = []

    lines = retrieve_list_from_input(input_file)

    # 2. check for unique keys (ort_words) and duplicates for disp_words
    for i in range(len(lines)):
        if (
            lines[i][0] not in unique_ort_word.keys()
            or unique_ort_word.get(lines[i][0]) != lines[i][1]
        ):
            unique_ort_word.update({lines[i][0]: lines[i][1]})
            unique_and_duplicates.append(lines[i][0])

    # 3. list only ort_word's which have multiple versions of disp_words
    dupes_ort_list = [
        x for n, x in enumerate(unique_and_duplicates) if x in unique_and_duplicates[:n]
    ]

    list_of_ort_disp_to_check = []

    for line in lines:
        if line[0] in dupes_ort_list:
            list_of_ort_disp_to_check.append(line)

    generate_duplicates_ort_vs_disp_report(list_of_duplicates=list_of_ort_disp_to_check)

    generate_general_report(
        total_len=len(lines),
        unique_ort_count=len(unique_ort_word),
        duplicates_count=len(list_of_ort_disp_to_check),
    )


def retrieve_list_from_input(input_file) -> List:
    with open(input_file, encoding="utf8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_line = line.replace(" [", "#[").replace("] ", "]#").split("#")
        new_lines.append(new_line)
    return new_lines


def find_duplicates_ort_vs_disp():
    pass


def list_unique_ort_words():
    pass


def generate_general_report(
    total_len: int, unique_ort_count: int, duplicates_count: int
) -> None:
    file1 = open("reports/general_report.txt", "a")
    file1.truncate(0)
    file1.write(
        f"Total input lines: {total_len}\n"
        f"Unique ort word count: {unique_ort_count}\n"
        f"Duplicates of requiring manual validation: {duplicates_count}"
    )
    file1.close()


def generate_duplicates_ort_vs_disp_report(list_of_duplicates: List) -> None:
    file2 = open("reports/duplicates_ort_vs_disp.dict", "a")
    file2.truncate(0)
    file2.write("".join(" ".join(el) for el in list_of_duplicates))
    file2.close()


if __name__ == "__main__":
    verification(sys.argv[1])
