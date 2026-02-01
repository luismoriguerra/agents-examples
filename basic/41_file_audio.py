import base64
from agno.agent import Agent
from agno.models.openai import OpenAIChat

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    name="OpenAI Speech Agent",
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    ),
    markdown=True,
)

response = agent.run("Say: 'Hello, this is a synthesized voice example.'")
print(f"Response content: {response.content if response else 'None'}")
if response and response.response_audio:
    # The content is base64-encoded bytes, decode it
    audio_bytes = base64.b64decode(response.response_audio.content)
    with open("tmp/hello.wav", "wb") as f:
        f.write(audio_bytes)
    print("Audio saved to tmp/hello.wav")
else:
    print("No audio in response")