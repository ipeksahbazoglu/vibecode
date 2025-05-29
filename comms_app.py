import streamlit as st
import numpy as np
from textblob import TextBlob
import random

st.set_page_config(page_title="Communications Assistant", layout="centered")

st.title("🧠 Communications Assistant")
st.markdown("Analyze communication impact across departments and brands using AI-powered sentiment and engagement scoring.")

option = st.radio("Select Communication Mode", ("Internal", "External"))

departments = ["Engineering", "Finance", "Commercial", "Design", "Manufacturing", "HR", "All"]
brands = ["Jaguar", "Range Rover", "Defender", "Discovery", "All"]

selected_dept = st.selectbox("Select Department (Internal)", departments) if option == "Internal" else None
selected_brand = st.selectbox("Select Brand (External)", brands) if option == "External" else None

keyword_dict = {
    "Engineering": ["deployment", "architecture", "optimization", "refactor", "scalability", "automation", "code", "build", "test", "version", "platform", "development", "QA", "integration", "pipeline", "repository", "security", "API", "framework", "debug", "release", "ticket", "agile", "scrum", "sprint", "backlog", "CI/CD", "performance", "bug", "issue", "devops", "frontend", "backend", "cloud", "server", "repository", "refactoring", "unit test", "load test", "hotfix", "merge", "pull request", "deployment", "infrastructure", "logging", "monitoring", "latency", "uptime", "failover", "incident"],
    "Finance": ["budget", "forecast", "expense", "revenue", "invoice", "payment", "financial", "report", "balance", "audit", "investment", "cost", "capital", "ROI", "profit", "loss", "P&L", "spreadsheet", "accounting", "analysis", "cash", "liquidity", "dividend", "compliance", "statement", "depreciation", "asset", "liability", "fiscal", "quarter", "tax", "VAT", "ledger", "CFO", "expenditure", "return", "earnings", "interest", "credit", "debit", "budgeting", "planning", "projection", "reconciliation", "variance", "policy", "allocation", "profitability", "fund", "equity"],
    "Commercial": ["sales", "campaign", "market", "conversion", "client", "lead", "target", "promotion", "deal", "pipeline", "retention", "growth", "CRM", "revenue", "negotiation", "closing", "customer", "product", "price", "discount", "B2B", "outreach", "account", "meeting", "opportunity", "strategy", "offer", "business", "email", "follow-up", "quota", "salesforce", "touchpoint", "funnel", "presentation", "demo", "launch", "feedback", "renewal", "cross-sell", "upsell", "prospect", "segment", "budget", "branding", "contact", "response", "adoption", "referral"],
    "Design": ["UX", "UI", "wireframe", "prototype", "aesthetic", "interface", "sketch", "figma", "illustration", "branding", "color", "palette", "layout", "concept", "mockup", "feedback", "revision", "graphic", "logo", "typography", "contrast", "grid", "symmetry", "visual", "creative", "ideation", "animation", "composition", "balance", "user-friendly", "navigation", "experience", "research", "persona", "testing", "flow", "interaction", "accessibility", "hierarchy", "element", "theme", "style", "visualization", "format", "asset", "draft", "final", "margin", "padding", "pixel"],
    "Manufacturing": ["assembly", "production", "machine", "process", "line", "plant", "schedule", "output", "tooling", "automation", "maintenance", "repair", "inventory", "stock", "QA", "QC", "waste", "efficiency", "cost", "supply", "raw material", "worker", "labor", "downtime", "cycle", "throughput", "capacity", "lean", "safety", "compliance", "standard", "SOP", "workstation", "warehouse", "logistics", "parts", "components", "inspection", "fabrication", "installation", "mechanical", "electrical", "production plan", "order", "demand", "schedule", "output", "process", "assembly", "operation"],
    "HR": ["recruitment", "onboarding", "employee", "benefits", "policy", "training", "engagement", "feedback", "leave", "PTO", "appraisal", "review", "performance", "team", "culture", "diversity", "equity", "inclusion", "DEI", "communication", "transparency", "job", "offer", "candidate", "interview", "role", "position", "vacancy", "HRBP", "HRIS", "termination", "hiring", "payroll", "attendance", "conflict", "resolution", "remote", "flexible", "motivation", "retention", "exit", "survey", "manager", "development", "compensation", "feedback", "training", "coaching", "wellness"],
    "Jaguar": ["luxury", "performance", "sleek", "agile", "sporty", "sedan", "electric", "EV", "dynamic", "elegant", "refined", "drive", "innovation", "power", "precision", "modern", "design", "style", "interior", "technology", "connectivity", "speed", "experience", "handling", "all-wheel", "comfort", "compact", "engine", "responsive", "torque", "LED", "features", "infotainment", "aerodynamics", "sculpted", "premium", "signature", "Jaguar Drive", "intelligent", "adaptive", "refinement", "British", "grille", "headlights", "seductive", "safety", "luxurious", "thrill"],
    "Range Rover": ["prestige", "SUV", "refined", "premium", "4x4", "terrain", "comfort", "leather", "quiet", "ride", "iconic", "off-road", "versatile", "capability", "elevated", "sophisticated", "elegant", "lifestyle", "bespoke", "luxury", "tailored", "command", "dynamic", "driver-assist", "panoramic", "roof", "tech", "touchscreen", "high-end", "custom", "signature", "presence", "powertrain", "smooth", "road", "bold", "LED", "air suspension", "V8", "effortless", "adaptive", "safety", "navigation", "infotainment", "grand", "experience", "precision", "design", "opulence", "excellence"],
    "Defender": ["rugged", "adventure", "durable", "explore", "outdoors", "4x4", "tough", "reliable", "trail", "all-terrain", "resilient", "performance", "capability", "freedom", "journey", "iconic", "classic", "reimagined", "stamina", "engine", "LED", "approach", "departure", "suspension", "hill descent", "off-road", "mud", "sand", "rock", "climb", "tow", "haul", "versatile", "roof rack", "snorkel", "winch", "ruggedized", "adventurous", "heritage", "exploration", "utility", "function", "terrain response", "gear", "endurance", "water wade", "grit", "torque", "rescue", "trailblazer"],
    "Discovery": ["family", "journey", "versatile", "space", "comfort", "drive", "capability", "technology", "entertainment", "seating", "luxury", "SUV", "performance", "elegant", "refinement", "adaptive", "connect", "infotainment", "storage", "panoramic", "roof", "adventure", "balanced", "smooth", "navigation", "ride", "rear-seat", "flexibility", "safety", "visibility", "intelligent", "LED", "interior", "touchscreen", "voice", "climate", "child", "comfort", "smart", "folding", "remote", "access", "USB", "comfort", "cooling", "heating", "ambient", "control", "ease", "system"]
}

internal_demo_texts = [
    "The Engineering team completed deployment and optimization of our CI/CD pipelines with improved automation that ensures fewer bugs and smoother releases.",
    "Finance completed the quarterly report with projections, budget revisions, and updated expense statements reviewed by the CFO.",
    "The Commercial team exceeded their sales quota and saw an increase in CRM-driven conversion and client engagement through personalized outreach.",
    "Design finalized the UI for the mobile app with feedback applied from user testing, improving overall user experience and interaction flow.",
    "Manufacturing optimized their assembly line processes by reducing downtime and increasing cycle throughput by 12%.",
    "HR launched new employee training modules focused on DEI, engagement, and flexible working policies. Feedback so far has been very positive.",
    "Engineering and HR should collaborate more closely to ensure new hires have access to all technical onboarding documentation.",
    "Despite solid production planning, coordination between Commercial and Manufacturing teams on order prioritization needs improvement.",
    "The Finance team needs more clarity on policy changes affecting expense allocation. We recommend a walkthrough from HR.",
    "Some Design feedback loops are delayed due to inconsistent cross-functional communication. Let’s improve alignment between departments."
]

external_demo_texts = [
    "Experience true performance with the new Jaguar EV—elegant design, powerful acceleration, and a connected drive that redefines modern luxury.",
    "The latest Range Rover offers an unmatched combination of comfort, dynamic drive, and premium interior. Discover a lifestyle of elevated refinement.",
    "Get ready to explore with Defender. Built for rugged journeys, its durability, torque, and off-road capability are second to none.",
    "The Discovery SUV reimagines comfort for the whole family. Adaptive technology, versatile storage, and seamless connectivity come standard.",
    "Jaguar's cutting-edge aerodynamics and high-performance engines now meet sustainable innovation in our latest luxury electric sedan.",
    "Range Rover's latest model features panoramic roof, leather interior, and intelligent suspension. Every journey feels first-class.",
    "Defender goes where few dare—mud, rock, or sand, it delivers power, grip, and confidence with every drive.",
    "Discovery makes daily drives exceptional. With rear-seat entertainment, USB access, and smart climate control, every seat is the best seat."
]

if st.button("Generate Sample Message"):
    st.session_state['input_text'] = random.choice(internal_demo_texts if option == "Internal" else external_demo_texts)

input_text = st.text_area("Enter a message or social media post:", height=200, key='input_text')

if st.button("Analyze"):
    if not input_text.strip():
        st.warning("Please enter a message to analyze.")
    else:
        blob = TextBlob(input_text)
        base_sentiment = blob.sentiment.polarity
        base_engagement = random.uniform(0.2, 1.0)

        def count_keyword_hits(text, keyword_list):
            return sum(1 for kw in keyword_list if kw.lower() in text.lower())

        def calculate_score(base, keyword_hits):
            bonus = min(keyword_hits * 2, 20)  # Cap bonus at 20
            return round(min(100, base * 100 + bonus))

        def generate_scores(targets):
            results = {}
            for target in targets:
                sentiment_variation = random.uniform(-0.2, 0.2)
                engagement_variation = random.uniform(-0.2, 0.2)
                text_score_sentiment = base_sentiment + sentiment_variation
                text_score_engagement = base_engagement + engagement_variation
                keyword_hits = count_keyword_hits(input_text, keyword_dict.get(target, []))
                sentiment_score = calculate_score(text_score_sentiment, keyword_hits)
                engagement_score = calculate_score(text_score_engagement, keyword_hits)
                results[target] = {
                    "Sentiment": sentiment_score,
                    "Engagement": engagement_score
                }
            return results

        if (selected_dept == "All" and option == "Internal") or (selected_brand == "All" and option == "External"):
            targets = departments[:-1] if option == "Internal" else brands[:-1]
            scores = generate_scores(targets)
            st.subheader("Individual Scores:")
            for target, score in scores.items():
                st.markdown(f"**{target}** — Sentiment: `{score['Sentiment']}`, Engagement: `{score['Engagement']}`")
        else:
            target = selected_dept if option == "Internal" else selected_brand
            score = generate_scores([target])[target]
            st.subheader(f"Scores for {target}:")
            st.markdown(f"**Sentiment Score:** `{score['Sentiment']}`")
            st.markdown(f"**Engagement Score:** `{score['Engagement']}`")
