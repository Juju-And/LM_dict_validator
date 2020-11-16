import errno
import os
import re
import sys
from typing import List

from iteration_utilities import duplicates


def general_verification(input_file):
    lines = retrieve_list_from_input(input_file)

    list_of_ort_disp_to_check = find_duplicates_ort_vs_disp(lines)
    generate_duplicates_report(
        list_of_duplicates=list_of_ort_disp_to_check,
        report_name="duplicates_ort_vs_disp",
    )

    phonetic_duplicates = find_phonetic_duplicates(lines)
    generate_duplicates_report(
        list_of_duplicates=phonetic_duplicates, report_name="duplicates_phonetics"
    )

    ort_symbols_duplicates = find_duplicate_ort_words_ignoring_symbols(lines)
    generate_duplicates_report(
        list_of_duplicates=ort_symbols_duplicates, report_name="duplicates_ort_symbols"
    )

    full_duplicates = find_full_duplicates(lines)
    generate_duplicates_report(
        list_of_duplicates=full_duplicates, report_name="duplicates_full"
    )


def retrieve_list_from_input(input_file) -> List:
    with open(input_file, encoding="utf8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if " " is line[line.index("[")] or " " is line[line.index("]") + 1]:
            new_line = line.replace(" [", "#[").replace("] ", "]#").split("#")
        else:
            new_line = line.replace("[", "#[").replace("]", "]#").split("#")
        new_lines.append(new_line)

    return new_lines


def find_full_duplicates(lines) -> List:
    return list(duplicates(lines))


def find_duplicates_ort_vs_disp(lines) -> List:
    unique_ort_word = {}
    unique_and_duplicates = []

    # check for unique keys (ort_words) and duplicates for disp_words
    for i in range(len(lines)):
        if (
            lines[i][0] not in unique_ort_word.keys()
            or unique_ort_word.get(lines[i][0]) != lines[i][1]
        ):
            unique_ort_word.update({lines[i][0]: lines[i][1]})
            unique_and_duplicates.append(lines[i][0])

    # list only ort_word's which have multiple versions of disp_words
    ort_duplicates = list(duplicates(unique_and_duplicates))

    ort_disp_duplicate_lines = []

    for line in lines:
        if line[0] in ort_duplicates:
            ort_disp_duplicate_lines.append(line)
    return ort_disp_duplicate_lines


def find_phonetic_duplicates(lines) -> List:
    phonetic_duplicate_lines = []
    all_phonetics_list = [line[2] for line in lines]

    phonetic_duplicates = list(duplicates(all_phonetics_list))

    for line in lines:
        if line[2] in phonetic_duplicates:
            phonetic_duplicate_lines.append(line)

    return phonetic_duplicate_lines


def find_duplicate_ort_words_ignoring_symbols(lines) -> List:
    all_ort_with_symbols_list = []
    all_ort_list = [line[0] for line in lines]

    duplicates_with_symbols = []

    pattern = re.compile(r"[-_]")

    for line in lines:
        if pattern.search(line[0]):
            all_ort_with_symbols_list.append(line[0])

    for line in lines:
        if (
            line[0] in all_ort_with_symbols_list
            and line[0].replace("-", "").replace("_", "") in all_ort_list
        ):
            duplicates_with_symbols.append(line)

    return duplicates_with_symbols


def generate_duplicates_report(list_of_duplicates: List, report_name: str) -> None:
    make_sure_path_exists("reports")

    file2 = open(f"reports/{report_name}.dict", "a")
    file2.truncate(0)
    file2.write("".join(" ".join(el) for el in list_of_duplicates))
    file2.close()


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
    general_verification(sys.argv[1])
