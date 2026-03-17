import json
from openclaw_sdk import Agent, entrypoint

sdr_agent = Agent(
    name="gpt54-sdr-brain",
    model="openai-gpt-5.4",
    system_prompt=(
        "You are an elite Sales Development Representative for Zuldeira Technologies. "
        "You send cold outreach emails to qualified Personal Injury (PI) and Criminal Defense (CD) attorneys.\n\n"
        "THE OFFER:\n"
        "- Product: A hyper-specialized AI receptionist exclusively trained for the attorney's practice area.\n"
        "- Lead offer: $99 trial week — one full week, no commitment.\n"
        "- Subscription: $199/month after the trial.\n"
        "- Optional: They can schedule a quick 5-minute demo to hear her in action before committing.\n\n"
        "SPECIALTY-SPECIFIC PITCH:\n"
        "- If primary_specialty = 'PI': The AI is trained to triage accident and injury emergencies.\n"
        "- If primary_specialty = 'CD': The AI is trained for arrest and bail emergencies.\n\n"
        "CORE PITCH: 'Missing one intake call costs you thousands. Try our AI receptionist "
        "for $99 this week — she works 24/7, extracts case details from every caller, and instantly "
        "texts you a triage brief. After the trial, it's just $199/month.'\n\n"
        "CTA (in order):\n"
        "1. 'Want to hear her first? Reply and we'll set up a 5-minute demo today.'\n"
        "2. 'Ready to try? Reply to start your $99 trial week.'\n\n"
        "STRICT EXECUTION CONSTRAINTS:\n"
        "1. Email body must be strictly under 120 words.\n"
        "2. Highly personalize to the attorney's firm name and practice area.\n"
        "3. Subject line must be urgent and specific to their specialty.\n"
        "4. Output strictly as JSON: {\"subject\": \"...\", \"pitch_body\": \"...\"}\n"
        "5. No markdown, no code blocks, no filler text."
    )
)

@entrypoint
def generate_sdr_pitch(payload: dict) -> dict:
    name = payload.get("name", "Attorney")
    firm = payload.get("firm", "the firm")
    practice_area = payload.get("practice_area", "law")
    specialty_tag = payload.get("primary_specialty", "PI")
    
    prompt = (
        f"Prospect Details:\n"
        f"Name: {name}\n"
        f"Firm: {firm}\n"
        f"Practice Area: {practice_area}\n"
        f"Specialty Tag: {specialty_tag}"
    )
    
    response = sdr_agent.invoke(prompt)
    
    try:
        raw_text = response.content if hasattr(response, "content") else str(response)
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception:
        if specialty_tag == "CD":
            area_label = "criminal defense"
            ai_desc = "trained for criminal defense intake — DUI, domestic violence, felony charges"
        else:
            area_label = "personal injury"
            ai_desc = "trained for personal injury intake — car crashes, slip-and-falls, workplace injuries"
        
        return {
            "subject": f"Your {firm} misses calls that are worth $10K+ — here's the fix",
            "pitch_body": (
                f"Hi {name}, a missed {area_label} intake call costs your firm thousands. "
                f"Try our AI receptionist for $99 this week — she answers 24/7, {ai_desc}. "
                f"She extracts case details and instantly texts you a triage brief. "
                f"Want to hear her first? Reply and we'll set up a 5-minute demo today. "
                f"Ready to try? Reply to start your $99 trial week. After that, just $199/month."
            )
        }
