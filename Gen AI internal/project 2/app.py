"""
Multimodal AI-Based Image Understanding System
Streamlit Application
"""

import os
from pathlib import Path
from PIL import Image
import streamlit as st

from sample_data import SAMPLE_IMAGES
from analyzer import analyze_image, extract_image_metadata

# Page Configuration
st.set_page_config(
    page_title="Multimodal AI - Image Understanding System",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .badge-primary { background-color: #EEF2FF; color: #4F46E5; border: 1px solid #C7D2FE; }
    .badge-success { background-color: #ECFDF5; color: #059669; border: 1px solid #A7F3D0; }
    .badge-info { background-color: #F0F9FF; color: #0284C7; border: 1px solid #BAE6FD; }
    .badge-warning { background-color: #FFFBEB; color: #D97706; border: 1px solid #FDE68A; }
    
    .card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem;
    }
    .card-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .chip {
        display: inline-block;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 0.35rem 0.7rem;
        margin: 0.25rem;
        font-size: 0.88rem;
        color: #334155;
    }
    .eval-box-verified {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 0.85rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
    }
    .eval-box-omission {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 0.85rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
    }
    .eval-box-unsupported {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 0.85rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)

# Base sample paths
CURRENT_DIR = Path(__file__).parent.resolve()
SAMPLES_DIR = CURRENT_DIR / "samples"

# Initialize Session State
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "selected_sample_id" not in st.session_state:
    st.session_state.selected_sample_id = "education"
if "image_source" not in st.session_state:
    st.session_state.image_source = "sample"

# Sidebar: Controls & Configuration
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    st.markdown(
        "This system supports **Live Multimodal Vision AI** (Gemini 1.5 Flash) "
        "and includes a **Grounded Reference Engine** for offline viva/practical evaluation."
    )
    
    api_key_input = st.text_input(
        "Google Gemini API Key (Optional)",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Free key from https://aistudio.google.com/ - Leave empty for zero-config offline mode."
    )
    
    if api_key_input:
        st.success("🔑 API Key provided: Live Gemini Multimodal active.")
    else:
        st.info("💡 No API key: Grounded Reference Engine active (Works offline with zero configuration).")
        
    st.markdown("---")
    st.markdown("### 📚 Syllabus & Lab Context")
    st.markdown(
        "- **Course**: Multimodal Generative AI\n"
        "- **Lab**: Image Understanding System\n"
        "- **Architecture**: Vision-Language Model (VLM)\n"
        "- **Focus**: Grounding vs Hallucination Audit"
    )
    
    with st.expander("🎓 College Viva Q&A Guide", expanded=False):
        st.markdown("""
        **Q1: What is a Multimodal Vision-Language Model (VLM)?**  
        *Ans:* A multimodal model processes both visual tokens (from image encoders like ViT/SigLIP) and text tokens through unified transformer attention layers to generate cross-modal reasoning.

        **Q2: What is visual grounding?**  
        *Ans:* Grounding means tying generated text strictly to verified visual evidence (pixels). If an observation cannot be confirmed from the image, it is ungrounded.

        **Q3: How do vision AI hallucinations occur?**  
        *Ans:* When language priors overpower visual attention, the model guesses plausible-sounding details (e.g. brand names, unverified identities) not present in the image.
        """, unsafe_allow_html=True)

# Main Header
st.markdown('<div class="main-title">Multimodal AI-Based Image Understanding System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">'
    '<span class="badge badge-primary">Multimodal AI</span>'
    '<span class="badge badge-success">Vision-Language Grounding</span>'
    '<span class="badge badge-info">Zero-Config / Gemini Vision</span>'
    '<span class="badge badge-warning">AI Output Validation</span>'
    '<br><br>Analyze complex visual scenes, extract salient objects and activities, generate concise captions and summaries, '
    'and audit output fidelity through a rigorous evaluation report.'
    '</div>', 
    unsafe_allow_html=True
)

# Section 1: Image Selection
st.markdown("### 1. Image Selection")
source_option = st.radio(
    "Choose Image Source:",
    options=["Select Curated Sample Image (Education, Technology, Everyday)", "Upload Custom Image"],
    horizontal=True
)

current_image = None
current_sample_id = None

if "Curated Sample" in source_option:
    st.session_state.image_source = "sample"
    col1, col2, col3 = st.columns(3)
    
    sample_options = [
        ("education", "🎓 Education", "Machine Learning College Lecture", SAMPLES_DIR / "education_classroom.jpg"),
        ("technology", "💻 Technology", "AI Developer Dual-Monitor Workstation", SAMPLES_DIR / "technology_workspace.jpg"),
        ("everyday", "☕ Everyday Objects", "Cozy Morning Coffee & Study Desk", SAMPLES_DIR / "everyday_coffee_desk.jpg")
    ]
    
    selected_sample = st.selectbox(
        "Choose one of the three sample domains:",
        options=["education", "technology", "everyday"],
        format_func=lambda x: SAMPLE_IMAGES[x]["short_label"],
        index=0
    )
    current_sample_id = selected_sample
    
    sample_file = SAMPLES_DIR / SAMPLE_IMAGES[selected_sample]["filename"]
    if sample_file.exists():
        try:
            current_image = Image.open(sample_file)
        except Exception as e:
            st.error(f"Error loading sample image: {e}")
    else:
        st.error(f"Sample file not found at: {sample_file}")

else:
    st.session_state.image_source = "custom"
    current_sample_id = None
    uploaded_file = st.file_uploader(
        "Upload your image (PNG, JPG, JPEG, WEBP):",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload any clear photograph or digital image."
    )
    if uploaded_file is not None:
        try:
            current_image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Invalid image file: {e}")

# Action Button
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2 = st.columns([1, 4])
with btn_col1:
    analyze_btn = st.button("🚀 Analyze Image", type="primary", use_container_width=True)

if analyze_btn:
    if current_image is None:
        st.warning("Please select or upload an image before analyzing.")
    else:
        with st.spinner("Processing image through Multimodal Understanding Pipeline..."):
            result = analyze_image(
                img=current_image,
                sample_id=current_sample_id,
                api_key=api_key_input
            )
            st.session_state.analysis_result = result
            st.session_state.selected_image = current_image

# Display Section (Always show if image is selected or analyzed)
display_img = st.session_state.selected_image if st.session_state.selected_image else current_image
analysis = st.session_state.analysis_result

if display_img is not None:
    st.markdown("---")
    st.markdown("### 2. Visual Inspection & Multimodal Analysis")
    
    img_col, summary_col = st.columns([1, 1])
    
    with img_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🖼️ Selected Visual Input</div>', unsafe_allow_html=True)
        st.image(display_img, use_container_width=True)
        
        meta = extract_image_metadata(display_img)
        st.markdown(
            f"**Metadata:** `{meta['width']} x {meta['height']} px` | "
            f"**Aspect Ratio:** `{meta['aspect_ratio']}` | "
            f"**Color Tone:** `{meta['color_tone']}` | "
            f"**Lighting:** `{meta['relative_brightness']}`"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with summary_col:
        if analysis:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div class="card-header">⚡ Engine: {analysis.get("engine", "Multimodal Engine")}</div>', unsafe_allow_html=True)
            
            if analysis.get("warning"):
                st.info(analysis["warning"])
                
            st.markdown("#### 📌 Concise Image Caption")
            st.info(f"**"{analysis['caption']}"**")
            
            st.markdown("#### 📖 Contextual Summary")
            st.write(analysis["summary"])
            
            eval_rep = analysis.get("evaluation_report", {})
            st.markdown(
                f"**Grounding Index:** `{eval_rep.get('grounding_score', 90)}%` &nbsp;|&nbsp; "
                f"**Status:** `{eval_rep.get('grounding_status', 'Grounded')}`"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("👉 Click the **'Analyze Image'** button above to generate the Multimodal Description, Elements, Caption, Summary, and Evaluation Report.")

    # Detailed Analysis Sections
    if analysis:
        st.markdown("### 3. Detailed Multimodal Breakdown")
        
        # Section B: Image Description
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📝 Comprehensive Image Description</div>', unsafe_allow_html=True)
        st.write(analysis["description"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Section C: Important Elements
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">🏷️ Important Objects, Visible Activities & Visual Elements</div>', unsafe_allow_html=True)
        st.markdown("Extracted salient entities directly grounded in the visual frame:")
        
        chips_html = "".join([f'<span class="chip">🔍 {elem}</span>' for elem in analysis.get("important_elements", [])])
        st.markdown(f'<div style="margin-top: 0.5rem;">{chips_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Section E: Rigorous Evaluation Report
        st.markdown("### 4. Evaluation Report: Grounding & AI Output Validation")
        st.markdown(
            "Comparing generated descriptions with visual pixels to distinguish verified ground truth "
            "from possible omissions, unsupported assertions, and model limitations."
        )
        
        eval_data = analysis.get("evaluation_report", {})
        
        tab_verified, tab_omissions, tab_unsupported, tab_limits = st.tabs([
            "✅ Verified Observations",
            "⚠️ Possible Omissions (Min. 2)",
            "🚫 Potential Unsupported Observations",
            "🔬 Limitations & Guardrails"
        ])
        
        with tab_verified:
            st.markdown("#### Observations Directly Verified from Image Content")
            for obs in eval_data.get("verified_observations", []):
                st.markdown(f'<div class="eval-box-verified"><b>[VERIFIED]</b> {obs}</div>', unsafe_allow_html=True)
                
        with tab_omissions:
            st.markdown("#### Identifiable Details That Were Omitted or Glossed Over")
            st.caption("Demonstrating at least two fine-grained details present in the image that general descriptions tend to omit:")
            for om in eval_data.get("possible_omissions", []):
                st.markdown(f'<div class="eval-box-omission"><b>[POTENTIAL OMISSION]</b> {om}</div>', unsafe_allow_html=True)
                
        with tab_unsupported:
            st.markdown("#### Unsupported Observations & Hallucination Risks")
            st.caption("Distinguishing verified facts from speculative guesses that cannot be verified solely from the image:")
            for un in eval_data.get("unsupported_observations", []):
                st.markdown(f'<div class="eval-box-unsupported"><b>[UNSUPPORTED INFERENCE]</b> {un}</div>', unsafe_allow_html=True)
                
        with tab_limits:
            st.markdown("#### Model Architecture Limitations")
            st.write(eval_data.get("limitations_analysis", "Models operate strictly on static pixel representations without temporal or audio grounding."))
            st.markdown("""
            - **Resolution Constraints**: Small background text and distant objects fall below the patch token threshold.
            - **Visual-Language Prior Bias**: Models often predict stereotypical attributes (e.g. guessing brand names or laptop specs) rather than confirming pixels.
            - **Lack of Non-Visual Modalities**: Static images cannot confirm sound, intention, brand provenance, or internal device components.
            """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding: 1rem 0;">'
    'Multimodal Generative AI – Image Understanding System | Built with Streamlit, Pillow & Google Gemini Multimodal API'
    '</div>', 
    unsafe_allow_html=True
)
