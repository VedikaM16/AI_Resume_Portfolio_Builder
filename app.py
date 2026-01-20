import streamlit as st
import base64
from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils.llm import enhance_text
from utils.themes import THEMES
from ats import ats_analysis

st.set_page_config(page_title="AI Resume & Portfolio Builder", layout="wide")

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("AI Resume & Portfolio Builder Login")
    with st.form("login_form"):
        login_email = st.text_input("Gmail", placeholder="example@gmail.com")
        login_password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Login")

    if login_submitted:
        st.session_state.logged_in = True
        st.session_state.user_email = login_email
    else:
        st.warning("Please login to access the builder.")
        st.stop()

# ---------- MAIN APP ----------
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.user_email}")

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"])
    )

    theme_choice = st.selectbox("Choose Theme", THEMES.keys())
    theme = THEMES[theme_choice]

    st.markdown(
        f"<style>.stApp{{background-color:{theme.get('bg', '#fff')};}}</style>",
        unsafe_allow_html=True
    )

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        role = st.text_input("Target Role")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn")

        st.subheader("Education")
        secondary = st.text_input("Secondary School Name")
        secondary_year = st.text_input("Year of Completion (Secondary)")
        higher_secondary = st.text_input("Higher Secondary / Diploma Name")
        higher_secondary_year = st.text_input(
            "Year of Completion (HSC/Diploma)")
        college = st.text_input("Graduation College Name")
        college_year = st.text_input("Year of Graduation")

        st.subheader("Skills")
        skills = st.text_area("Skills (one per line)")

        st.subheader("Projects")
        projects = st.text_area("Projects (one per line)")
        project_links = st.text_area("Project Links (same order)")

        st.subheader("Experience")
        experience = st.text_area("Experience (describe briefly)")

        st.subheader("Achievements")
        achievements = st.text_area("Achievements")

        option = st.multiselect("Generate", ["Resume", "Portfolio"])
        submitted = st.form_submit_button("Generate")

    image = st.file_uploader("Upload Image (Portfolio only)", ["jpg", "png"])

    if submitted:
        education = []
        if secondary:
            education.append({"level": "Secondary School",
                             "institution": secondary, "year": secondary_year})
        if higher_secondary:
            education.append({"level": "Higher Secondary / Diploma",
                             "institution": higher_secondary, "year": higher_secondary_year})
        if college:
            education.append(
                {"level": "Graduation", "institution": college, "year": college_year})

        enhanced_experience = enhance_text(experience, role, "experience")

        skills_list = [s.strip() for s in skills.split("\n") if s.strip()]
        experience_list = [s.strip()
                           for s in enhanced_experience.split("\n") if s.strip()]
        achievements_list = [s.strip()
                             for s in achievements.split("\n") if s.strip()]
        projects_list = [p.strip() for p in projects.split("\n") if p.strip()]
        project_links_list = [l.strip()
                              for l in project_links.split("\n") if l.strip()]

        projects_with_links = []
        for i, project in enumerate(projects_list):
            link = project_links_list[i] if i < len(
                project_links_list) else None
            projects_with_links.append({"project": project, "link": link})

        full_resume_text = "\n".join([
            "\n".join(skills_list),
            "\n".join(projects_list),
            "\n".join(experience_list),
            "\n".join(achievements_list)
        ])

        ats_result = ats_analysis(full_resume_text, role)

        st.subheader("ATS Analysis")
        st.metric("ATS Score", f"{ats_result['score']}%")
        st.write("Matched Keywords:", ats_result["matched"])
        st.write("Missing Keywords:", ats_result["missing"])

        # ---------- RESUME ----------
        if "Resume" in option:
            template = env.get_template("resume_template.html")
            resume_html = template.render(
                name=name,
                role=role,
                email=email,
                phone=phone,
                linkedin=linkedin,
                education=education,
                skills=skills_list,
                projects=projects_list,                 # <-- KEEP
                projects_with_links=projects_with_links,  # <-- ADD
                experience=experience_list,
                achievements=achievements_list
            )
            st.components.v1.html(resume_html, height=900, scrolling=True)
            st.download_button("Download Resume",
                               resume_html, f"{name}_resume.html")

        # ---------- PORTFOLIO ----------
        if "Portfolio" in option:
            if not image:
                st.error("Image required for portfolio")
                st.stop()

            img = base64.b64encode(image.read()).decode()
            template = env.get_template("portfolio_template.html")
            portfolio_html = template.render(
                name=name,
                role=role,
                education=education,
                skills=skills_list,
                projects_with_links=projects_with_links,
                experience=experience_list,
                achievements=achievements_list,
                email=email,
                phone=phone,
                linkedin=linkedin,
                image=f"data:image/png;base64,{img}",
                theme=theme
            )

            st.components.v1.html(portfolio_html, height=900, scrolling=True)
            st.download_button("Download Portfolio",
                               portfolio_html, f"{name}_portfolio.html")
