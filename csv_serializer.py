import argparse
import json

leagues_simplified = 'data/leagues_simplified.json'
seasons_simplified = 'data/seasons_simplified.json'


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


def main():
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Convert JSON data to a TSV table.')
    parser.add_argument('input_file', help='Input JSON file name')
    parser.add_argument('output_file', help='Output TSV file name')
    parser.add_argument('--fields', nargs='+', help='Fields to read from JSON', required=True)
    parser.add_argument('--column-names', nargs='+', help='Column names in TSV file', required=True)

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the function to create the table
    create_table(args.input_file, args.output_file, args.fields, args.column_names)


if __name__ == '__main__':
    main()
