# Canvas Quiz Generator

A Python tool that converts a CSV file into a Canvas-compatible QTI quiz package (.zip) for easy import into **Canvas Classic Quizzes**.

---

## 🚀 Features
- **Auto-detects** CSV files in the current folder.
- Prompts the user if **multiple CSV files** are found.
- Generates a QTI-compliant `.zip` ready for Canvas import.
- ZIP file is automatically named using the CSV filename + `_quiz_` + timestamp.
- Supports multiple-choice questions with up to 3 distractors.
- Customizable quiz title and number of attempts.

---

## 📂 How to Use

### 1️⃣ Prerequisites
- Python 3.x installed on your system.

---

### 2️⃣ Prepare Your CSV File
Format your CSV like this:

| Question                  | Correct Answer                                          | Distractor 1     | Distractor 2      | Distractor 3       |
|---------------------------|----------------------------------------------------------|------------------|-------------------|--------------------|
| What is AI?               | Systems that perform tasks requiring human intelligence  | Data storage     | Web development   | Computer hardware  |

- Only `Question` and `Correct Answer` columns are required.
- Place the CSV file in the same folder as the script.

---

### 3️⃣ Run the Script

If there's one CSV file:
```bash
python generate_canvas_quiz.py --title "Your Quiz Title" --attempts 1

If multiple CSV files exist, the script will prompt you to select one.

You can still manually specify a CSV:

python generate_canvas_quiz.py --input yourfile.csv --title "Your Quiz Title" --attempts 1

The generated .zip will appear in the output folder as:
<csv_filename>_quiz_<timestamp>.zip

4️⃣ Import into Canvas
Go to Settings > Import Course Content in your Canvas course.

Select QTI .zip file and upload the generated package.

Use Classic Quizzes for best compatibility.

🤖 Generate Quiz Questions with AI
Use ChatGPT to quickly create quizzes in the correct CSV format.

Suggested Prompt:
Create [NUMBER] multiple-choice questions about [TOPIC].
Format as CSV with columns: Question, Correct Answer, Distractor 1, Distractor 2, Distractor 3.
Only output the CSV table.

After generating:

Copy the table into a .csv file.

Save it in the same folder as this script.

Run the script!

🛠️ Roadmap
 True/False and Short Answer support.

 Batch CSV processing.

 GUI version for easier use.

 Canvas New Quizzes compatibility.
After Generating:
Copy the CSV output into a text editor or spreadsheet software.

Save it as a .csv file (UTF-8 encoding recommended).

Use it as input for this script!
