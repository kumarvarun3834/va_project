from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .va_core import process_command
from .models import ChatSession, ChatMessage
from django.core.exceptions import ObjectDoesNotExist


# ================= HOME =================
def home(request):
    return render(request, "assistant/index.html")


# ================= MAIN ASSISTANT =================
@csrf_exempt
def assistant_view(request, session_id=None):
    if request.method != "POST":
        return JsonResponse({"type": "error", "message": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)
        command = data.get("command", "").strip()

        if not command:
            return JsonResponse({"type": "error", "message": "Empty command"}, status=400)

        # 🔥 Process command (returns dict now)
        response = process_command(command)

        # ===== SESSION HANDLING =====
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
            except ChatSession.DoesNotExist:
                return JsonResponse({"type": "error", "message": "Session not found"}, status=404)
        else:
            session = ChatSession.objects.create(title=command[:30] or "New Chat")

        # ===== SAVE MESSAGES =====
        ChatMessage.objects.create(
            session=session,
            role="user",
            content=command
        )

        # Only store readable assistant text
        assistant_text = response.get("message", "") if isinstance(response, dict) else str(response)

        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=assistant_text
        )

        # 🔥 RETURN STRUCTURED RESPONSE
        return JsonResponse({
            **response,
            "session_id": session.id
        })

    except json.JSONDecodeError:
        return JsonResponse({"type": "error", "message": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"type": "error", "message": str(e)}, status=500)


# ================= GET SESSIONS =================
def get_sessions(request):
    sessions = ChatSession.objects.all().order_by("-created_at")

    data = [
        {
            "id": s.id,
            "title": s.title or f"Session {s.id}"
        }
        for s in sessions
    ]

    return JsonResponse({"sessions": data})


# ================= GET HISTORY =================
def get_history(request, session_id):
    try:
        session = ChatSession.objects.get(id=session_id)
    except ObjectDoesNotExist:
        return JsonResponse({"type": "error", "message": "Session not found"}, status=404)

    messages = session.messages.order_by("timestamp")

    history = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in messages
    ]

    return JsonResponse({"history": history})


# ================= DELETE SESSION =================
@csrf_exempt
def delete_session(request, session_id):
    if request.method != "DELETE":
        return JsonResponse({"type": "error", "message": "DELETE request required"}, status=400)

    try:
        session = ChatSession.objects.get(id=session_id)
        session.delete()

        return JsonResponse({
            "type": "success",
            "message": "Session deleted successfully"
        })

    except ChatSession.DoesNotExist:
        return JsonResponse({"type": "error", "message": "Session not found"}, status=404)

    except Exception as e:
        return JsonResponse({"type": "error", "message": str(e)}, status=500)


# ================= UPDATE SESSION =================
@csrf_exempt
def update_session(request, session_id):
    if request.method != "PUT":
        return JsonResponse({"type": "error", "message": "PUT request required"}, status=400)

    try:
        data = json.loads(request.body)
        new_title = data.get("title", "").strip()

        if not new_title:
            return JsonResponse({"type": "error", "message": "Title cannot be empty"}, status=400)

        session = ChatSession.objects.get(id=session_id)
        session.title = new_title
        session.save()

        return JsonResponse({
            "type": "success",
            "message": "Session title updated successfully"
        })

    except ChatSession.DoesNotExist:
        return JsonResponse({"type": "error", "message": "Session not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"type": "error", "message": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"type": "error", "message": str(e)}, status=500)