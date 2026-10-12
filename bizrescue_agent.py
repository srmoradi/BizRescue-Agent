
import os
import json
import uuid
import urllib.request
from datetime import datetime

API_URL = "https://litellm.vision.aivar.app/v1/chat/completions"
MODEL = "nova-micro"


def ask_model(incident):
    api_key = os.environ.get("LITELLM_API_KEY")

    if not api_key:
        return "AI analysis skipped: LITELLM_API_KEY is not set."

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are BizRescue Agent. Analyze the recorded workflow "
                    "events briefly. Never claim an action occurred unless "
                    "it appears in the supplied event data."
                )
            },
            {
                "role": "user",
                "content": json.dumps(incident)
            }
        ],
        "temperature": 0.2
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"]
    except Exception as exc:
        return "AI analysis unavailable: " + str(exc)


def run_workflow():
    run_id = str(uuid.uuid4())
    events = []

    print("\n=== BizRescue Agent ===")
    print("Test: real file export with controlled failure\n")

    # Deliberately use a directory that this test does not create.
    primary_path = os.path.join(
        "primary_target_DO_NOT_CREATE",
        "report.json"
    )

    report_data = {
        "run_id": run_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "message": "BizRescue recovery test"
    }

    try:
        with open(primary_path, "w", encoding="utf-8") as file:
            json.dump(report_data, file)

        events.append({
            "event": "primary_export",
            "status": "success"
        })
        print("[1] Primary export: SUCCESS")

    except OSError as exc:
        events.append({
            "event": "primary_export",
            "status": "failed",
            "error": str(exc)
        })
        print("[1] Primary export: FAILED")
        print("    Reason:", exc)

    recovered_path = "recovered_export.json"

    try:
        with open(recovered_path, "w", encoding="utf-8") as file:
            json.dump(report_data, file, indent=2)

        events.append({
            "event": "fallback_export",
            "status": "success",
            "path": recovered_path
        })
        print("[2] Fallback export: SUCCESS")

    except OSError as exc:
        events.append({
            "event": "fallback_export",
            "status": "failed",
            "error": str(exc)
        })
        print("[2] Fallback export: FAILED")

    verified = False

    try:
        with open(recovered_path, "r", encoding="utf-8") as file:
            saved_data = json.load(file)

        verified = saved_data.get("run_id") == run_id

    except (OSError, ValueError):
        verified = False

    events.append({
        "event": "verification",
        "status": "passed" if verified else "failed"
    })

    print("[3] Verification:", "PASSED" if verified else "FAILED")

    incident = {
        "run_id": run_id,
        "workflow": "report_export",
        "primary_status": events[0]["status"],
        "fallback_status": (
            events[1]["status"] if len(events) > 1 else "unknown"
        ),
        "verified": verified,
        "events": events
    }

    print("\n[4] Analyzing recorded events with AI...")
    analysis = ask_model(incident)

    print("\nAI analysis:\n" + analysis)

    final_status = (
        "recovered"
        if verified and incident["fallback_status"] == "success"
        else "unresolved"
    )

    report = {
        "agent": "BizRescue Agent",
        "run_id": run_id,
        "workflow": "report_export",
        "status": final_status,
        "events": events,
        "ai_analysis": analysis
    }

    with open("run_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    with open("events.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(report, ensure_ascii=False) + "\n")

    print("\nReport saved to: run_report.json")
    print("Recovered file: " + recovered_path)
    print("Event history appended to: events.jsonl")
    print("Final status:", final_status.upper())


if __name__ == "__main__":
    run_workflow()
