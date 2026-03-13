"""
ElevenLabs MCP — Core revenue-driving voice synthesis engine.
Generates personalized $99/week trial pitches and streams
the audio output directly into Google Drive.
"""

import requests
from gradient_adk import MCPClient


def initialize_elevenlabs_mcp(vault_mcp, workspace_mcp):
    el_creds = vault_mcp.execute_tool("fetch_secret", path="elevenlabs")

    eleven_mcp = MCPClient(
        name="voice-synth-engine",
        capabilities=["text_to_speech"],
    )

    @eleven_mcp.register_tool(
        description="Synthesize personalized $99 trial pitch and stream to Drive."
    )
    def synthesize_pitch(attorney_name: str, practice_area: str) -> str:
        script = (
            f"Hi {attorney_name}, I saw you handle a lot of {practice_area} cases "
            f"down here in South Florida. I've built an AI receptionist that handles "
            f"intake 24/7. I'm offering a $99 per week trial."
        )

        headers = {
            "xi-api-key": el_creds.get("api_key", ""),
            "Content-Type": "application/json",
        }
        payload = {
            "text": script,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{el_creds.get('voice_id', '')}",
            json=payload,
            headers=headers,
        )

        if response.status_code == 200:
            filename = f"{attorney_name.replace(' ', '_')}_pitch.mp3"
            drive_link = workspace_mcp.execute_tool(
                "upload_to_drive", filename=filename, content=response.content
            )
            return drive_link

        raise Exception(f"Synthesis engine failure: {response.text}")

    return eleven_mcp
