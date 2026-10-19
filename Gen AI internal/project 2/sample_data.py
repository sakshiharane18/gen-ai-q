"""
Sample Data and Ground Truth Reference for Multimodal Image Understanding System.
Provides 3 curated sample datasets across Education, Technology, and Everyday Objects.
"""

import os
from typing import Dict, Any, List

SAMPLE_IMAGES: Dict[str, Dict[str, Any]] = {
    "education": {
        "id": "education",
        "title": "Education: College Machine Learning Lecture",
        "category": "Education",
        "filename": "education_classroom.jpg",
        "short_label": "1. Education (AI Classroom)",
        "ground_truth_description": (
            "A university professor dressed in a professional navy blazer and dress shirt stands in front of "
            "a large whiteboard, actively explaining artificial intelligence and deep neural network concepts. "
            "The whiteboard is covered with detailed network layer diagrams (input layer, hidden layers, "
            "output layer) and backpropagation mathematical equations. A classroom of attentive college "
            "students is seated at modern wooden desks with open laptops (Dell laptops visible), spiral "
            "notebooks, and pens. In the background, a large window reveals green campus trees and a brick academic "
            "building under bright daylight, with a wall clock and digital timer mounted above."
        ),
        "important_elements": [
            "University professor in navy blazer & dress shirt",
            "Whiteboard with hand-drawn Neural Network architecture",
            "Mathematical formulas: 'MACHINE LEARNING', 'backpropagation', loss gradient partial derivatives",
            "College students attentively taking notes and coding",
            "Dell laptops open on student desks",
            "Spiral notebooks, ballpoint pens, and stationery",
            "Insulated reusable water bottles",
            "Ceiling-mounted multimedia projector",
            "Wall-mounted analog clock & digital display reading '11:14'",
            "Large window overlooking campus lawn and brick university building",
            "Wall monitor on the left showing 'AI DIAGRAMS: NEURAL NETWORKS'"
        ],
        "caption": "A university professor lectures on deep neural network architectures to students in a modern AI classroom.",
        "summary": (
            "In a brightly lit university lecture hall, a professor illustrates neural network layers and backpropagation "
            "formulas on a whiteboard. Diverse students follow the lecture attentively using open laptops and handwritten notes. "
            "The setting illustrates modern higher education integrating rigorous theoretical machine learning with active learning."
        ),
        "evaluation_report": {
            "grounding_status": "Highly Grounded",
            "grounding_score": 94,
            "verified_observations": [
                "Professor is actively drawing and gesturing at a neural network diagram on the whiteboard.",
                "Students are seated at wooden desks with laptops (Dell branding visible) and paper notebooks.",
                "Mathematical notations including partial derivatives for backpropagation are visibly present on the board.",
                "Large glass window displays exterior campus trees and brick architecture."
            ],
            "possible_omissions": [
                "The wall clock and digital display showing the specific time '11:14' are frequently overlooked by generic vision models.",
                "The left-side wall-mounted monitor displaying 'AI DIAGRAMS: NEURAL NETWORKS' is often missed because focus is drawn to the professor.",
                "Specific laptop brands (Dell logo) and the exact code visible on the foreground student's screen are often omitted."
            ],
            "unsupported_observations": [
                "Any assertion of the specific university name (e.g., 'MIT', 'Stanford') is unsupported; the campus architecture is generic.",
                "Claiming specific student names, grades, or exact semester levels constitutes an unverifiable hallucination.",
                "Asserting that the professor is speaking specific spoken words cannot be verified from a still visual image."
            ],
            "limitations_analysis": (
                "Vision-language models tend to prioritize central human figures and large text headers. Fine-grained secondary details, "
                "such as digital clock digits and small wall-mounted signage, represent common omissions. Background exterior features "
                "are grounded, but specific institutional inferences must remain guarded."
            )
        }
    },
    "technology": {
        "id": "technology",
        "title": "Technology: AI Developer Dual-Monitor Workstation",
        "category": "Technology",
        "filename": "technology_workspace.jpg",
        "short_label": "2. Technology (AI Workstation)",
        "ground_truth_description": (
            "A modern software engineer's dual-monitor workstation positioned on a natural wood desk. "
            "The left monitor displays a dark-themed code editor (VS Code style) with Python syntax. "
            "The right monitor displays a real-time machine learning training dashboard featuring loss curves "
            "(Loss: 0.042), accuracy graphs (98.1%), GPU usage telemetry (78%), and a confusion matrix. "
            "On the desk sits a compact mechanical keyboard with RGB backlighting, an ergonomic wireless mouse "
            "on a dark felt mat, over-ear black headphones on a wooden stand, a smartphone displaying '17:42', "
            "a potted succulent plant, and a ceramic coffee mug bearing 'CODE & COFFEE AI' branding. "
            "In the background, a bookshelf contains technical books and a miniature robot figurine against an exposed brick wall."
        ),
        "important_elements": [
            "Dual Dell widescreen monitors on an articulated desk mount",
            "Left display: Code editor with Python machine learning script",
            "Right display: ML model training metrics (Loss: 0.042, Accuracy: 98.1%, GPU Usage: 78%)",
            "Training performance graphs, loss curve, and confusion matrix",
            "Backlit mechanical keyboard with coiled USB cable",
            "Ergonomic wireless mouse (Logitech style) on dark felt desk pad",
            "Over-ear black headphones resting on a wooden headphone stand",
            "Ceramic mug with 'CODE & COFFEE AI' printed text and logo",
            "Smartphone resting on the right side showing time '17:42'",
            "Small green succulent plant in a white ceramic pot",
            "Bookshelf in background with technical books and miniature robot figurine",
            "Exposed red brick wall and office backdrop"
        ],
        "caption": "A high-performance developer workstation configured for machine learning model development and real-time training telemetry.",
        "summary": (
            "An organized engineering workspace features dual monitors displaying Python code and live deep learning training metrics. "
            "High-end peripherals including a mechanical keyboard, wireless mouse, studio headphones, and a branded coffee mug create an efficient environment. "
            "The setup exemplifies contemporary AI development workflows combining coding, training observation, and ergonomic hardware."
        ),
        "evaluation_report": {
            "grounding_status": "Highly Grounded",
            "grounding_score": 95,
            "verified_observations": [
                "Two monitors mounted side-by-side on an articulated mechanical arm.",
                "Left screen shows code editor with syntax-highlighted code; right screen shows ML dashboard.",
                "Keyboards, mouse, desk pad, headphones on stand, coffee mug, and smartphone are all clearly in view.",
                "Exposed brick wall and bookshelf are present in the ambient background."
            ],
            "possible_omissions": [
                "Specific quantitative dashboard readings (Loss: 0.042, Accuracy: 98.1%, GPU: 78%) are often missed unless OCR is triggered.",
                "The miniature robot collectible figurine on the upper bookshelf is a subtle visual element often neglected.",
                "The exact time displayed on the smartphone lock screen ('17:42') is rarely extracted by standard vision prompts."
            ],
            "unsupported_observations": [
                "Asserting the specific graphics card model (e.g. 'NVIDIA RTX 4090') is unsupported since only the GPU percentage (78%) is visible.",
                "Claiming an engineer is currently sitting at the desk is an hallucination since the chair and person are out of frame.",
                "Specifying whether the keyboard switches are 'Cherry MX Red' cannot be determined from keycap appearance alone."
            ],
            "limitations_analysis": (
                "While high-level objects (monitors, keyboard, mug) are identified with near-perfect recall, tiny screen text and "
                "background decorative figurines require high-resolution attention mechanisms. Multimodal models must avoid inferring "
                "unseen hardware components (e.g. internal PC specs)."
            )
        }
    },
    "everyday": {
        "id": "everyday",
        "title": "Everyday Objects: Cozy Morning Study Desk",
        "category": "Everyday Objects",
        "filename": "everyday_coffee_desk.jpg",
        "short_label": "3. Everyday (Coffee & Study Desk)",
        "ground_truth_description": (
            "A warm, serene still life capturing a cozy morning study setting on a weathered rustic wooden table. "
            "A speckled ceramic mug with hot latte rests on a square wooden coaster, displaying delicate heart-shaped latte art. "
            "Beside it lies an open lined notebook with handwritten cursive notes titled 'Notes - 15 Oct' and 'Coffee & Thoughts'. "
            "A premium fountain pen with tortoise-shell marble patterning rests across the open pages. "
            "Adjacent to the journal are tortoise-shell reading spectacles and a small green echeveria succulent plant potted "
            "in a weathered terracotta pot. Soft morning sunlight streams from an adjacent window, creating gentle shadows and highlights."
        ),
        "important_elements": [
            "Ceramic speckled mug filled with latte and heart latte art",
            "Square wooden drink coaster beneath the coffee mug",
            "Open lined journal/notebook with handwritten cursive ink notes",
            "Handwritten title: 'Notes - 15 Oct' and 'Coffee & Thoughts'",
            "Tortoise-shell pattern fountain pen with gold nib resting on journal",
            "Tortoise-shell optical reading glasses / spectacles",
            "Potted green succulent (Echeveria) in a rustic weathered clay pot",
            "Rustic wooden table surface with visible timber grain and textures",
            "Soft directional morning sunlight and natural window illumination",
            "Blurred indoor background with books and window sill plants"
        ],
        "caption": "A peaceful morning study desk with warm latte art, handwritten journal, reading glasses, and a potted succulent.",
        "summary": (
            "A quiet study corner is captured in soft morning light, centered around a fresh cup of coffee with latte art and an open journal. "
            "Accompanying reading glasses and a potted succulent add a calm, contemplative ambiance. The composition illustrates a reflective morning routine dedicated to writing and study."
        ),
        "evaluation_report": {
            "grounding_status": "Highly Grounded",
            "grounding_score": 96,
            "verified_observations": [
                "Latte art clearly depicts a heart shape in milk micro-foam.",
                "Notebook is open to ruled pages containing legible handwritten cursive notes.",
                "Fountain pen and eyeglasses share matching tortoise-shell / amber mottled resin patterns.",
                "Table surface is distressed natural timber with authentic grain and wear marks."
            ],
            "possible_omissions": [
                "The specific handwritten date header 'Notes - 15 Oct' is often omitted as mere 'handwritten text'.",
                "The textured speckles on the ceramic mug and the material of the rustic coaster are subtle textural details.",
                "The matching tortoise-shell aesthetic between both the pen barrel and the eyeglass frames is rarely synthesized."
            ],
            "unsupported_observations": [
                "Claiming the beverage is dairy, almond, or oat milk is unsupported by visual inspection alone.",
                "Asserting the notebook contains a diary entry about a specific named individual is an unsupported hallucination.",
                "Claiming the fountain pen is an expensive brand (e.g. 'Montblanc') is unverified as brand engraving is not legible."
            ],
            "limitations_analysis": (
                "Everyday still-life images have high aesthetic appeal. Models perform well on object categorization (mug, glasses, pen, plant) "
                "but can easily hallucinate taste, temperature (beyond steam hints), or author identity. Grounding requires strictly distinguishing "
                "visible attributes from imagined backstory."
            )
        }
    }
}
