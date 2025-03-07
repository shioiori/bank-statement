import re
import os
import glob
import sqlite3
import PyPDF2
import concurrent.futures

def process_pdf_file(pdf_file_path):
    """
    Process a single PDF file:
    - Skip page 1 (header)
    - Extract text from remaining pages
    - Group lines into records (each record starts with a date line in dd/mm/yyyy format)
    - For each record, the first line (header) is split into:
          token1 => ctNo,
          token2 => credit,
          remaining tokens + any extra lines become the description.
    - Return a list of record dictionaries with keys: txtDate, ctNo, credit, description.
    """
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ""
            # Skip the first page (index 0)
            for page in pdf_reader.pages[1:]:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
    except Exception as e:
        print(f"Error processing file {pdf_file_path}: {e}")
        return []

    # Remove empty lines
    lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]

    # Group lines by record. Each record begins with a line that matches a date (dd/mm/yyyy).
    date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}$")
    records = []
    current_date = None
    current_group = []

    for line in lines:
        if date_pattern.match(line):
            # Process the previous group if available
            if current_date is not None and current_group:
                record = process_group(current_date, current_group)
                if record:
                    records.append(record)
            current_date = line
            current_group = []
        else:
            current_group.append(line)
    # Process final group if exists
    if current_date is not None and current_group:
        record = process_group(current_date, current_group)
        if record:
            records.append(record)
    return records

def process_group(date_line, group_lines):
    """
    Process a group of lines (a record) that follow a date line.
    The first line of the group is the header containing:
         ctNo (first token), credit (second token),
         the rest tokens (if any) are the beginning of the description.
    Additional lines in the group are appended to the description.
    """
    if not group_lines:
        return None
    tokens = group_lines[0].split()
    ctNo = tokens[0] if len(tokens) > 0 else ""
    credit = tokens[1] if len(tokens) > 1 else ""
    header_description = " ".join(tokens[2:]) if len(tokens) > 2 else ""
    description_lines = [header_description] if header_description else []
    # Append any extra lines from the group into the description.
    for extra_line in group_lines[1:]:
        extra_tokens = extra_line.split()
        # Sometimes an extra line may start with "Nam" due to line break issues.
        if extra_tokens and extra_tokens[0] == "Nam":
            extra_line_processed = " ".join(extra_tokens[1:])
        else:
            extra_line_processed = extra_line
        description_lines.append(extra_line_processed)
    description = " ".join(description_lines).strip()
    return {
        "txtDate": date_line,
        "ctNo": ctNo,
        "credit": credit,
        "description": description
    }

def main():
    # Get list of PDF files from the folder
    pdf_folder = "./files/pdfs"
    pdf_files = glob.glob(os.path.join(pdf_folder, "*.pdf"))
    print(f"Found {len(pdf_files)} PDF files to process.")

    all_records = []
    # Process PDF files in parallel using ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_pdf_file, pdf_file): pdf_file for pdf_file in pdf_files}
        for future in concurrent.futures.as_completed(future_to_file):
            pdf_file = future_to_file[future]
            try:
                records = future.result()
                print(f"Processed {pdf_file}: extracted {len(records)} records.")
                all_records.extend(records)
            except Exception as exc:
                print(f"{pdf_file} generated an exception: {exc}")

    # Create the SQLite database (with .sqlite3 extension) and store the records in table bankStatement.
    db_path = "./files/csvs/output.sqlite3"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bankStatement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            txtDate TEXT,
            ctNo TEXT,
            credit TEXT,
            description TEXT
        )
    ''')
    # Insert each record into the table.
    for record in all_records:
        cursor.execute('''
            INSERT INTO bankStatement (txtDate, ctNo, credit, description)
            VALUES (?, ?, ?, ?)
        ''', (record["txtDate"], record["ctNo"], record["credit"], record["description"]))
    conn.commit()
    conn.close()

    print(f"All data from {len(pdf_files)} files have been stored in database: {db_path}")

if __name__ == "__main__":
    main()
