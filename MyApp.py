import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import re  # For robust date parsing
from PIL import Image  # For profile picture
import openai
import os # For OpenAI API Key

# --- Skill Scores - Icon-Based Representation - Updated Leadership Skills ---
skill_scores = {
    "Leadership & Strategy 🧭": {
        "Stakeholder Management": 4.5,
        "Strategic Thinking": 5,
        "Building Teams": 5,
        "Long-Term Vision Alignment": 4.5,
        "Risk & Control Management": 4
    },
    "Data Engineering 🧮": {
        "Data Pipeline": 5,
        "Data Modelling": 5,
        "Data Engineering": 5,
        "SQL": 5,
        "Python": 4,
        "GIT": 4,
        "AWS": 4,
        "Snowflake": 4,
        "API": 4,
        "Data Governance": 4,
        "Platform Eng": 4,
        "AI/NLP": 4
    },
    "BI & Analytics 📊": {
        "BI Product Dev": 5,
        "Data Storytelling": 5,
        "Tableau": 5,
        "Alteryx": 4,
        "Power BI": 4,
        "Teradata": 3
    },
    "Process & Delivery ⚙️": {
        "Iterative Delivery": 4,
        "Agile": 4,
        "Human-Centered Design": 5,
        "Customer Exp": 3
    }
}

skill_categories_order = ["Leadership & Strategy 🧭", "Data Engineering 🧮", "BI & Analytics 📊", "Process & Delivery ⚙️"]

resume_data = {
    "Contact": {
        "Name": "Binay Siddharth",
        "Email": "binay.siddharth@gmail.com",
        "Phone": "+61 451 943 584",
        "LinkedIn": "www.linkedin.com/in/binaysiddharth",
        "GitHub": "github.com/binzidd",
        "Location": "Sydney, AU"
    },
    "Summary": """
    Executive-ready Senior Manager in Financial Services Analytics, specializing in data-driven strategy and high-impact team leadership. Proven ability to deliver cutting-edge data engineering and strategic solutions.
    """,

    "Skills": [
        "Stakeholder Management 🌟",
        "Strategic Thinking 🌟",
        "Building Teams 🌟",
        "Long-Term Vision Alignment 🌟",
        "Risk & Control Management",
        "BI Product Development",
        "Iterative Deliveries",
        "Human Centred Interface Designs",
        "Customer Experience",
        "Data Story Telling",
        "Data Pipeline",
        "Data Modelling",
        "Data Engineering",
        "API",
        "Data Governance and Lineage",
        "SQL",
        "Tableau",
        "Alteryx",
        "Power BI",
        "Teradata",
        "Python",
        "GIT",
        "Agile",
        "AWS",
        "Snowflake",
        "AI/NLP 🚀",
        "Platform Engineering 🚀"
    ],
    "Certifications": [
        "Tableau 5x: Community Leader | Data Scientist | Data Steward | Executive Sponsor | Desktop Specialist",
        "Alteryx 2x: Core & Advanced",
        "AWS: Analytics Service Overview",
        "Snowflake Hands-on Essentials 2x: Data Warehouse | Data Applications",
        "Tableau Certified Designer",
        "Alteryx 2020 Certified Specialist",
        "AWS Certified Cloud Practitioner"
    ],
    "Experience": sorted([
        {
            "Title": "Senior Manager, BI Reporting Hub (Insights and Data)",
            "Company": "Commonwealth Bank of Australia",
            "Dates": "2018 - Current",
            "Location": "Sydney, AU",
            "Description": """
            Collaborating with finance leaders on strategic data-driven decisions. Led high-performing BI Reporting Hub.
            Managed data assets for Executive Leadership, driving decision-making through interactive KPI reports.
            Championed BI innovation and upskilling across the organization.
            """,
            "Learnings": [
                "**Executive Stakeholder Management:** Honed skills in aligning data strategy with executive vision.",
                "**Team Cohesion & Delivery:** Built and led a high-performing team focused on mentorship and collaboration.",
                "**BI Innovation & Upskilling:** Drove a culture of continuous learning and innovation."
            ]
        },
        {
            "Title": "Intern, Business Intelligence and Analytics",
            "Company": "Institute of Analytics and Planning, The University of Sydney",
            "Dates": "2017-18",
            "Location": "Sydney, AU",
            "Description": """
            Implemented agile analytics solutions using Tableau and Alteryx.
            Focused on data mining, cleansing, and transformation for analytics initiatives.
            Collaborated with product owners to gather and visualize business requirements.
            """,
            "Learnings": [
                "**Agile Analytics Implementation:** Applied agile methodologies to deliver analytics projects.",
                "**Data Transformation & Tooling:** Developed data mining, cleansing, and transformation skills.",
                "**Stakeholder Requirement Gathering:** Learned to translate business needs into data solutions."
            ]
        },
        {
            "Title": "Data Engineering Intern, Data and Platform Enablement",
            "Company": "BizCubed Pty Ltd",
            "Dates": "2016-17",
            "Location": "Sydney, AU",
            "Description": """
            Developed performance dashboards and data pipelines for Managed Services.
            Designed heartbeat services and dimensional models for data layer.
            Liaised between engineering, product, and visualization teams.
            """,
            "Learnings": [
                "**Data Pipeline Development:** Built data pipelines and heartbeat services for data management.",
                "**Dimensional Data Modeling:** Developed skills in creating dimensional models.",
                "**Cross-functional Collaboration:** Enhanced liaison skills between diverse teams."
            ]
        },
        {
            "Title": "Production Support Analyst, Subscription Services",
            "Company": "Contracted to Adobe Sys Inc., Tata Consultancy Services",
            "Dates": "2012-15",
            "Location": "Mumbai, India",
            "Description": """
            Managed cross-functional teams and scrum meetings to drive project execution.
            Responsible for metrics generation, reporting, and risk analysis for product launches.
            """,
            "Learnings": [
                "**Cross-functional Project Management:** Coordinated diverse teams and scrum meetings.",
                "**Metrics-Driven Approach:** Learned to define and report key metrics for product performance.",
                "**Risk Analysis & Communication:** Conducted risk analysis and communicated findings."
            ]
        }
    ], key=lambda item: item['Dates'].split('-')[0], reverse=True),
    "Projects": [
        {
            "Section": "Key Projects (Senior Manager Role) 🏆",
            "Projects": [
                {
                    "Name": "Reporting hub for Executive Leadership, strategic measures | Data Lake and Reporting 📊",
                    "Description": "Uplifting manual process by introducing auto-ingest feeds from various source systems, paired with a suite of Tableau reporting. 70% time saved for data reports and modern BI tools utilized for executive leadership engagement."
                },
                {
                    "Name": "Process Efficiency and Data Lineage for Capital Engine ⚙️",
                    "Description": "Cutting load times, removing manual processes and redesigning existing production steps, resulting in a Capital Production Month End lifecycle reduction from 4 WD to 1.5 WD. Achieved 85% faster production process and increased Data Visibility for Governance."
                },
                {
                    "Name": "ELT Scorecard | Strategic Metrics | Data Lake and Visualization Layer ☁️",
                    "DescriptionPoints": [
                        "Creation of conceptual data lake infrastructure and implementation of Extract Load Transform architecture for executive leadership reporting.",
                        "Developing focused executive dashboards in Tableau, enabling drill-through capabilities from strategic measures to financial P&L for executive insights.",
                        "Integrating data from diverse sources, including manual feeds, with robust data lineage tracking for new infrastructure."
                    ]
                },
                {
                    "Name": "Project Spur | Data Transformation and Reporting 🔄",
                    "DescriptionPoints": [
                        "Delivering a strategic data asset enabling the IB&M Performance Reporting team to perform PACC Calculations.",
                        "Ingesting and modelling data from various source systems and subject areas (Risk, Finance, Treasury, Capital) to fit a required schema.",
                        "Separating visualization and data layers, enabling dynamic data refreshes and eliminating manual Flash Reporting processes.",
                        "Achieving process efficiency."
                    ]
                },
                {
                    "Name": "Loan IQ Data Feed Ingestion and Integration with Data Infrastructure 🔗",
                    "DescriptionPoints": [
                        "Capturing document-based files from a new application and integrating it with the capital engine for RWA calculation.",
                        "Data Transformation and Processing in Alteryx with reconciliation for data quality assurance, load assurance, and data delivery.",
                        "Delivering reporting layer to stakeholders on monthly portfolio movement insights."
                    ]
                }
            ]
        },
        {
             "Section": "Key Projects (Intern Roles) 🧑‍🎓",
            "Projects": [
                {
                    "Name": "Canvas Reporting and Student Engagement dashboards 📈",
                    "DescriptionPoints": [
                        "Exploring and designing dashboards for Unit of Study co-ordinators to check student engagement.",
                        "Extracting data from S3, APIs, data modeling, and creating a presentation layer for Aggregated views.",
                        "Implementing RLS on data sets for security."
                    ]
                },
                {
                    "Name": "HDR Students Predictive model for Course Completion 🎯",
                    "DescriptionPoints": [
                        "Working alongside Business Analysts to facilitate reporting on the predictive model.",
                        "Hypothesis - Call to action dashboards for DVC Grants."
                    ]
                },
                {
                    "Name": "National Sales Report | Yahoo7 📰",
                    "DescriptionPoints": [
                        "Creating summary reports on social media interaction across different platforms.",
                        "Developing KPI and OKR monitoring dashboards for stakeholders.",
                        "Ingesting streaming and transactional data from multiple data sources."
                    ]
                },
                {
                    "Name": "Performance Monitoring Report | Managed Services 📊",
                    "DescriptionPoints": [
                        "Generating daily summary reports on server health and status.",
                        "Providing focused commentary on downtime and resolution.",
                        "Creating One Pagers for Leadership on future roadmap insights."
                    ]
                },
                {
                    "Name": "Cush (Community Unified Social Hub) 🧑‍🤝‍🧑",
                    "DescriptionPoints": [
                        "Serving as Tech BA for creating Adobe's social media platform.",
                        "Engaging with stakeholders, capturing features, and driving development.",
                        "Providing break-fix coding to ensure web application uptime."
                    ]
                },
                {
                    "Name": "RSM (Retail Subscription Management) 💰",
                    "DescriptionPoints": [
                        "Automating SQL processes to ensure data ingestion from various source systems.",
                        "Providing Root Cause Analysis for discrepancies in Data Flows.",
                        "Creating revenue-affecting reports for subscription fulfilment, payment realization, detailed trend analysis, insights generation, and setting up monitors for error detection."
                    ]
                }
            ]
        }

    ],
    "References": "Available on Request"
}

st.set_page_config(page_title=f"{resume_data['Contact']['Name']} - Executive Resume", page_icon="📄")

st.title(f"{resume_data['Contact']['Name']} - Executive Resume")

# --- Sidebar Navigation Buttons ---
st.sidebar.header("Navigation")
# Reordered sections with icons
sections = ["Contact 📞", "Summary 🚀", "Skills 🤹", "Experience 💼", "Certifications 🏆", "Projects 💡", "Ask Binay 🤖", "References 🤝", "Feedback 📝", "Download PDF ⬇️"] # Added Feedback
section_icons = {"Contact 📞": "📞", "Summary 🚀": "🚀", "Skills 🤹": "🤹", "Experience 💼": "💼", "Certifications 🏆": "🏆", "Projects 💡": "💡", "Ask Binay 🤖": "🤖", "References 🤝": "🤝", "Download PDF ⬇️": "⬇️", "Feedback 📝": "📝"}

# Initialize selected section using session state
if 'selected_section' not in st.session_state:
    st.session_state['selected_section'] = "Contact 📞"

def update_selected_section(section):
    st.session_state['selected_section'] = section

for section_name in sections:
    # Use different styling for the selected button
    if st.session_state['selected_section'] == section_name:
        button_style = """
            background-color: #d0e1f9 !important;
            color: #2d545e !important;
            font-weight: bold !important;
        """
    else:
        button_style = ""

    st.sidebar.button(section_name, key=f"nav_button_{section_name}", on_click=update_selected_section, args=(section_name,))

# --- Main Content Area ---

# Access selected_section from session_state
selected_section = st.session_state['selected_section']

if selected_section == "Contact 📞":
    st.header(f"Contact Information {section_icons['Contact 📞']}")
    col1, col2 = st.columns([1, 3]) # Adjust column ratio as needed

    with col1:
        try:
            profile_image = Image.open("profile_photo.jpg")  # 📸 Replace "profile_photo.png" with your image file in the same directory
            st.image(profile_image, width=150) # Adjust width as needed
        except FileNotFoundError:
            st.warning("Profile photo not found. Please add 'profile_photo.png' to the directory.")

    with col2:
        st.write(f"**Name:** {resume_data['Contact']['Name']}")
        st.write(f"**Email:** {resume_data['Contact']['Email']}")
        st.write(f"**Phone:** {resume_data['Contact']['Phone']}")
        st.write(f"**Location:** {resume_data['Contact']['Location']}")
        st.write(f"**LinkedIn:** [{resume_data['Contact']['LinkedIn']}]({resume_data['Contact']['LinkedIn']})")
        st.write(f"**GitHub:** [{resume_data['Contact']['GitHub']}]({resume_data['Contact']['GitHub']})")
        st.info("Connect with me to discuss data-driven leadership and analytics strategies.")

elif selected_section == "Summary 🚀":
    st.header(f"Executive Summary {section_icons['Summary 🚀']}")
    st.write(resume_data['Summary'].strip())

    # --- Leadership Strengths Highlight ---
    st.subheader("Key Leadership Competencies ✨")
    lcol1, lcol2, lcol3 = st.columns(3)
    with lcol1:
        st.metric("Stakeholder Manag.", f"{skill_scores['Leadership & Strategy 🧭']['Stakeholder Management']}/5", "Expert: Building consensus and trust") # Added description
    with lcol2:
        st.metric("Strategic Thinking", f"{skill_scores['Leadership & Strategy 🧭']['Strategic Thinking']}/5", "Visionary: Charting data-driven roadmaps") # Added description
    with lcol3:
        st.metric("Team Building", f"{skill_scores['Leadership & Strategy 🧭']['Building Teams']}/5", "Empowering: Fostering collaboration and growth") # Added description

    lcol4, lcol5 = st.columns(2)
    with lcol4:
        st.metric("Long-Term Vision", f"{skill_scores['Leadership & Strategy 🧭']['Long-Term Vision Alignment']}/5", "Forward-Thinking: Aligning with strategic objectives") # Added description
    with lcol5:
        st.metric("Risk & Control", f"{skill_scores['Leadership & Strategy 🧭']['Risk & Control Management']}/5", "Pragmatic: Balancing innovation with governance") # Added description

elif selected_section == "Skills 🤹":
    st.header(f"Skills & Expertise {section_icons['Skills 🤹']}")
    st.write(", ".join(resume_data['Skills']))

    # --- Icon-Based Skill Chart ---
    st.subheader("Skills Proficiency Showcase")
    st.write("*(Proficiency levels indicated by filled icons)*")

    for category_name in skill_categories_order:
        st.subheader(category_name)
        skills_in_category = skill_scores[category_name]
        for skill_name, score in skills_in_category.items():
            skill_col, score_col = st.columns([3, 2])
            with skill_col:
                st.markdown(f"**{skill_name}**")
            with score_col:
                # Fix TypeError: can't multiply sequence by non-int of type 'float'
                full_icons = "🟢" * int(skill_scores[category_name][skill_name])  # Convert score to integer before multiplication
                empty_icons = "⚪" * (5 - int(skill_scores[category_name][skill_name])) # Convert 5-score to int
                st.markdown(f"{full_icons}{empty_icons}")

elif selected_section == "Certifications 🏆":
    st.header(f"Certifications {section_icons['Certifications 🏆']}")
    for certification in resume_data['Certifications']:
        st.markdown(f"- ✨ {certification}")

elif selected_section == "Experience 💼":
    st.header(f"Professional Journey {section_icons['Experience 💼']}")
    st.subheader("Career Progression: Ladders of Success")

    for job in resume_data['Experience']:
        with st.container():
            st.markdown("---")
            st.subheader(f"**{job['Title']}**")
            st.markdown(f"*{job['Company']}* ({job['Dates']}) - {job['Location']}")

            with st.expander("More Details", expanded=False):
                job_col1, job_col2 = st.columns(2)
                with job_col1:
                    st.markdown("**Role Summary:**")
                    st.write(job['Description'].strip())
                with job_col2:
                    st.markdown("**Key Learnings & Contributions:**")
                    for learning_point in job['Learnings']:
                        st.markdown(f"- ✨ {learning_point}")

elif selected_section == "Projects 💡":
    st.header(f"Impactful Projects {section_icons['Projects 💡']}")
    for project_section in resume_data['Projects']:
        st.subheader(project_section["Section"])
        for project in project_section["Projects"]:
             with st.expander(f"**{project['Name']}**"):
                st.subheader(project['Name'])
                if "Description" in project:
                    st.write(project["Description"].strip())
                if "DescriptionPoints" in project:
                    for point in project["DescriptionPoints"]:
                        st.markdown(f"- ✨ {point.strip()}")

elif selected_section == "References 🤝":
    st.header(f"Testimonials {section_icons['References 🤝']}")
    st.write(resume_data['References'])

elif selected_section == "Ask Binay 🤖":
    st.header(f"Ask Binay (AI Chat) {section_icons['Ask Binay 🤖']}")
    st.write("Ask me anything about my resume, skills, and experience!")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I'm Binay's AI assistant. How can I help you?"}]

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    if prompt := st.chat_input("Ask me anything"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # --- OpenAI Integration ---
        # 1. Prepare Resume Text for Context
        resume_text_for_context = f"""
        Contact Information:
        Name: {resume_data['Contact']['Name']}
        Email: {resume_data['Contact']['Email']}
        Phone: {resume_data['Contact']['Phone']}
        LinkedIn: {resume_data['Contact']['LinkedIn']}
        GitHub: {resume_data['Contact']['GitHub']}
        Location: {resume_data['Contact']['Location']}

        Summary:
        {resume_data['Summary']}

        Skills:
        {', '.join(resume_data['Skills'])}

        Certifications:
        {', '.join(resume_data['Certifications'])}

        Experience:
        """
        for job in resume_data['Experience']:
            resume_text_for_context += f"""
            Title: {job['Title']}
            Company: {job['Company']}
            Dates: {job['Dates']}
            Location: {job['Location']}
            Description: {job['Description']}
            Learnings: {', '.join(job['Learnings'])}
            """

        resume_text_for_context += """
        Projects:
        """
        for project_section in resume_data['Projects']:
            resume_text_for_context += f"""
            Section: {project_section['Section']}
            """
            for project in project_section['Projects']:
                resume_text_for_context += f"""
                Name: {project['Name']}
                Description: {project.get('Description', '')}
                Description Points: {', '.join(project.get('DescriptionPoints', []))}
                """
        resume_text_for_context += f"""
        References: {resume_data['References']}
        LinkedIn Profile: {resume_data['Contact']['LinkedIn']}
        GitHub Profile: {resume_data['Contact']['GitHub']}
        """

        # 2. Call OpenAI API (Make sure you have set your OPENAI_API_KEY as environment variable)
        openai.api_key =  st.secrets["OPENAI_API_KEY"] 

        if not openai.api_key:
            st.error("OpenAI API key is missing. Please set it as an environment variable `OPENAI_API_KEY`.")
        else:
            try:
                # Enhanced Prompt - Be specific about persona and context
                enhanced_prompt = f"""
                You are Binay Siddharth's AI assistant, designed to answer questions based on his resume, LinkedIn, and GitHub profiles.
                Use the following resume information to answer the question. If the question is outside the scope of the resume, politely say you can only answer questions based on the provided resume, LinkedIn profile ({resume_data['Contact']['LinkedIn']}), and GitHub profile ({resume_data['Contact']['GitHub']}).

                Resume Information:
                ```
                {resume_text_for_context}
                ```

                Now, answer the following question from the user:
                User Question: {prompt}
                """

                response = openai.chat.completions.create( # Updated to openai.chat.completions.create
                    model="gpt-4-1106-preview", # or "gpt-3.5-turbo-1106" or another suitable model
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant specialized in answering questions about a resume."},
                        {"role": "user", "content": enhanced_prompt}
                    ],
                    temperature=0.5, # Adjust for creativity vs. accuracy
                )

                ai_response_content = response.choices[0].message.content

                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response_content})
                # Display AI response
                with st.chat_message("assistant"):
                    st.markdown(ai_response_content)

            except openai.OpenAIError as e: # Using the corrected error class
                st.error(f"Error communicating with OpenAI: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


elif selected_section == "Feedback 📝":
    st.header(f"Feedback {section_icons['Feedback 📝']}")
    st.write("I value your feedback! Please share your thoughts on this interactive resume:")

    with st.form("feedback_form"):
        name = st.text_input("Your Name (Optional)")
        email = st.text_input("Your Email (Optional)")
        comments = st.text_area("Comments", help="Please provide any feedback or suggestions.")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            # In a real application, you would save this feedback to a database or file.
            st.success("Thank you for your feedback!")
            st.balloons() # Easter Egg - Balloons on feedback submission!

elif selected_section == "Download PDF ⬇️":
    st.header(f"Download PDF Resume {section_icons['Download PDF ⬇️']}")
    st.write("Click the button below to download the PDF version of my resume.")
    pdf_path = "your_resume.pdf"
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="Download PDF Resume",
                data=pdf_bytes,
                file_name="Binay_Siddharth_Executive_Resume.pdf",
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error(f"PDF file not found at: {pdf_path}. Please ensure 'your_resume.pdf' is in the correct location.")


# --- Styling --- (Executive Theme - HCI Refined)
st.markdown(f"""
<style>
.streamlit-expanderHeader {{
    font-weight: bold;
    font-size: 1.15em;
    border-bottom: 2px solid #e0e0e0;
    margin-bottom: 0.6em;
    padding-bottom: 0.3em;
    color: #444;
}}
h1.streamlit-header, h2.streamlit-header, h3.streamlit-header, h4.streamlit-header, h5.streamlit-header, h6.streamlit-header {{
    color: #3a4750;
}}
.stButton > button {{
    background-color: #f9fafa;
    color: #4a5568;
    border: 1px solid #f0f0f0;
    border-radius: 5px;
    padding: 0.45em 0.9em;
    margin-bottom: 0.25em;
    width: 100%;
    font-weight: 400;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}}
.stButton > button:hover {{
    background-color: #f0f2f5;
    color: #4a5568;
}}
div.stButton > button:focus:not(:active) {{
    border-color: transparent;
    box-shadow: none;
}}
.metric-container {{
    border: none;
    padding: 0.5em 0;
    border-radius: 0;
    text-align: center;
    box-shadow: none;
    background-color: transparent;
}}
.metric-value {{
    font-size: 1.4em !important;
    color: #3490dc !important;
}}
.metric-label {{
    font-size: 0.85em !important;
    color: #6a7180 !important;
}}
.metric-delta {{
    font-size: 1em !important;
    color: #7a8190 !important;
}}
/* Ladders of Success Styling */
.st-container > section > div.st-container > div > div:nth-child(6) > div > div > div > div {{
    border-left: 3px solid #ddd;
    padding-left: 1.5em;
    margin-left: 0.5em;
}}
.st-container > section > div.st-container > div > div:nth-child(6) > div > div > div > div:last-child {{
    border-left: none;
}}
/* Highlight selected tab */
[data-baseweb="tab-list"] > div[role="tab"][aria-selected="true"] {{
  background-color: #d0e1f9;
  color: #2d545e;
  font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Interactive Resume by Binay Siddharth 🚀")