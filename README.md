# canvas-quiz-generator
A Python tool to generate Canvas-compatible QTI quizzes from CSV files.
# Canvas Quiz Generator

A simple Python tool that converts a CSV file into a Canvas-compatible QTI quiz package (.zip) for easy import into **Canvas Classic Quizzes**.

---

## 🚀 Features
- Generate multiple-choice quizzes from a CSV file.
- Fully QTI 1.2-compliant package (includes `imsmanifest.xml`).
- Supports flexible CSV formatting with up to 3 distractors per question.
- Customizable quiz title and number of attempts.
- Output is ready-to-import into Canvas (Classic Quizzes).

---

## 📂 How to Use

### 1️⃣ Prerequisites
- Python 3.x installed on your system.
- Basic knowledge of running Python scripts via command line.

### 2️⃣ Prepare Your CSV File
Use the following format:

| Question                  | Correct Answer                                          | Distractor 1     | Distractor 2      | Distractor 3       |
|---------------------------|----------------------------------------------------------|------------------|-------------------|--------------------|
| What is AI?               | Systems that perform tasks requiring human intelligence  | Data storage     | Web development   | Computer hardware  |
| What is Machine Learning? | Systems that learn from data without explicit programming| Manual coding    | Database querying | Internet browsing  |

- **Required Columns:** `Question` and `Correct Answer`
- Distractors are optional but recommended.

### 3️⃣ Run the Script
```bash
python generate_canvas_quiz.py --input sample_quiz.csv --title "AI Basics Quiz" --attempts 1
