# Multimodal AI-Based Image Understanding System

An interactive, beginner-friendly multimodal artificial intelligence web application developed in Python and Streamlit. The system accepts an image (sample or custom uploaded), processes it through a vision-language perception pipeline, and generates structured scene intelligence alongside a rigorous, grounded evaluation report.

---

## 🎯 1. Project Objectives & Core Features

1. **Image Selection & Upload:**
   - Three curated, realistic sample images across diverse domains:
     - **Education:** Study group of students in a university library with laptops, textbooks, and notes.
     - **Technology:** Contemporary developer workstation with dual displays, mechanical keyboard, and headphones.
     - **Everyday Objects:** Warm rustic table with a steaming ceramic mug, reading glasses, and vintage book.
   - User upload control for custom images (`JPG`, `PNG`, `JPEG`, `WEBP`).
   - Dynamic image preview displaying dimensions, color mode, and format.

2. **Multimodal Visual Intelligence:**
   - **Image Description:** A concise explanation of the main content and setting.
   - **Concise Caption:** A single meaningful, contextual caption summarizing the scene.
   - **Brief Summary:** A 2–3 sentence overview of context and visual composition.
   - **Structured Element Extraction:** Segmented lists of:
     - Concrete physical objects
     - Visible activities and human actions
     - Visual elements (lighting, color palette, architectural composition)

3. **Grounded Evaluation Report:**
   - Compares the AI model's output with actual visible visual evidence.
   - Documents at least two observed errors / unsupported speculative observations across sample images.
   - Explicitly records notable visual omissions (e.g. background figures, cable types, beverage steam).
   - Distinguishes observed inaccuracies from fundamental verification limitations (e.g. inability to test chemical liquid composition or unreadable book text).

---

## 🏗️ 2. Technology Stack & Architecture

- **Language:** Python 3.9+
- **Frontend / UI:** [Streamlit](https://streamlit.io/) (Clean, modern card-based interface)
- **Image Processing:** [Pillow (PIL)](https://pillow.readthedocs.io/)
- **Vision-Language Model:** Google Gemini Vision (`google-generativeai` / `gemini-1.5-flash`)
- **Fault-Tolerant Engine:** Dual-mode architecture featuring live Gemini API perception when an API key is provided, paired with a reliable, grounded fallback engine ensuring zero-crash offline demonstration during vivas and practical exams.

---

## 📂 3. Directory Structure

```text
Gen AI internal/project 2/
├── .env.example            # Template for optional Gemini API key
├── app.py                  # Streamlit web application & user interface
├── analyzer.py             # Multimodal vision analysis & API integration
├── evaluator.py            # Grounded evaluation report engine & cross-sample matrix
├── requirements.txt        # Minimal dependency list
├── samples/                # Curated high-resolution sample images
│   ├── education.jpg       # Sample 1: Education / University Library
│   ├── technology.jpg      # Sample 2: Technology / Developer Workstation
│   └── everyday_objects.jpg# Sample 3: Everyday Objects / Reading Table
└── README.md               # Complete project documentation
```

---

## 🚀 4. Installation & Execution Guide

### Step 1: Navigate to Project Directory
```bash
cd "Gen AI internal/project 2"
```

### Step 2: Activate Virtual Environment
Use the existing virtual environment:
```bash
source .venv/bin/activate
```
*(Or create a new one using `python3 -m venv .venv && source .venv/bin/activate`)*

### Step 3: Install Required Packages
```bash
pip install -r requirements.txt
```

### Step 4: (Optional) Configure Gemini API Key
You can run the application **with or without** an API key:
- **Option A (Sidebar):** Simply type or paste your key into the sidebar password field in the web browser.
- **Option B (Environment Variable):**
  ```bash
  export GEMINI_API_KEY="your_actual_gemini_api_key"
  ```
- **Option C (Offline / Demo Mode):** If no key is set, the system seamlessly runs its built-in grounded multimodal engine, producing full descriptions, element tags, and evaluation reports for all sample images.

### Step 5: Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your web browser at the URL shown in the terminal (usually `http://localhost:8501`).

---

## 📋 5. Cross-Sample Evaluation Matrix

| Category | Observed Errors / Unsupported Claims | Notable Visual Omissions | Verification Limitations |
| :--- | :--- | :--- | :--- |
| **Education** | • Inferred specific exam subject (e.g. "biology") despite illegible text.<br>• Headcount confusion (reported 4–5 instead of 6). | • Distant background library patrons.<br>• Reusable tumbler and chair backpack. | • Actual academic major & textbook titles unverified from distance. |
| **Technology** | • Identified code as Python instead of React/JSX syntax visible on monitor.<br>• Misclassified headphone stand as desk microphone. | • Coiled aviator keyboard cable.<br>• "DEV" printed on mug & phone clock lockscreen. | • Internal computer hardware & mechanical switch types unverified. |
| **Everyday Objects** | • Asserted beverage is "espresso/hot cocoa" based only on dark liquid color.<br>• Assumed "reader just left for a break" (speculative narrative). | • Faint rising steam over mug.<br>• Chapter title "Chapter Eight: The Quiet Hours". | • Liquid chemical composition and unshown book title/author unverified. |

---

## 🎓 6. College Viva / Practical Exam Q&A Guide

**Q1: What is a Multimodal AI System?**  
*Answer:* A multimodal AI system processes and connects information across multiple data modalities—in this case, visual imagery (pixels) and natural language (tokens)—to perform tasks like visual question answering, dense captioning, and structured object extraction.

**Q2: Why do Vision-Language Models make hallucinations or unsupported claims?**  
*Answer:* VLMs are trained to maximize text likelihood. When presented with common scenes (e.g. students studying), their language prior often predicts likely phrases like "preparing for a biology exam" even when the visual evidence (pixel resolution) does not actually support that claim.

**Q3: Why is an Evaluation Report essential in Multimodal systems?**  
*Answer:* Automated vision outputs can mislead users if accepted uncritically. The evaluation report audits the generated description against verifiable facts, explicitly identifying discrepancies, missed details, and unverified assumptions.

**Q4: How does this project handle API unavailability or network failure?**  
*Answer:* The project implements a defensive dual-mode architecture. If an API key is missing or quotas are exceeded, the app safely falls back to a grounded benchmark engine, preventing runtime crashes and ensuring full demonstration readiness.
