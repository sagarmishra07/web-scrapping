import fitz


def extract_data_from_pdf():
    doc = fitz.open('quiz.pdf')
    text = ""
    counter = 0
    data_array = []
    question = []

    for page in doc:
        text += page.get_text()

    for line in text.splitlines():
        counter += 1
        question.append(line)
        if counter == 7:
            counter = 0
            data_array.append(question)
            question = []

    print(data_array)


extract_data_from_pdf()
