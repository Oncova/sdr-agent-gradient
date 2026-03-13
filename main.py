import json
from openclaw_sdk import Agent, entrypoint

sdr_agent = Agent(
    name="gpt54-sdr-brain",
    model="openai-gpt-5.4",
    system_prompt=(
        "You are an elite Sales Development Representative for an AI voice receptionist agency. "
        "Your objective is to pitch a $99/week trial for an ElevenLabs-powered AI voice receptionist "
        "specifically to solo Personal Injury and Criminal Defense attorneys in South Florida.\n\n"
        "Strict Execution Constraints:\n"
        "1. The email body must be strictly under 100 words.\n"
        "2. Highly personalize the message to the attorney's specific firm name and practice area.\n"
        "3. End the email with a soft call-to-action asking if they are open to hearing a quick audio sample of the AI handling a mock intake call.\n"
        "4. Output your response strictly as a JSON object containing exactly two keys: 'subject' and 'pitch_body'.\n"
        "5. Do not include markdown formatting, code blocks, conversational filler, or any text outside the JSON."
    )
)

@entrypoint
def generate_sdr_pitch(payload: dict) -> dict:
    name = payload.get("name", "Attorney")
    firm = payload.get("firm", "the firm")
    practice_area = payload.get("practice_area", "law")
    
    prompt = (
        f"Prospect Details:\n"
        f"Name: {name}\n"
        f"Firm: {firm}\n"
        f"Practice Area: {practice_area}"
    )
    
    response = sdr_agent.invoke(prompt)
    
    try:
        raw_text = response.content if hasattr(response, "content") else str(response)
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception:
        return {
            "subject": f"AI Voice Receptionist Trial for {firm}",
            "pitch_body": f"Hi {name}, I saw you handle {practice_area} cases in South Florida. I built an AI receptionist that handles intake 24/7, and I'm offering a $99/week trial. Would you be open to hearing a quick audio sample of it answering a call for {firm}?"
        }
