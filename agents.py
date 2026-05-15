from dotenv import load_dotenv
from livekit import agents
from prompt import AGENT_INSTRUCTION, AGENT_RESPONSE
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import (
       google, # Using Google for the model as in your previous snippet
       ai_coustics, # The new noise cancellation plugin
)

load_dotenv(".env")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTION )

server = AgentServer()

@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: agents.JobContext):
    session = AgentSession(
    llm=google.realtime.RealtimeModel(
            voice="Aoede",
            temperature=0.8,
           ),
       )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(
        audio_input=room_io.AudioInputOptions(
                   # FIX: Using the documented ai_coustics plugin
        noise_cancellation=ai_coustics.audio_enhancement(
        model=ai_coustics.EnhancerModel.QUAIL_VF_L
                   ),
               ),
           ),
       )

    await session.generate_reply(
        instructions=AGENT_RESPONSE
       )

if __name__ == "__main__":
       agents.cli.run_app(server)
