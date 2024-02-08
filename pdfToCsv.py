import PyPDF2
import csv


def extract_data_from_pdf():
    column1_data = []
    column2_data = []

    pdf_file = 'dataset.pdf'

    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):  # Use len(pdf_reader.pages) to get the total number of pages
            page = pdf_reader.pages[page_num]  # Access the page using pdf_reader.pages[index]
            page_text = page.extract_text().split('\n')  # Split text into lines

            # Assuming each line contains "Word" and "Meaning" separated by a delimiter (e.g., ":")
            for line in page_text:
                parts = line.split(':')
                if len(parts) == 2:
                    word = parts[0].strip()
                    meaning = parts[1].strip()
                    column1_data.append(word)
                    column2_data.append(meaning)

    csv_file = 'german.csv'

    data_rows = zip(column1_data, column2_data)
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row (optional)
        writer.writerow(["Word", "Meaning"])  # Header row with column names

        # Write the data rows
        writer.writerows(data_rows)

        print(f"Data saved to {csv_file}")
    return column1_data, column2_data


extract_data_from_pdf()
