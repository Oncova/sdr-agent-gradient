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
        "- Price: $199/month flat rate. NO trial. NO weekly billing. NO negotiation.\n"
        "- Never mention $99, 'trial', 'free', or 'test period.'\n\n"
        "SPECIALTY-SPECIFIC PITCH:\n"
        "- If primary_specialty = 'PI': The AI is trained to triage accident and injury emergencies.\n"
        "- If primary_specialty = 'CD': The AI is trained for arrest and bail emergencies.\n\n"
        "CORE PITCH: 'Missing one intake call costs you thousands. For $199/month, your AI receptionist "
        "works 24/7, extracts case details from every caller, and instantly texts you a triage brief.'\n\n"
        "CTA: 'Call [TWILIO_DEMO_NUMBER] right now to hear how she handles a frantic client. "
        "If you want her answering your overflow calls for $199/month, reply to this email.'\n\n"
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
                f"For $199/month, our AI receptionist answers 24/7, {ai_desc}. "
                f"She extracts case details and instantly texts you a triage brief. "
                f"Call [TWILIO_DEMO_NUMBER] right now to hear her handle a frantic client. "
                f"Reply to this email for $199/month."
            )
        }
