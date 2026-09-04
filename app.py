import streamlit as st

from email_generator import generate_email


st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)


st.markdown(
    """
    <style>

    .main {
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .email-header {
        font-size: 22px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="title">✉️ AI Email Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Generate professional emails in seconds using AI'
    '</div>',
    unsafe_allow_html=True
)


try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

except KeyError:
    st.error(
        "GROQ_API_KEY is not configured. "
        "Please add it to your Streamlit Secrets."
    )
    st.stop()


st.subheader("📝 Email Details")


recipient = st.text_input(
    "Recipient",
    placeholder="e.g. Professor, Manager, Client"
)


purpose = st.selectbox(
    "Purpose",
    [
        "Request",
        "Thank You",
        "Follow Up",
        "Apology",
        "Introduction",
        "Meeting",
        "Application",
        "Complaint",
        "Other"
    ]
)


topic = st.text_input(
    "Email Topic",
    placeholder="e.g. Request for assignment extension"
)


key_points = st.text_area(
    "Key Points",
    placeholder=(
        "Enter the important information you want "
        "to include in the email..."
    ),
    height=150
)


col1, col2 = st.columns(2)


with col1:
    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Friendly",
            "Formal",
            "Casual",
            "Persuasive"
        ]
    )


with col2:
    length = st.selectbox(
        "Length",
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )


st.write("")


generate_button = st.button(
    "✨ Generate Email",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not recipient.strip():
        st.warning("Please enter the recipient.")
        st.stop()

    if not topic.strip():
        st.warning("Please enter the email topic.")
        st.stop()

    if not key_points.strip():
        st.warning("Please enter the key points.")
        st.stop()

    with st.spinner("🤖 Generating your email..."):

        try:
            generated_email = generate_email(
                api_key=GROQ_API_KEY,
                recipient=recipient,
                purpose=purpose,
                topic=topic,
                key_points=key_points,
                tone=tone,
                length=length
            )

            st.session_state["generated_email"] = generated_email

        except Exception as e:
            st.error(
                f"❌ Failed to generate email: {str(e)}"
            )


if "generated_email" in st.session_state:

    st.markdown(
        '<div class="email-header">📧 Generated Email</div>',
        unsafe_allow_html=True
    )

    generated_email = st.session_state["generated_email"]

    st.text_area(
        "Your generated email",
        value=generated_email,
        height=400,
        key="email_output"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="⬇️ Download",
            data=generated_email,
            file_name="generated_email.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        if st.button(
            "🗑️ Clear",
            use_container_width=True
        ):
            del st.session_state["generated_email"]
            st.rerun()


st.divider()

st.caption(
    "Powered by Groq + GPT • Built with Streamlit"
)
