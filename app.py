import streamlit as st
from logs.services.assistant import process_request

st.set_page_config(
    page_title="Code Explainer",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Session state

st.session_state.setdefault("result", None)
st.session_state.setdefault("status", "idle")  # idle | running | done

# Styling

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg: #0B0E14;
        --panel: #11151C;
        --panel-alt: #161B22;
        --border: #262C38;
        --text: #E6EDF3;
        --muted: #7D8590;
        --accent: #E3B341;
        --accent-2: #56D4C1;
        --danger: #FF5F56;
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .stApp {
        background-color: var(--bg);
        background-image: radial-gradient(circle, rgba(255,255,255,0.035) 1px, transparent 1px);
        background-size: 26px 26px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--text);
    }

    .block-container {
        max-width: 1160px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* ---------- Hero ---------- */
    .hero { margin-bottom: 2.4rem; }
    .hero-eyebrow {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: var(--accent-2);
        letter-spacing: 0.02em;
        margin-bottom: 0.6rem;
    }
    .hero-eyebrow::before { content: " "; color: var(--muted); }
    .hero-title {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 700;
        font-size: 2.6rem;
        line-height: 1.15;
        margin: 0 0 0.6rem 0;
        color: var(--text);
    }
    .cursor {
        display: inline-block;
        width: 0.5em;
        background: var(--accent);
        animation: blink 1.1s steps(1) infinite;
        margin-left: 2px;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: var(--muted);
        max-width: 560px;
        margin: 0;
    }
    @keyframes blink { 50% { opacity: 0; } }

    /* ---------- Panel chrome ---------- */
    .panel-chrome {
        display: flex;
        align-items: center;
        gap: 6px;
        background: var(--panel-alt);
        border: 1px solid var(--border);
        border-bottom: none;
        border-radius: 10px 10px 0 0;
        padding: 10px 14px;
    }
    .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .dot.red { background: #FF5F56; }
    .dot.amber { background: #FFBD2E; }
    .dot.green { background: #27C93F; }
    .filename {
        margin-left: 8px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: var(--muted);
    }
    .chrome-spacer { flex-grow: 1; }
    .status-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .status-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--muted); }
    .status-dot.running { background: var(--accent); animation: pulse 1s ease-in-out infinite; }
    .status-dot.done { background: var(--accent-2); }
    @keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

    /* Container-key panels */
    .st-key-input_panel, .st-key-output_panel {
        border: 1px solid var(--border);
        border-top: none;
        border-radius: 0 0 10px 10px;
        background: var(--panel);
        padding: 18px 16px 16px 16px;
    }
    .st-key-input_panel [data-testid="stVerticalBlock"],
    .st-key-output_panel [data-testid="stVerticalBlock"] {
        gap: 0.9rem;
    }

    /* ---------- Text area ---------- */
    .stTextArea textarea {
        background: var(--panel-alt) !important;
        color: var(--text) !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus-visible {
        outline: none !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(227, 179, 65, 0.18) !important;
    }
    .stTextArea textarea::placeholder { color: var(--muted) !important; }

    /* ---------- Button ---------- */
    .stButton > button {
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        background: var(--accent);
        color: #1A1305;
        border: none;
        border-radius: 8px;
        padding: 0.65rem 1rem;
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 0 3px rgba(227, 179, 65, 0.25);
        transform: translateY(-1px);
    }
    .stButton > button:focus-visible {
        outline: 2px solid var(--accent-2) !important;
        outline-offset: 2px;
    }

    /* ---------- Output / empty state ---------- */
    .empty-console {
        font-family: 'IBM Plex Mono', monospace;
        color: var(--muted);
        font-size: 0.9rem;
        padding: 0.4rem 0.1rem 1.2rem 0.1rem;
    }
    .empty-console .cursor { background: var(--muted); }

    .st-key-output_panel code {
        background: var(--panel-alt);
        color: var(--accent-2);
        padding: 0.1rem 0.35rem;
        border-radius: 4px;
        font-family: 'IBM Plex Mono', monospace;
    }
    .st-key-output_panel pre {
        background: var(--panel-alt) !important;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem !important;
    }

    /* ---------- Alerts / spinner ---------- */
    [data-testid="stAlert"] {
        font-family: 'IBM Plex Sans', sans-serif;
        border-radius: 8px;
    }
    .stSpinner p {
        font-family: 'IBM Plex Mono', monospace !important;
        color: var(--muted) !important;
    }

    .footnote {
        margin-top: 2.4rem;
        color: var(--muted);
        font-size: 0.8rem;
        font-family: 'IBM Plex Mono', monospace;
    }

    @media (prefers-reduced-motion: reduce) {
        .cursor, .status-dot.running { animation: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Hero

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow"></div>
        <h1 class="hero-title">Your AI Coding Assistant<span class="cursor">&nbsp;</span></h1>   
        <p class="hero-sub">Drop a snippet into the editor on the left. The console on the right
        walks through what it does, step by step.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
# edittttt

# Layout

left, right = st.columns(2, gap="medium")

with left:
    current_code = st.session_state.get("code_input", "")
    line_count = len([l for l in current_code.splitlines() if l != ""]) if current_code.strip() else 0
    st.markdown(
        f"""
        <div class="panel-chrome">
            <span class="dot red"></span><span class="dot amber"></span><span class="dot green"></span>
            <span class="filename">assistant.input</span>
            <span class="chrome-spacer"></span>
            <span class="filename">{line_count} lines</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="input_panel"):
        code = st.text_area(
            "Python code",
            height=360,
            placeholder="Ask anything...\n\nExamples:\n• Explain this Python function\n• Write a Flask API\n• Debug this code",
            label_visibility="collapsed",
            key="code_input",
        )
        button_text = "Ask AI"

run_clicked = st.button(
    button_text,
    use_container_width=True
)

if run_clicked:
        if not code.strip():
            st.warning("Paste some code before running explain().")
        else:
            st.session_state.status = "running"
            with st.spinner("Analyzing your code..."):
                st.session_state.result = process_request(code)  ####
            st.session_state.status = "done"

with right:
    status = st.session_state.status
    status_label = {"idle": "idle", "running": "analyzing", "done": "ready"}[status]
    st.markdown(
        f"""
        <div class="panel-chrome">
            <span class="dot red"></span><span class="dot amber"></span><span class="dot green"></span>
            <span class="filename">assistant.md</span>
            <span class="chrome-spacer"></span>
            <span class="status-pill"><span class="status-dot {status}"></span>{status_label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="output_panel"):
        if st.session_state.result:
            st.markdown(st.session_state.result)
        else:
            st.markdown(
                '<div class="empty-console">Waiting for input<span class="cursor">&nbsp;</span></div>',
                unsafe_allow_html=True,
            )

