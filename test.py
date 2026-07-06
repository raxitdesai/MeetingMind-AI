from src.orchestrator.meetingmind_orchestrator import MeetingMindOrchestrator

transcript = """
Weekly Meeting

Alice will prepare documentation.
Bob will deploy the application.
Charlie will perform testing.
"""

orchestrator = MeetingMindOrchestrator()

result = orchestrator.process_meeting(transcript)

print(result)