import os
import PyPDF2

ROOT_DIRECTORY_PATH = os.getcwd()


async def pdf_extraction_alg(uploaded_file):

    unique_file_name = os.path.join(
        ROOT_DIRECTORY_PATH,
        uploaded_file.filename
    )

    contents = await uploaded_file.read()

    with open(unique_file_name, 'wb') as destination_file:
        destination_file.write(contents)

    pdf_text = []

    with open(unique_file_name, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf, strict=False)

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

    os.remove(unique_file_name)

    output_string = ''

    for item in pdf_text:
        output_string += item
    return output_string
