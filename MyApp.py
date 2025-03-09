import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
import re  # For robust date parsing
from PIL import Image, ImageDraw  # For profile picture and circular crop
import openai
import os  # For OpenAI API Key
from datetime import datetime
import csv  # For chat logging

# --- Skill Scores Data ---
skill_scores = {
    "Leadership & Strategy": {
        "Stakeholder Management": (4.5, "Extensive experience collaborating with finance leaders and executive teams.",
                                  [
                                      {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": None}
                                  ]),
        "Strategic Thinking": (5, "Demonstrated in developing strategic initiatives and leading complex projects.",
                              [
                                  {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "ELT Scorecard"},
                                  {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions"}
                              ]),
        "Team Building": (5, "Led and mentored high-performing teams across multiple organizations.",
                         [
                             {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "BI Reporting Hub"},
                             {"job": "Manager, BI Reporting", "company": "IB&M Finance", "project": None},
                             {"job": "Production Support Analyst", "company": "Adobe Systems Inc.", "project": None}
                         ]),
        "Vision Alignment": (4.5, "Experience aligning project goals with broader organizational objectives.",
                            [
                                {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Reporting hub for Executive Leadership"},
                                {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                            ]),
        "Risk Management": (4, "Involved in risk analysis and mitigation strategies during product launches.",
                           [
                               {"job": "Production Support Analyst", "company": "Adobe Systems Inc.", "project": "RSM (Retail Subscription Management)"}
                           ])
    },
    "Generative AI & Emerging Tech": {
        "AWS Services (Textract, Lambda)": (4, "Hands-on experience with AWS Textract and Lambda for GenAI solutions.",
                                            [
                                                {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions - Receipt Processing"}
                                            ]),
        "NLP & SQL": (4, "Developed NLP-driven solutions for natural language to SQL conversion.",
                      [
                          {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions - NLP to SQL"}
                      ]),
        "RAG & Vector Stores": (4, "Exploration and implementation of RAG and vector DBs for enhanced GenAI.",
                               [
                                   {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions - RAG & Vector Stores"}
                               ]),
        "LangChain": (4, "Utilized LangChain framework for building GenAI applications.",
                      [
                          {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions - LangChain Applications"}
                      ]),
        "Agentic AI": (4, "Designed and implemented agentic AI systems for intelligent task routing.",
                       [
                           {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions - Master Agentic Bot"}
                       ])
    },
    "Data Engineering": {
        "Data Pipelines": (5, "Expertise in building robust and scalable data pipelines.",
                          [
                              {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Reporting hub for Executive Leadership"},
                              {"job": "Data Engineering Intern", "company": "BizCubed Pty Ltd", "project": "National Sales Report | Yahoo7"}
                          ]),
        "Data Modelling": (5, "Extensive experience in data modeling (dimensional and relational).",
                          [
                              {"job": "Manager, BI Reporting", "company": "IB&M Finance", "project": "Project Spur"},
                              {"job": "Data Engineering Intern", "company": "BizCubed Pty Ltd", "project": "Performance Monitoring Report | Managed Services"}
                          ]),
        "SQL": (5, "Highly proficient in SQL for data manipulation, analysis, and automation.",
                [
                    {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Process Efficiency and Data Lineage for Capital Engine"},
                    {"job": "Production Support Analyst", "company": "Adobe Systems Inc.", "project": "RSM (Retail Subscription Management)"}
                ]),
        "Python": (4, "Proficient in Python for data engineering and application development.",
                   [
                       {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions"},
                       {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                   ]),
        "Cloud (AWS/Snowflake)": (4, "Experience with AWS and Snowflake for data warehousing/analytics.",
                                 [
                                     {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Generative AI & AWS-Powered Solutions"},
                                     {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "ELT Scorecard"}
                                 ]),
        "APIs": (4, "Utilized APIs for data integration and extraction.",
                 [
                     {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"},
                     {"job": "Analyst, Gems Operations", "company": "GCARD", "project": "Loan IQ Data Feed Ingestion"}
                 ])
    },
    "BI & Analytics": {
        "BI Product Dev": (5, "Led development of BI products from concept to delivery.",
                           [
                               {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Reporting hub for Executive Leadership"},
                               {"job": "Manager, BI Reporting", "company": "IB&M Finance", "project": "Project Spur"},
                               {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                           ]),
        "Data Storytelling": (5, "Exceptional ability to communicate insights through narratives/visualizations.",
                             [
                                 {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "ELT Scorecard"},
                                 {"job": None, "company": None, "project": "Uber Analytics Dashboard"},
                                 {"job": None, "company": None, "project": "Airbnb Tableau Community Project"}
                             ]),
        "Tableau": (5, "Extensive expertise in Tableau for interactive dashboards.",
                    [
                        {"job": "Senior Manager, Group BI Reporting", "company": "Commonwealth Bank of Australia", "project": "Reporting hub for Executive Leadership"},
                        {"job": "Manager, BI Reporting", "company": "IB&M Finance", "project": "Project Spur"},
                        {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                    ]),
        "Alteryx/Power BI": (4, "Proficient in Alteryx for data prep and Power BI for reporting.",
                           [
                               {"job": "Analyst, Gems Operations", "company": "GCARD", "project": "Loan IQ Data Feed Ingestion"},
                               {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                           ]),
    },
    "Process & Delivery": {
        "Agile/Iterative": (4, "Experienced in Agile and iterative development.",
                           [
                               {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"},
                               {"job": "Production Support Analyst", "company": "Adobe Systems Inc.", "project": "Cush (Community Unified Social Hub)"}
                           ]),
        "Human-Centered Design": (5, "Focus on user-centered design for effective solutions.",
                               [
                                   {"job": "Production Support Analyst", "company": "Adobe Systems Inc.", "project": "User Analytics and Journey Optimization"},
                                   {"job": "Analyst, BI and Analytics", "company": "The University of Sydney", "project": "Canvas Reporting and Student Engagement dashboards"}
                               ])
    }
}


# --- Resume Data ---
resume_data = {
    "Contact": {
        "Name": "Binay Siddharth",
        "Email": "binay.siddharth@gmail.com",
        "Phone": "+61 451 943 584",
        "LinkedIn": "www.linkedin.com/in/binaysiddharth",
        "GitHub": "github.com/binzidd",
        "Location": "Sydney, AU"
    },
    "Overview": {
        "Summary": """
        Results-driven Senior Manager with 7 years of progressive experience at Commonwealth Bank of Australia, specializing in transforming financial services through data. A proven leader in building high-performing teams, I excel at turning complex data into actionable insights and strategic solutions.  From developing executive-level reporting hubs to pioneering Generative AI applications, I'm passionate about leveraging cutting-edge technology to optimize business performance and drive innovation. My expertise spans the full data lifecycle, from data engineering and modeling to impactful BI and advanced analytics.  I thrive in collaborative environments, working closely with stakeholders to deliver solutions that make a tangible difference.
        """,
        "FeaturedWork": [
            {
                "name": "Uber Analytics",
                "url": "https://public.tableau.com/app/profile/binay5660/viz/MyUberAnalytics/MyUberJourney",
                "description": "Advanced Analytics Dashboard"
            },
            {
                "name": "Airbnb Tableau Community",
                "url": "https://public.tableau.com/app/profile/binay5660/viz/HeyAirbnbWhataremychoicesinSydney/AirbnbDashboard",
                "description": "Tableau Community Project"
            }
        ]
    },
   "Experience": [
        {
            "Title": "Senior Manager, Group BI Reporting (Insights and Data)",
            "Company": "Commonwealth Bank of Australia",
            "Dates": "2022 - Current",
            "Location": "Sydney, AU",
            "Description": """
            Collaborating with finance leaders on strategic data-driven decisions. Led high-performing BI Reporting Hub.
            Managed data assets for Executive Leadership, driving decision-making through interactive KPI reports.
            Championed BI innovation and upskilling. Leading GenAI solutions for business optimization.
            """,
            "Projects": [
                {
                    "Name": "Reporting hub for Executive Leadership, strategic measures | Data Lake and Reporting 📊",
                    "Description": "Uplifting manual processes with auto-ingest feeds and Tableau. 70% time saved and modern BI tools used for executive engagement."
                },
                {
                    "Name": "Process Efficiency and Data Lineage for Capital Engine ⚙️",
                    "Description": "Reduced Capital Production Month End lifecycle from 4 WD to 1.5 WD. Achieved 85% faster process and increased Data Visibility."
                },
                {
                    "Name": "ELT Scorecard | Strategic Metrics | Data Lake and Visualization Layer ☁️",
                    "DescriptionPoints": [
                        "Created conceptual data lake infrastructure and Extract Load Transform architecture.",
                        "Developed Tableau dashboards with drill-through to financial P&L.",
                        "Integrated data with robust lineage tracking."
                    ]
                },
                {
                    "Name": "Generative AI & AWS-Powered Business Solutions (Proof of Concept & Experimentation) 🤖",
                    "Dates": "2024-10 - Present",
                    "DescriptionPoints": [
                        "**Intelligent Receipt Processing with AWS Textract:** Led PoC to production using Textract and Lambda. Explored GenAI (RAG, vector stores, intent-based routing).",
                        "**Natural Language to SQL with AWS and LangChain:** System for accountants to query databases using natural language, leveraging NLP, LangChain, and GenAI.",
                        "**Master Agentic Bot for Intelligent Task Routing:** Designed a 'master bot' using classification to understand user intent and direct requests.",
                        "**Key Technologies:** Python, LangChain, AWS (Textract, Lambda, S3, RDS, etc.), GenAI, RAG, Vector Databases."
                    ]
                }
            ]
        },
        {
            "Title": "Manager, BI Reporting",
            "Company": "IB&M Finance",
            "Dates": "2020 - 2022",
            "Location": "Sydney, AU",
            "Description": "Managed BI Reporting Projects, delivering data based solutions for financial insights.",
            "Projects": [
                {
                    "Name": "Project Spur | Data Transformation and Reporting 🔄",
                    "DescriptionPoints": [
                        "Ingested and modelled data from various source systems (Risk, Finance, Treasury, Capital).",
                        "Separated visualization/data layers, enabling dynamic refreshes and eliminating manual processes.",
                        "Achieved process efficiency."
                    ]
                }
            ]
        },
        {
            "Title": "Senior Analyst, Capital Tech",
            "Company": "GCARD",
            "Dates": "2019 - 2020",
            "Location": "Sydney, AU",
            "Description": "Senior Analyst role focused on Capital Tech projects.",
            "Projects": [
                {
                    "Name": "Daily Capital Reporting",
                    "Description": "Developed/maintained daily capital reporting, ensuring timely/accurate metrics."
                }
            ]
        },
        {
            "Title": "Analyst, Gems Operations",
            "Company": "GCARD",
            "Dates": "2018 - 2019",
            "Location": "Sydney, AU",
            "Description": "Analyst role in Gems Operations.",
            "Projects": [
                {
                    "Name": "Loan IQ Data Feed Ingestion and Integration with Data Infrastructure 🔗",
                    "DescriptionPoints": [
                        "Captured document-based files and integrated with capital engine for RWA calculation.",
                        "Data Transformation/Processing in Alteryx with reconciliation.",
                        "Delivered reporting layer on monthly portfolio movement."
                    ]
                }
            ]
        },
       {
            "Title": "Analyst, University of Sydney Roles",
            "Company": "The University of Sydney",
            "Dates": "2017 - 2018",
            "Location": "Sydney, AU",
            "Description": "Held multiple roles focused on BI, analytics, and business analysis.",
            "Roles": [
                {
                    "SubTitle": "Analyst, BI and Analytics (Design and Reporting)",
                    "SubDates": "2017 - 2018",
                    "SubDescription": """Implemented agile analytics using Tableau and Alteryx. Data mining, cleansing, and transformation. Collaborated with product owners.""",
                     "Projects": [
                        {
                            "Name": "Canvas Reporting and Student Engagement dashboards 📈",
                            "DescriptionPoints": [
                                "Designed dashboards for Unit of Study co-ordinators to check engagement.",
                                "Extracted data from S3, APIs, data modeling, presentation layer.",
                                "Implemented RLS."
                            ]
                        },
                        {
                            "Name": "HDR Students Predictive model for Course Completion 🎯",
                            "DescriptionPoints": [
                                "Reporting on predictive model.",
                                "Call to action dashboards for DVC Grants."
                            ]
                        },
                        {
                            "Name": "Student Performance Forecasting and Classification 🤖", #New Project Added Here
                            "DescriptionPoints": [
                                "Developed forecasting models for student performance using ARIMA in Alteryx.",
                                "Implemented classification models using Random Forest for predicting student outcomes.",
                                "Utilized machine learning techniques to enhance predictive accuracy."
                            ]
                        }
                    ]
                },
                {
                    "SubTitle": "BI Dev, HDR Reporting",
                    "SubDates": "2018",
                    "SubDescription": "BI Development for HDR Reporting.",
                    "SubCompany": "IAP"
                },
                {
                    "SubTitle": "Business Analyst, Canvas",
                    "SubDates": "2017",
                    "SubDescription": "Business Analyst role for Canvas project.",
                    "SubCompany" : "IAP"
                },
            ],
        },
       { #New Section for Public speaking
            "Title": "Tutoring Post Grads",
            "Company": "The University of Sydney",
            "Dates": "2019 - 2021",
            "Location": "Sydney, AU",
            "Description": "Tutoring and mentoring post-graduate students on BI tools and data analytics techniques within the Knowledge Management Systems course.",
           "Subject": "Knowledge Management Systems",
                    "SubjectDescription": """
                    This course provides a comprehensive introduction to Knowledge Management (KM) from both technological and organizational perspectives.  It covers a range of KM-related topics through published papers, case studies, and other publications.  Key areas include: KM Conceptual Foundations; Taxonomies of organizational knowledge and KM mechanisms; Case/Field Studies of KM Initiatives; Data Warehousing and OLAP/Business Analytics; Data, text, and web mining; Social media, crowdsourcing, and KM; Big data and actionable knowledge.  The course includes detailed coverage of Business Intelligence Systems, with hands-on work using the BI (Online Analytical Processing - OLAP) tool, COGNOS.
                    """

        },
        {
            "Title": "Data Engineering Intern and Related Roles",
            "Company": "BizCubed Pty Ltd, Yahoo7, Internal Services",
            "Dates": "2016 - 2018",
            "Location": "Sydney, AU",
            "Description": "Various roles in data engineering, development, and performance monitoring.",
            "Roles": [
                {
                    "SubTitle": "Data Engineering Intern, Data and Platform Enablement",
                    "SubDates": "2016 - 2017",
                    "SubDescription": """Developed performance dashboards and pipelines. Designed "heartbeat" services and dimensional models.  Liaised between teams.""",
                    "SubCompany": "BizCubed Pty Ltd",
                     "Projects" : [
                        {
                            "Name": "National Sales Report | Yahoo7 📰",
                            "DescriptionPoints": [
                                "Created summary reports on social media interaction.",
                                "Developed KPI and OKR dashboards.",
                                "Ingested streaming and transactional data."
                            ]
                        },
                        {
                            "Name": "Performance Monitoring Report | Managed Services 📊",
                            "DescriptionPoints": [
                                "Generated daily reports on server health.",
                                "Provided commentary on downtime/resolution.",
                                "Created One Pagers for Leadership."
                            ]
                        }
                    ]
                },
                {
                    "SubTitle": "Developer, Chanel Data",
                    "SubDates": "2018",
                    "SubDescription": "Developer role for Chanel Data.",
                    "SubCompany": "Yahoo7",
                },
                {
                    "SubTitle": "Junior Developer, Managed Services",
                    "SubDates": "2018",
                    "SubDescription": "Junior Developer in Managed Services. Interned at BizCubed.",
                    "SubCompany": "Internal Services",
                },
            ],
        },
        {
            "Title": "Production Support Analyst and Related Roles",
            "Company": "Adobe Systems Inc.",
            "Dates": "2012 - 2015",
            "Location": "Mumbai, India",
            "Description": "Multiple roles in production support, business analysis, and web content.",
            "Roles": [
                {
                    "SubTitle": "Production Support Analyst, Subscription Services",
                    "SubDates": "2012 - 2015",
                    "SubDescription": """Managed cross-functional teams and scrum meetings. Metrics generation, reporting, and risk analysis.""",
                    "Projects": [
                        {
                            "Name": "Cush (Community Unified Social Hub) 🧑‍🤝‍🧑",
                            "DescriptionPoints": [
                                "Tech BA for Adobe's social media platform.",
                                "Engaged with stakeholders, captured features, drove development.",
                                "Provided break-fix coding."
                            ]
                        },
                        {
                            "Name": "RSM (Retail Subscription Management) 💰",
                            "DescriptionPoints": [
                                "Automated SQL processes for data ingestion.",
                                "Provided Root Cause Analysis for discrepancies.",
                                "Created revenue-affecting reports."
                            ]
                        },
                        {
                            "Name": "User Analytics and Journey Optimization",
                            "DescriptionPoints": [
                                "Conducted user analytics to understand behavior/pain points.",
                                "Developed strategies to optimize user journeys.",
                                "Utilized Adobe Experience Manager (AEM).",
                                "Collaborated with teams to improve engagement/conversion."
                            ]
                        }
                    ]
                },
                {
                    "SubTitle": "Business Analyst, CUSH",
                    "SubDates": "2014 - 2015",
                    "SubDescription": "Business Analyst role for CUSH project.",
                    "SubCompany": "Digital Engineering"
                },
                {
                    "SubTitle": "Analyst, Web Content",
                    "SubDates": "2013 - 2014",
                    "SubDescription": "Analyst role focused on Web Content.",
                    "SubCompany": "Digital Engineering"
                },
                {
                    "SubTitle": "Analyst, Subscription",
                    "SubDates": "2012 - 2013",
                    "SubDescription": "Analyst role in Subscription services.",
                    "SubCompany": "RSM"
                },
            ],
        },
    ],
    "Certifications": [
        "Tableau: Community Leader, Data Scientist, Data Steward, Executive Sponsor, Desktop Specialist",
        "Alteryx: Core & Advanced",
        "AWS: Analytics Service Overview, Certified Cloud Practitioner",
        "Snowflake Hands-on Essentials: Data Warehouse, Data Applications",
        "Tableau Certified Designer",
        "Alteryx 2020 Certified Specialist"
    ],
    "References": "Available on Request",
    "Areas_of_Improvement": ["Strategic Messaging - Enhancing the narrative around my strategic contributions.", "Technology (Continuous Learning) - Staying ahead of the curve in rapidly evolving technologies.", "Public Speaking - Refining presentation skills for larger audiences.", "Cross-functional Collaboration -  Deepening collaboration across diverse business units."]
}

# --- Global Section Icons ---
section_icons = {"Overview & Skills": "🚀", "Experience & Projects": "💼", "Ask Binay": "🤖", "Feedback": "📝", "Download PDF": "⬇️"}


# --- Streamlit App Functions ---

def configure_page():
    """Configures the Streamlit page settings."""
    st.set_page_config(page_title=f"{resume_data['Contact']['Name']} - Resume", page_icon="📄", layout="wide")

def create_sidebar():
    """Creates the sidebar content including contact information and navigation."""
    st.sidebar.header(f"{resume_data['Contact']['Name']}")

    # Profile Picture (in Sidebar) - No Oval
    try:
        profile_image = Image.open("profile_photo.JPG")
        st.sidebar.image(profile_image, width=150)
    except FileNotFoundError:
        st.sidebar.warning("Profile photo not found.")

    st.sidebar.write(f"**Email:** {resume_data['Contact']['Email']}")
    st.sidebar.write(f"**Phone:** {resume_data['Contact']['Phone']}")
    st.sidebar.write(f"**Location:** {resume_data['Contact']['Location']}")
    st.sidebar.write(f"**LinkedIn:** [{resume_data['Contact']['LinkedIn']}]({resume_data['Contact']['LinkedIn']})")
    st.sidebar.write(f"**GitHub:** [{resume_data['Contact']['GitHub']}]({resume_data['Contact']['GitHub']})")

    st.sidebar.markdown("---")
    sections = ["Ask Binay", "Overview & Skills", "Experience & Projects", "Feedback", "Download PDF"]


    if 'selected_section' not in st.session_state:
        st.session_state['selected_section'] = "Ask Binay" # Default to Ask Binay

    def update_selected_section(section):
        st.session_state['selected_section'] = section

    for section_name in sections:
        if st.session_state['selected_section'] == section_name:
            button_style = """
                background-color: #d0e1f9 !important;
                color: #2d545e !important;
                font-weight: bold !important;
            """
            st.sidebar.button(f"{section_name} {section_icons.get(section_name, '')}", key=f"nav_button_{section_name}", on_click=update_selected_section, args=(section_name,), ) # Removed css=button_style
        else:
            st.sidebar.button(f"{section_name} {section_icons.get(section_name, '')}", key=f"nav_button_{section_name}", on_click=update_selected_section, args=(section_name,), )# Removed css=button_style

    st.sidebar.markdown("---")
    # st.sidebar.info("Interactive Resume by Binay Siddharth 🚀") # Removed

def render_overview_and_skills_section():
    """Renders the 'Overview & Skills' section of the resume."""
    st.title(f"Overview & Skills {section_icons['Overview & Skills']}")

    st.header("Executive Summary")
    st.write(resume_data['Overview']['Summary'].strip())

    st.subheader("Featured Work")
    for work in resume_data['Overview']['FeaturedWork']:
        st.markdown(f"- **[{work['name']}]({work['url']})**: {work['description']}")

    st.subheader("Skills Proficiency Showcase")
    st.write("*(Click on a skill category, then a skill to see related experiences)*")

    if 'selected_skill_category' not in st.session_state:
        st.session_state['selected_skill_category'] = "Generative AI & Emerging Tech"  # Default
    if 'selected_skill' not in st.session_state:
        st.session_state['selected_skill'] = None

    skill_category_col, skill_detail_col, skill_experience_col = st.columns([0.30, 0.35, 0.35])

    with skill_category_col:
        st.markdown("**Skill Categories**")
        skill_categories_list = list(skill_scores.keys())
        for category_name in skill_categories_list:
            if st.button(category_name, key=f"category_button_{category_name}"):
                st.session_state['selected_skill_category'] = category_name
                st.session_state['selected_skill'] = None

    with skill_detail_col:
        selected_category = st.session_state['selected_skill_category']
        st.markdown(f"**Skills in {selected_category}**")
        if selected_category in skill_scores:
            for skill_name, (score, tooltip_text, _) in skill_scores[selected_category].items():
                skill_button_key = f"skill_button_{category_name}_{skill_name}"
                if st.button(f"{skill_name}", key=skill_button_key):
                    st.session_state['selected_skill'] = skill_name
                st.write(tooltip_text)
                full_icons = "🟢" * int(score)
                empty_icons = "⚪" * (5 - int(score))
                st.markdown(f"Proficiency: {full_icons}{empty_icons}")
                st.markdown("---")

        else:
            st.write("Select a category.")

    with skill_experience_col:
        selected_skill = st.session_state['selected_skill']
        st.markdown("**Experience Highlights**")
        if selected_skill:
            st.markdown(f"**{selected_skill} Skill:**")
            selected_category_skills = skill_scores.get(st.session_state['selected_skill_category'], {}) #Use session state to get category
            skill_data = selected_category_skills.get(selected_skill)

            if skill_data and len(skill_data) > 2:
                experience_links = skill_data[2]
                if experience_links:
                    for link in experience_links:
                        job_title = link.get("job", "Various Roles")
                        company = link.get("company", "Various Companies")
                        project_name = link.get("project", "General Experience")

                        st.markdown(f"- **{job_title}**, *{company}*")
                        if project_name:
                            st.markdown(f"  - Project: {project_name}")
                else:
                    st.write("No specific project highlights.")
            else:
                st.write("No experience data.")
        else:
            st.write("Click on a skill to view experience.")

    st.subheader("Certifications")
    for certification in resume_data['Certifications']:
        st.markdown(f"- ✨ {certification}")

    st.subheader("Areas of Improvement")
    for area in resume_data["Areas_of_Improvement"]:
        st.markdown(f"- {area}")


def render_experience_and_projects_section():
    """Renders the 'Experience & Projects' section of the resume with date filtering."""
    st.title(f"Experience & Projects {section_icons['Experience & Projects']}")

    st.subheader("Filter Experience by Date")

    all_years = set()
    for exp in resume_data["Experience"]:
        dates = exp["Dates"].replace("Current", str(datetime.now().year)).split(" - ")
        if len(dates) == 2:
            all_years.add(int(dates[0].split("-")[0]))
            all_years.add(int(dates[1].split("-")[0]))
        elif len(dates) == 1:
            all_years.add(int(dates[0].split("-")[0]))
        if "Projects" in exp:
            for project in exp["Projects"]:
                if "Dates" in project:
                    pdates = project["Dates"].replace("Present",str(datetime.now().year)).split(" - ")
                    if len(pdates) == 2:
                        all_years.add(int(pdates[0].split("-")[0]))
                        all_years.add(int(pdates[1].split("-")[0]))
                    elif len(pdates) ==1:
                        all_years.add(int(pdates[0].split("-")[0]))

    all_years = sorted(list(all_years))
    if len(all_years) == 0:
        all_years = [2010, datetime.now().year]
    min_year = min(all_years)
    max_year = max(all_years)

    start_year, end_year = st.slider("Select Date Range", min_year, max_year, (min_year, max_year))

    filtered_experience = []
    for job in resume_data['Experience']:
        dates = job["Dates"].replace("Current", str(datetime.now().year)).split(" - ")
        if len(dates) == 2:
            job_start_year, job_end_year = int(dates[0].split("-")[0]), int(dates[1].split("-")[0])
        elif len(dates) == 1:
            job_start_year = job_end_year = int(dates[0].split("-")[0])
        else:
            job_start_year = 0
            job_end_year = 99999

        if job_end_year >= start_year and job_start_year <= end_year:
            filtered_experience.append(job)

    for job in filtered_experience:
        with st.container():
            st.markdown("---")
            st.subheader(f"**{job['Title']}**")
            st.markdown(f"*{job['Company']}* ({job['Dates']}) - {job['Location']}")

            with st.expander("More Details", expanded=True):
                if "Roles" in job:
                    for role in job["Roles"]:
                        st.markdown(f"**{role['SubTitle']}** ({role.get('SubCompany', job['Company'])} - {role['SubDates']})")
                        st.write(role["SubDescription"].strip())
                        if 'Projects' in role:
                            st.markdown("**Key Projects:**")
                            for project in role['Projects']:
                                if "Description" in project:
                                    st.markdown(f"- **{project['Name']}**: {project['Description']}")
                                if "DescriptionPoints" in project:
                                    st.markdown(f"- **{project['Name']}**")
                                    for point in project['DescriptionPoints']:
                                        st.markdown(f"  - ✨ {point.strip()}")
                        if "Subject" in role:
                            st.markdown(f"**Subject: {role['Subject']}**")
                            st.write(role["SubjectDescription"].strip())

                else:
                    job_col1, job_col2 = st.columns(2)
                    with job_col1:
                        st.markdown("**Role Summary:**")
                        st.write(job['Description'].strip())
                    with job_col2:
                        if 'Projects' in job:
                            st.markdown("**Key Projects:**")
                            for project in job['Projects']:
                                display_project = True
                                if "Dates" in project:
                                    project_dates = project["Dates"].replace("Present", str(datetime.now().year)).split(" - ")
                                    if len(project_dates) == 2:
                                      proj_start, proj_end = int(project_dates[0].split("-")[0]), int(project_dates[1].split("-")[0])
                                    elif len(project_dates) == 1:
                                      proj_start = proj_end = int(project_dates[0].split("-")[0])
                                    else:
                                      proj_start, proj_end = 0, 9999

                                    if not (proj_end >= start_year and proj_start <= end_year):
                                        display_project = False

                                if display_project:
                                    if "Description" in project:
                                        st.markdown(f"- **{project['Name']}**: {project['Description']}")
                                    if "DescriptionPoints" in project:
                                        st.markdown(f"- **{project['Name']}**")
                                        for point in project['DescriptionPoints']:
                                            st.markdown(f"  - ✨ {point.strip()}")

def render_ask_binay_section():
    """Renders the 'Ask Binay' (AI Chat) section with OpenAI integration and humor."""
    if st.session_state['selected_section'] == "Ask Binay": #Correct condition
        st.header(f"Ask Binay (AI Chat) {section_icons['Ask Binay']}") #Correct icon key
        st.write("Ask me anything about my resume, skills, and experience!")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I'm Binay's AI assistant. How can I help you?"}]

        # Display chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Get user input
        if prompt := st.chat_input("Ask me about my resume, skills, and experience!"):
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
            {resume_data['Overview']['Summary']}


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
                """
                if "Projects" in job:
                    for project in job["Projects"]:
                        resume_text_for_context += f"""
                        Project Name: {project.get('Name', '')}
                        """
                        if "Description" in project:
                            resume_text_for_context += f""" Project Description: {project.get('Description', '')}
                            """
                        if "DescriptionPoints" in project:
                            resume_text_for_context += "Project Description Points:\n" + "\n".join([f"    - {point}" for point in project.get("DescriptionPoints", [])]) + "\n"
                if "Roles" in job:  # Include sub-roles and their projects
                    for role in job["Roles"]:
                        resume_text_for_context += f"""
                            Sub-Role Title: {role.get('SubTitle', '')}
                            Sub-Role Company: {role.get('SubCompany', job['Company'])}
                            Sub-Role Dates: {role.get('SubDates', '')}
                            Sub-Role Description: {role.get('SubDescription', '')}
                        """
                        if "Projects" in role:
                            for project in role["Projects"]:
                                resume_text_for_context += f"""
                                    Project Name: {project.get('Name', '')}
                                    """
                                if "Description" in project:
                                    resume_text_for_context += f"""  Project Description: {project.get('Description', '')}
                                    """
                                if "DescriptionPoints" in project:
                                    resume_text_for_context += "Project Description Points:\n" + "\n".join([f"        - {point}" for point in project.get("DescriptionPoints", [])]) + "\n"


            resume_text_for_context += f"""
            References: {resume_data['References']}
            LinkedIn Profile: {resume_data['Contact']['LinkedIn']}
            GitHub Profile: {resume_data['Contact']['GitHub']}
            """

            # 2. Call OpenAI API 
            openai.api_key =  st.secrets["OPENAI_API_KEY"]

            if not openai.api_key:
                st.error("OpenAI API key is missing") # Updated error message
            else:
                try:
                    # Enhanced Prompt - Be specific about persona and context
                    enhanced_prompt = f"""
                You are Binay Siddharth's AI assistant.  Your primary goal is to answer questions accurately and concisely based on his resume.  When answering, prioritize information found within the "Experience" section, paying close attention to the "Projects" subsections.

                Here's the user's question: {prompt}

                For this question, specifically focus on extracting information from {resume_text_for_context}, deciside if it is a technology or a finance question. Add a spin to the answer based on your deicision.

                ```

                Here is the format of the response, give a overview of how Binay has used this skill, list the project name first then provide a short description of the project with key words:

                Explain how Binay can be a value ad based on skills \n
                
                **Experience**: Role and Year \n
                **Project Name**: Project description (key technologies used).\n


                If the provided resume information doesn't contain details about AI-related projects, you can briefly mention the overall involvement in AI mentioned in the summary, and *then* suggest checking LinkedIn and GitHub.  But ONLY do this if the resume itself is insufficient. Do NOT mention LinkedIn or GitHub if the resume has the answer.
                """

                    # --- Humor Check ---
                    if "are you high" in prompt.lower():
                        ai_response_content = "As a humble AI, I operate on algorithms and electricity, not... other substances.  But I can generate some *high*-quality resume answers for you! 😉 What's your question?"
                    elif "should i hire Binay?" in prompt.lower():
                        ai_response_content = "Definitely hire Binay. Team builder? Hes excellent at building a team around the coffee machine. Path leader? Knows the path to the break room like the back of his hand. And practices what he preaches? He preaches delegate and practices it flawlessly."
                    else: # Proceed with OpenAI API call for other questions
                        response = openai.chat.completions.create( # Updated to openai.chat.completions.create
                            model="gpt-4-1106-preview", # or "gpt-3.5-turbo-1106" or another suitable model
                            messages=[
                                {"role": "system", "content": "You are a helpful AI assistant specialized in answering questions about a resume."},
                                {"role": "user", "content": enhanced_prompt}
                            ],
                            temperature=0.1, # Adjust for creativity vs. accuracy
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

def render_feedback_section():
    """Renders the 'Feedback' section for user feedback submission."""
    st.header(f"Feedback {section_icons['Feedback']}")
    st.write("Your feedback is valuable and helps me improve. Please share your thoughts on this resume!")

    feedback = st.text_area("Enter your feedback here:")
    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_feedback(feedback) # Use separate log_feedback function
        else:
            st.warning("Please enter your feedback before submitting.")

def render_download_pdf_section():
    st.write("Click the button below to download the PDF version of my resume.")
    pdf_path = "Binay_Resume.pdf"  # Make sure this path is CORRECT!
    try:
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download PDF Resume",
                data=file,
                file_name=pdf_path,
                mime="application/pdf"  # More general MIME type for PDFs
            )
    except FileNotFoundError:
        st.error(f"Error: PDF file not found at '{pdf_path}'. Please ensure 'my_resume.pdf' is in the same directory as your script, or update the path.")
    except Exception as e:
        st.error(f"An error occurred while trying to open or download the PDF: {e}")

    
def log_chat(user_message, ai_response):
    """Logs chat messages to a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("chat_log.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, user_message, ai_response])

def log_feedback(feedback_text):
    """Logs feedback messages to a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("feedback_log.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, feedback_text])


# --- Main App Function ---
def main():
    configure_page()
    create_sidebar()

    selected_section = st.session_state['selected_section']

    if selected_section == "Overview & Skills":
        render_overview_and_skills_section()
    elif selected_section == "Experience & Projects":
        render_experience_and_projects_section()
    elif selected_section == "Ask Binay":
        render_ask_binay_section()
    elif selected_section == "Feedback":
        render_feedback_section()
    elif selected_section == "Download PDF":
        render_download_pdf_section()


if __name__ == "__main__":
    main()
