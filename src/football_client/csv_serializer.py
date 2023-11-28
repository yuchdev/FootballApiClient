import csv
import json
import os


class CsvSerializer:
    def __init__(self, data_dir, file_name, settings):
        self.data_dir = data_dir
        self.delimiter = settings.get("delimiter", "\t")
        self.headers = settings.get("headers", [])
        self.columns = settings.get("columns", [])
        self.serialized_file = os.path.join(self.data_dir, f"{file_name}.tsv")

    def write(self, data):
        with open(self.serialized_file, "w", newline="", encoding="utf-8") as tsv_file:
            writer = csv.writer(tsv_file, delimiter="\t")
            # Write header
            writer.writerow(["ID", "Name", "Type," "Country", "Seasons"])
            # Write data
            for item in data:
                writer.writerow([item["id"], item["name"], item["country"], ", ".join(map(str, item["seasons"]))])
        print("Serialized data to TSV.")

    def read(self):
        with open(self.serialized_file, "r", newline="", encoding="utf-8") as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter="\t")
            return [row for row in reader]


def create_table(input_file, output_file, fields, column_names):
    # Load the JSON data from the file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Create a list to store the rows of the final table
    table_data = []

    # Iterate through each item in the JSON data
    for item in data:
        # Extract information based on provided fields
        row = [str(item[field]) for field in fields]

        # Append the row to the table data
        table_data.append(row)
        print(f"Added row: {row}")

    # Write the table data to a tab-separated file
    with open(output_file, 'w') as output_file:
        # Write the header
        output_file.write('\t'.join(column_names) + '\n')

        # Write each row
        for row in table_data:
            output_file.write('\t'.join(row) + '\n')

    print("Table has been created successfully.")
