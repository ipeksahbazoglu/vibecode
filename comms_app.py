import streamlit as st
from textblob import TextBlob
import string
import random

from inclusivity_score import calculate_inclusivity_score

# Define keyword dictionary
keyword_dict = {
    "Engineering": ["deployment", "architecture", "optimization", "automation", "code", "build", "test", "pipeline", "security", "API"],
    "Finance": ["budget", "forecast", "expense", "revenue", "invoice", "payment", "financial", "report", "audit", "investment"],
    "Commercial": ["sales", "campaign", "market", "conversion", "client", "lead", "promotion", "deal", "growth", "CRM"],
    "Design": ["UX", "UI", "wireframe", "prototype", "aesthetic", "interface", "branding", "layout", "graphic", "logo"],
    "Manufacturing": ["assembly", "production", "machine", "process", "plant", "schedule", "output", "tooling", "maintenance", "repair"],
    "HR": ["recruitment", "onboarding", "employee", "benefits", "policy", "training", "engagement", "feedback", "leave", "performance"],
    "Jaguar": ["luxury", "performance", "sleek", "sedan", "electric", "dynamic", "elegant", "refined", "drive", "technology"],
    "Range Rover": ["SUV", "terrain", "comfort", "leather", "ride", "off-road", "versatile", "premium", "luxury", "adaptive"],
    "Defender": ["rugged", "adventure", "durable", "explore", "4x4", "trail", "performance", "freedom", "engine", "resilient"],
    "Discovery": ["family", "journey", "versatile", "space", "comfort", "drive", "technology", "entertainment", "seating", "luxury"]
}

internal_demo_texts = [
    "The Engineering team completed deployment and optimization of our CI/CD pipelines with improved automation that ensures fewer bugs and smoother releases.",
    "Finance completed the quarterly report with projections, budget revisions, and updated expense statements reviewed by the CFO.",
    "The Commercial team exceeded their sales quota and saw an increase in CRM-driven conversion and client engagement through personalized outreach.",
    "Design finalized the UI for the mobile app with feedback applied from user testing, improving overall user experience and interaction flow.",
    "Manufacturing optimized their assembly line processes by reducing downtime and increasing cycle throughput by 12%.",
    "HR launched new employee training modules focused on DEI, engagement, and flexible working policies. Feedback so far has been very positive.",
    "Engineering initiated a refactor of the monolithic architecture to enhance modularity, but the deployment cadence remains suboptimal due to unresolved merge conflicts.",
    "Finance stakeholders were looped in post-facto on fiscal reallocations, leading to misalignment in Q3 projections and downstream reporting inconsistencies.",
    "Commercial's outreach lacked segmentation strategy, resulting in diluted messaging and subpar conversion metrics across verticals.",
    "Design iterations were delayed due to asynchronous feedback loops and insufficient alignment on visual hierarchy principles.",
    "Manufacturing encountered throughput bottlenecks attributed to legacy tooling and non-standardized SOP adherence.",
    "HR's onboarding documentation is fragmented and lacks clarity, making it difficult for new hires to navigate benefits and compliance requirements."
]

external_demo_texts = [
    "Jaguar’s new electric sedan combines luxury and performance with a sleek design and intuitive technology for a refined driving experience.",
    "Range Rover redefines comfort and capability with a premium SUV built for both city streets and rugged terrain.",
    "The Defender is engineered for adventure — durable, reliable, and ready for any terrain with advanced off-road features.",
    "Discovery offers a spacious, family-friendly SUV with smart storage, adaptive technology, and a smooth, comfortable ride.",
    "Explore the future of luxury with Jaguar Land Rover’s all-electric lineup — designed for performance, sustainability, and style.",
    "Our latest Range Rover model features a panoramic roof, adaptive suspension, and a quiet cabin for an elevated driving experience.",
    "Jaguar’s modular EV platform leverages torque vectoring and dynamic load balancing to optimize performance across drive modes.",
    "Range Rover’s latest iteration integrates a multi-modal infotainment stack with AI-assisted terrain calibration — redefining SUV intelligence.",
    "Defender’s ruggedized chassis and torque-mapped drivetrain ensure resilience under extreme duress, ideal for expedition-grade mobility.",
    "Discovery’s infotainment UX has been rearchitected to support multi-zone climate logic and rear-seat entertainment concurrency.",
    "Our electric lineup utilizes a proprietary e-architecture with over-the-air firmware orchestration and predictive diagnostics.",
    "The new Range Rover integrates a V2X-ready telematics suite with adaptive ride profiling and biometric cabin personalization."
]

# Streamlit UI
st.set_page_config(page_title="Communications Assistant", layout="centered")
st.title("🧠 Communications Assistant")
st.markdown("Analyze communication impact across departments and brands using AI-powered sentiment, engagement, and inclusivity scoring.")


option = st.radio("Select Communication Mode", ("Internal", "External"))
departments = ["Engineering", "Finance", "Commercial", "Design", "Manufacturing", "HR", "All"]
brands = ["Jaguar", "Range Rover", "Defender", "Discovery", "All"]
selected_dept = st.selectbox("Select Department (Internal)", departments) if option == "Internal" else None
selected_brand = st.selectbox("Select Brand (External)", brands) if option == "External" else None

if st.button("Generate Sample Message"):
    st.session_state['input_text'] = random.choice(internal_demo_texts if option == "Internal" else external_demo_texts)

input_text = st.text_area("Enter a message or social media post:", height=200, key='input_text')

def count_keyword_hits(text, keyword_list):
    return sum(1 for kw in keyword_list if kw.lower() in text.lower())


def calculate_score(base, keyword_hits):
    bonus = min(keyword_hits * 2, 20)
    return round(min(100, base * 100 + bonus))

def generate_scores(targets):
    results = {}
    blob = TextBlob(input_text)
    base_sentiment = blob.sentiment.polarity
    for target in targets:
        keyword_hits = count_keyword_hits(input_text, keyword_dict.get(target, []))
        sentiment_score = sentiment_score = round((base_sentiment + 1) * 50)
        engagement_score = min(100, keyword_hits * 5)
        inclusivity_score = calculate_inclusivity_score(input_text)
        results[target] = {
            "Sentiment": sentiment_score,
            "Engagement": engagement_score,
            "Inclusivity": inclusivity_score
        }
    return results

if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please enter a message to analyze.")
    else:
        if (selected_dept == "All" and option == "Internal") or (selected_brand == "All" and option == "External"):
            targets = departments[:-1] if option == "Internal" else brands[:-1]
            scores = generate_scores(targets)
            st.subheader("Individual Scores:")
            for target, score in scores.items():
                st.markdown(f"**{target}** — Sentiment: `{score['Sentiment']}/100`, Engagement: `{score['Engagement']}/100`, Inclusivity: `{score['Inclusivity']}/25`")
        else:
            target = selected_dept if option == "Internal" else selected_brand
            score = generate_scores([target])[target]
            st.subheader(f"Scores for {target}:")
            st.markdown(f"**Sentiment Score:** `{score['Sentiment']}/100`")
            st.markdown(f"**Engagement Score:** `{score['Engagement']}/100`")
            st.markdown(f"**Inclusivity Score:** `{score['Inclusivity']}/25`")
        
        with st.expander("What do the scores mean?"):
            st.markdown("""
        **Sentiment Score (/100)**  
        - Measures emotional tone (negative to positive).  
        - 0–40: Negative | 41–60: Neutral | 61–100: Positive

        **Engagement Score (/100)**  
        - Measures keyword alignment and relevance.  
        - 0–40: Low | 41–70: Moderate | 71–100: High

        **Inclusivity Score (/25)**  
        - Measures readability and accessibility.  
        - 0–7: Low | 8–14: Moderate | 15–25: High
        """)
