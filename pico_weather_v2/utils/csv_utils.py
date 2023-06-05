from pico_weather_v2.utils import files_utils


def get_header(file_path):
    header = None

    if files_utils.check_if_exists(file_path):
        with open(file_path, "r") as file:
            row = file.readline()

            if row:
                header = row.split(",")

    return header


def parse_row(row, header):
    splited_row = row.split(",")
    parsed_row = {}

    for index, header_item in enumerate(header):
        parsed_row[header_item] = splited_row[index]

    return parsed_row


def get_csv_content(file_path):
    content = []

    if files_utils.check_if_exists(file_path):
        header = get_header(file_path)

        if header:
            with open(file_path, "r") as file:
                row_id = 0

                for row in file:
                    if row_id > 0:
                        content.append(parse_row(row, header))

                    row_id += 1

    return content


def init_csv_file(file_path, header):
    with open(file_path, "w") as file:
        file.write(",".join(header) + "\n")


def write_row(file_path, row):
    with open(file_path, "a") as file:
        file.write(row + "\n")


def get_rows_count(file_path):
    rows_count = 0

    if files_utils.check_if_exists(file_path):
        with open(file_path, "r") as file:
            for _ in file:
                rows_count += 1

    if rows_count >= 1:
        rows_count -= 1

    return rows_count
