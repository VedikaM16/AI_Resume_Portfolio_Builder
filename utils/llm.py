from transformers import pipeline
import random

print("LLM MODULE LOADED")

enhancer = pipeline(
    task="text2text-generation",
    model="google/flan-t5-base"
)

# ---------------- Role-specific bullets for worked-at (full-time) ----------------
ROLE_BULLETS_WORKED = {
    "HR": [
        "Managed recruitment and hiring processes",
        "Oversaw onboarding and employee integration",
        "Implemented HR policies and compliance",
        "Handled employee relations and engagement",
        "Organized training and development programs",
        "Facilitated performance reviews and feedback"
    ],
    "AI Engineer": [
        "Developed AI/ML models and pipelines",
        "Collaborated with cross-functional teams",
        "Optimized machine learning solutions",
        "Deployed AI systems for production",
        "Performed model evaluation and tuning",
        "Researched new AI technologies"
    ],
    "Software Engineer": [
        "Developed scalable software solutions",
        "Implemented new features and modules",
        "Maintained code quality and standards",
        "Optimized application performance",
        "Debugged and resolved technical issues",
        "Collaborated with cross-functional teams"
    ],
    "Designer": [
        "Created user-focused designs",
        "Improved UI/UX",
        "Collaborated with product and development teams",
        "Designed prototypes and mockups",
        "Conducted user research",
        "Developed creative visual assets"
    ],
    "Manager": [
        "Led team projects and coordinated resources",
        "Ensured timely delivery of tasks",
        "Managed stakeholders and team members",
        "Planned and allocated budgets",
        "Monitored performance metrics"
    ],
    "Data Scientist": [
        "Analyzed large datasets",
        "Built predictive models",
        "Visualized insights",
        "Deployed models into production",
        "Researched new data techniques"
    ],
    "Product Manager": [
        "Defined product roadmap and features",
        "Coordinated cross-functional teams",
        "Monitored product performance",
        "Collected user feedback",
        "Ensured timely feature delivery"
    ],
    "Marketing Specialist": [
        "Planned and executed campaigns",
        "Analyzed market trends",
        "Managed social media presence",
        "Created marketing content",
        "Monitored campaign performance"
    ],
    "Sales Executive": [
        "Managed client accounts",
        "Generated leads and closed deals",
        "Negotiated contracts",
        "Prepared sales reports",
        "Maintained CRM records"
    ],
    "Teacher": [
        "Planned and delivered lessons",
        "Managed classroom activities",
        "Assessed student performance",
        "Provided mentorship",
        "Prepared teaching materials"
    ],
    # Add more full-time roles here
}

# ---------------- Role-specific bullets for interned-at (internship) ----------------
ROLE_BULLETS_INTERN = {
    "HR": [
        "Assisted in recruitment and interviews",
        "Supported onboarding processes",
        "Maintained employee records",
        "Helped organize training sessions",
        "Shadowed HR managers"
    ],
    "AI Engineer": [
        "Assisted in developing AI models",
        "Prepared datasets for analysis",
        "Tested model performance",
        "Documented experiments",
        "Shadowed senior engineers"
    ],
    "Software Engineer": [
        "Assisted in coding modules",
        "Performed unit testing",
        "Debugged issues under supervision",
        "Documented code",
        "Collaborated with senior engineers"
    ],
    "Designer": [
        "Created UI/UX mockups under guidance",
        "Prepared graphics and assets",
        "Participated in brainstorming sessions",
        "Helped test prototypes",
        "Shadowed senior designers"
    ],
    "Manager": [
        "Assisted in project coordination",
        "Prepared progress reports",
        "Helped organize meetings",
        "Supported resource planning",
        "Shadowed senior managers"
    ],
    "Data Scientist": [
        "Assisted in data cleaning",
        "Performed exploratory analysis",
        "Helped build small models",
        "Created visualizations",
        "Shadowed senior data scientists"
    ],
    "Product Manager": [
        "Assisted in feature documentation",
        "Monitored product progress",
        "Prepared reports",
        "Collected user feedback",
        "Shadowed senior PMs"
    ],
    "Marketing Specialist": [
        "Helped create marketing content",
        "Monitored campaign performance",
        "Assisted in social media management",
        "Researched market trends",
        "Prepared marketing reports"
    ],
    "Sales Executive": [
        "Assisted in client communications",
        "Prepared sales reports",
        "Shadowed senior sales executives",
        "Helped in lead generation",
        "Maintained CRM entries"
    ],
    "Teacher": [
        "Assisted in classroom activities",
        "Prepared teaching materials",
        "Observed teaching methods",
        "Helped students with exercises",
        "Supported grading"
    ],
    # Add more intern roles here
}

# Generic fallback bullets
GENERIC_BULLETS_WORKED = [
    "Performed core responsibilities with excellence",
    "Collaborated effectively with team members",
    "Completed assigned tasks professionally",
    "Contributed to team goals",
    "Implemented standard procedures"
]

GENERIC_BULLETS_INTERN = [
    "Assisted in day-to-day tasks",
    "Collaborated with team members",
    "Supported project activities",
    "Shadowed senior team members",
    "Completed assigned tasks professionally"
]

# ---------------- Enhancement function ----------------


def enhance_text(user_text: str, role: str, section: str) -> str:
    """
    Enhances ONLY the Experience section.
    Preserves company, role, duration exactly as entered.
    Adds 2–3 realistic role-based responsibilities.
    """

    if not user_text or not user_text.strip():
        return user_text

    if section.lower() != "experience":
        return user_text  # DO NOT touch other sections

    role_key = role.strip()
    lines = user_text.split("\n")
    enhanced_lines = []

    for line in lines:
        clean = line.strip()
        if not clean:
            enhanced_lines.append("")
            continue

        is_intern = "intern" in clean.lower()

        if is_intern:
            bullets = ROLE_BULLETS_INTERN.get(role_key, GENERIC_BULLETS_INTERN)
        else:
            bullets = ROLE_BULLETS_WORKED.get(role_key, GENERIC_BULLETS_WORKED)

        selected = random.sample(bullets, k=min(3, len(bullets)))
        enhanced_line = clean + "; " + "; ".join(selected)

        enhanced_lines.append(enhanced_line)

    return "\n".join(enhanced_lines)
