import csv
import os
import uuid
import zipfile
import xml.etree.ElementTree as ET
import argparse

# --- Argument Parser ---
parser = argparse.ArgumentParser(description="Generate Canvas Quiz from CSV.")
parser.add_argument('--input', help='Path to input CSV file')
parser.add_argument('--title', required=True, help='Quiz title')
parser.add_argument('--attempts', default='1', help='Max attempts (default: 1)')
parser.add_argument('--output', default='output', help='Output folder')
args = parser.parse_args()

# --- Auto-detect CSV if not provided ---
if not args.input:
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the current directory. Please provide a CSV file.")
        exit(1)
    elif len(csv_files) == 1:
        args.input = csv_files[0]
        print(f"Automatically selected CSV file: {args.input}")
    else:
        print("Multiple CSV files found. Please select one:")
        for idx, file in enumerate(csv_files, 1):
            print(f"{idx}: {file}")
        choice = input("Enter the number of the file to use: ")
        try:
            args.input = csv_files[int(choice) - 1]
        except (IndexError, ValueError):
            print("Invalid selection.")
            exit(1)

# --- Required Columns ---
REQUIRED_COLUMNS = ['question', 'correct answer']

# --- Read CSV with Flexible Headers ---
questions = []
try:
    with open(args.input, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = [h.strip().lower() for h in reader.fieldnames]

        for col in REQUIRED_COLUMNS:
            if col not in headers:
                raise ValueError(f"Missing required column: '{col}' in CSV header.")

        for row in reader:
            row_normalized = {k.strip().lower(): v.strip() for k, v in row.items()}
            distractors = [row_normalized.get(f'distractor {i}', '') for i in range(1, 4)]
            distractors = [d for d in distractors if d]

            q = {
                'question': row_normalized['question'],
                'correct': row_normalized['correct answer'],
                'distractors': distractors
            }
            questions.append(q)
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# --- Build Assessment XML ---
ET.register_namespace('', "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
root = ET.Element("questestinterop")
assessment = ET.SubElement(root, "assessment", {"title": args.title, "ident": str(uuid.uuid4())})

qtimetadata = ET.SubElement(assessment, "qtimetadata")
attempts_field = ET.SubElement(qtimetadata, "qtimetadatafield")
ET.SubElement(attempts_field, "fieldlabel").text = "cc_maxattempts"
ET.SubElement(attempts_field, "fieldentry").text = args.attempts

section = ET.SubElement(assessment, "section", {"ident": "root_section"})

item_id = 1000
choice_id = 5000

for q in questions:
    item = ET.SubElement(section, "item", {"title": q['question'][:50], "ident": f"i{item_id}"})
    item_id += 1

    itemmeta = ET.SubElement(item, "itemmetadata")
    qti_meta = ET.SubElement(itemmeta, "qtimetadata")

    qtype_field = ET.SubElement(qti_meta, "qtimetadatafield")
    ET.SubElement(qtype_field, "fieldlabel").text = "question_type"
    ET.SubElement(qtype_field, "fieldentry").text = "multiple_choice_question"

    points_field = ET.SubElement(qti_meta, "qtimetadatafield")
    ET.SubElement(points_field, "fieldlabel").text = "points_possible"
    ET.SubElement(points_field, "fieldentry").text = "1"

    presentation = ET.SubElement(item, "presentation")
    material = ET.SubElement(presentation, "material")
    ET.SubElement(material, "mattext", {"texttype": "text/plain"}).text = q['question']

    response_ident = f"response_{item_id}"
    response_lid = ET.SubElement(presentation, "response_lid", {"ident": response_ident, "rcardinality": "Single"})
    render_choice = ET.SubElement(response_lid, "render_choice", {"shuffle": "yes"})

    choices = [(q['correct'], True)] + [(d, False) for d in q['distractors']]

    correct_choice_ident = ""

    for choice_text, is_correct in choices:
        cid = f"choice_{choice_id}"
        choice_id += 1
        resp_label = ET.SubElement(render_choice, "response_label", {"ident": cid})
        material = ET.SubElement(resp_label, "material")
        ET.SubElement(material, "mattext", {"texttype": "text/plain"}).text = choice_text
        if is_correct:
            correct_choice_ident = cid

    resprocessing = ET.SubElement(item, "resprocessing")
    outcomes = ET.SubElement(resprocessing, "outcomes")
    ET.SubElement(outcomes, "decvar", {"maxvalue": "1", "minvalue": "0", "varname": "SCORE", "vartype": "Decimal"})

    respcondition = ET.SubElement(resprocessing, "respcondition", {"continue": "No"})
    conditionvar = ET.SubElement(respcondition, "conditionvar")
    ET.SubElement(conditionvar, "varequal", {"respident": response_ident}).text = correct_choice_ident
    ET.SubElement(respcondition, "setvar", {"action": "Set", "varname": "SCORE"}).text = "1"

# --- Save Assessment XML ---
os.makedirs(args.output, exist_ok=True)
assessment_xml = os.path.join(args.output, "assessment1.xml")
ET.ElementTree(root).write(assessment_xml, encoding="UTF-8", xml_declaration=True)

# --- Build imsmanifest.xml ---
manifest = ET.Element("manifest", {"identifier": str(uuid.uuid4()), "xmlns": "http://www.imsglobal.org/xsd/imscp_v1p1"})
organizations = ET.SubElement(manifest, "organizations")
resources = ET.SubElement(manifest, "resources")
resource = ET.SubElement(resources, "resource", {
    "identifier": "assess1",
    "type": "imsqti_xmlv1p2",
    "href": "assessment1.xml"
})
ET.SubElement(resource, "file", {"href": "assessment1.xml"})

manifest_xml = os.path.join(args.output, "imsmanifest.xml")
ET.ElementTree(manifest).write(manifest_xml, encoding="UTF-8", xml_declaration=True)

# --- Zip for Canvas ---
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
zip_path = os.path.join(args.output, f"{args.title.replace(' ', '_')}_{timestamp}.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(assessment_xml, arcname="assessment1.xml")
    zipf.write(manifest_xml, arcname="imsmanifest.xml")

print(f"Canvas QTI package generated: {zip_path}")
