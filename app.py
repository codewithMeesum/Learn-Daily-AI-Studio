import streamlit as st
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# ==========================================
# 1. SCHEMAS & PROMPTS
# ==========================================
class PollOutput(BaseModel):
    question: str
    options: list[str]

class EngagementOutput(BaseModel):
    question: str
    options: list[str]

class ContentPackage(BaseModel):
    best_hook: str = Field(description="The single strongest viral hook, entirely in lowercase.")
    hooks: list[str] = Field(description="10 different hook variations, all entirely in lowercase.")
    caption_body: str = Field(description="The main Instagram caption body (sentence case).")
    poll: PollOutput
    engagement: EngagementOutput
    seo_keywords: list[str]
    keyword_tags: list[str]
    hashtags: list[str]
    accuracy_notes: list[str] = Field(description="Internal notes about verified vs uncertain claims.")

SYSTEM_PROMPT = """
You are the content strategist for Learn Daily AI (@learningdailyai).
Your job is to transform the supplied image/text into an engaging Instagram package.

RULES:
1. ACCURACY > VIRALITY. Never invent facts, dates, stats, or quotes.
2. NO HYPERBOLE. Don't claim "first", "largest", or "revolutionary" unless strictly supported.
3. LOWERCASE HOOKS. All hooks MUST be strictly lowercase (e.g., "you won't believe what terry davis built.").
4. CAPTION STYLE. Professional, natural, standard sentence case. 
5. NO FAKE SCORES. Pick the best hook naturally.
6. NO ADDED CTAs. The system adds "Follow us" automatically.

PROCESS:
Analyze content -> Separate fact from assumption -> Write 10 lowercase hooks -> Pick the best -> Write caption -> Generate SEO/Tags/Poll -> Note accuracy adjustments.
"""

# ==========================================
# 2. CORE LOGIC
# ==========================================
def generate_content(image, description: str) -> ContentPackage:
    if "GEMINI_API_KEY" not in st.secrets:
        raise ValueError("Gemini API key is missing. Add GEMINI_API_KEY to Streamlit Secrets.")
    
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    contents = []
    if image: contents.append(image)
    if description.strip(): contents.append(description.strip())
        
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=ContentPackage,
        temperature=0.4, 
    )
    
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=contents,
        config=config,
    )
    
    if not response.text:
        raise RuntimeError("Model returned an empty response.")
        
    return ContentPackage.model_validate_json(response.text)

# ==========================================
# 3. UI INJECTION & CSS
# ==========================================
st.set_page_config(page_title="Learn Daily AI | Studio", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    /* Dark Premium Theme */
    :root {
        --background: #0E1117;
        --text-main: #FFFFFF;
        --text-muted: #A0AEC0;
        --accent: #6B46C1;
        --border: #2D3748;
    }
    #MainMenu, header, footer {visibility: hidden;}
    .block-container { max-width: 800px; padding-top: 2rem; padding-bottom: 5rem; }
    h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.02em !important; }
    .brand-subtitle { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); margin-bottom: 0px; }
    .brand-title { font-size: 2.5rem; margin-top: -10px; margin-bottom: 5px; color: var(--text-main); }
    .brand-desc { font-size: 1rem; margin-bottom: 2rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border); color: var(--text-muted); }
    .stButton > button { width: 100%; background-color: var(--text-main) !important; color: var(--background) !important; font-weight: 600 !important; border-radius: 8px !important; transition: all 0.2s ease !important; }
    .stButton > button:hover { transform: translateY(-1px); }
    .stTextArea textarea { background-color: #1A202C !important; border: 1px solid var(--border) !important; color: var(--text-main) !important; border-radius: 8px !important; }
    .app-footer { text-align: center; margin-top: 4rem; padding-top: 2rem; border-top: 1px solid var(--border); font-size: 0.85rem; color: var(--text-muted); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. FRONTEND LAYOUT
# ==========================================
st.markdown('<p class="brand-subtitle">Content Studio</p>', unsafe_allow_html=True)
st.markdown('<h1 class="brand-title">LEARN DAILY AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="brand-desc">Turn your content into a ready-to-post Instagram package.</p>', unsafe_allow_html=True)

# --- State ---
if 'generated_content' not in st.session_state: st.session_state.generated_content = None
if 'compiled_post' not in st.session_state: st.session_state.compiled_post = None

# --- Inputs ---
st.markdown("### 1. Upload Content")
uploaded_file = st.file_uploader("Drop image here", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")
image = Image.open(uploaded_file) if uploaded_file else None
if image: st.image(image, use_container_width=True)

st.markdown("### 2. Context & Details")
description = st.text_area("Context", height=150, label_visibility="collapsed", placeholder="Paste reel description, transcript, or explain the context...")

# --- Action ---
if st.button("GENERATE CONTENT"):
    if not image and not description.strip():
        st.warning("Please upload an image or provide a description.")
    else:
        with st.spinner("Analyzing content & building package..."):
            try:
                res = generate_content(image, description)
                st.session_state.generated_content = res
                
                fixed_cta = "Follow @learningdailyai | Here's learn something Daily."
                
                st.session_state.compiled_post = f"""{res.best_hook}

{res.caption_body}

{fixed_cta}

---------------------
POLL:
{res.poll.question}
Options: {', '.join(res.poll.options)}

---------------------
ENGAGEMENT:
{res.engagement.question}
Options: {', '.join(res.engagement.options)}

---------------------
SEO & TAGS:
Keywords: {', '.join(res.seo_keywords)}
Tags: {', '.join(res.keyword_tags)}

---------------------
{' '.join(res.hashtags)}"""
            except Exception as e:
                st.error(str(e) if isinstance(e, ValueError) else "Something went wrong while generating the content. Please try again.")

# --- Results ---
if st.session_state.generated_content:
    st.markdown("---")
    res = st.session_state.generated_content
    
    st.markdown("### 🔥 BEST HOOK")
    st.code(res.best_hook, language="markdown")
    
    st.markdown("### 📝 CAPTION")
    st.code(f"{res.caption_body}\n\nFollow @learningdailyai | Here's learn something Daily.", language="markdown")
    
    st.markdown("### 📊 POLL & ENGAGEMENT")
    st.markdown(f"**Poll:** {res.poll.question}")
    for opt in res.poll.options: st.markdown(f"- {opt}")
    st.markdown(f"**Question:** {res.engagement.question}")
    for opt in res.engagement.options: st.markdown(f"- {opt}")
        
    st.markdown("### #️⃣ DISCOVERY")
    st.code(" ".join(res.hashtags), language="markdown")
    
    with st.expander("View 10 Hook Variations"):
        for i, hook in enumerate(res.hooks, 1): st.markdown(f"{i}. {hook}")
            
    with st.expander("View SEO & Tags"):
        st.markdown("**SEO:** " + ", ".join(res.seo_keywords))
        st.markdown("**Tags:** " + ", ".join(res.keyword_tags))
        
    if res.accuracy_notes:
        with st.expander("⚠️ Accuracy & Fact-Check Notes"):
            for note in res.accuracy_notes: st.markdown(f"- {note}")

    st.markdown("---")
    st.markdown("### 📋 COPY COMPLETE POST")
    st.info("Click the copy icon in the top right of the box below to grab everything at once.")
    st.code(st.session_state.compiled_post, language="markdown")

st.markdown('<div class="app-footer">Follow @learningdailyai | Here\'s learn something Daily.</div>', unsafe_allow_html=True)