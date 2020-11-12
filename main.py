import sys


def verification():
    unique_ort_word = {}
    unique_and_duplicates = []

    with open(sys.argv[1], encoding="utf8") as f:
        lines = f.readlines()
        new_lines = []

        # 1. clean lines to split it to 3 elements
        for line in lines:
            new_line = line.replace(" [", "#[").replace("] ", "]#").split("#")
            new_lines.append(new_line)

        # 2. check for unique keys (ort_words) and duplicates for disp_words
        for i in range(len(new_lines)):
            if (
                new_lines[i][0] not in unique_ort_word.keys()
                or unique_ort_word.get(new_lines[i][0]) != new_lines[i][1]
            ):
                unique_ort_word.update({new_lines[i][0]: new_lines[i][1]})
                unique_and_duplicates.append(new_lines[i][0])

        # 3. list only ort_word's which have multiple versions of disp_words
        dupes_ort_list = [
            x
            for n, x in enumerate(unique_and_duplicates)
            if x in unique_and_duplicates[:n]
        ]

        list_of_full_dupes = []
        for line in new_lines:
            if line[0] in dupes_ort_list:
                list_of_full_dupes.append(line)

    file2 = open("reports/duplicates_ort_vs_disp.dict", "a")
    file2.truncate(0)
    file2.write("".join(" ".join(el) for el in list_of_full_dupes))
    file2.close()

    general_report(
        total_len=len(lines),
        unique_ort_count=len(unique_ort_word),
        dupes_count=len(list_of_full_dupes),
    )


def general_report(total_len: int, unique_ort_count: int, dupes_count: int):
    file1 = open("reports/general_report.txt", "a")
    file1.truncate(0)
    file1.write(
        f"Total input lines: {total_len}\n"
        f"Unique ort word count: {unique_ort_count}\n"
        f"Duplicates requiring manual validation: {dupes_count}"
    )
    file1.close()


if __name__ == "__main__":
    verification()
