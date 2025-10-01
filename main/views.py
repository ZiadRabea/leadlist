from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMessage

import json
import requests

from .models import Lead



@csrf_exempt
@require_POST
def lead_capture(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            name = data.get("name")
            school = data.get("school")
            email = data.get("email")
            phone = data.get("phone")

            # 1. Save to DB
            Lead.objects.create(
                name=name,
                school=school,
                email=email,
                phone=phone,
                created_at=timezone.now(),
                state="Lead"
            )

            # 2. PDF file URL (Google Drive direct download)
            pdf_url = "https://drive.google.com/uc?export=download&id=1Qc6C9nMy5B4d5zLFt6bZn6ZNFuKgBZIi"

            subject = "🎉 Thanks for booking a demo with Mawjood"
            message = (
                f"Hello {name},\n\n"
                f"Thank you for booking a demo with Mawjood! 🚀\n\n"
                f"Attached is your onboarding guide to help you get started.\n\n"
                f"Our team will reach out to you shortly.\n\n"
                f"- Mawjood Team"
            )

            # 3. Try attaching the PDF from URL
            try:
                response = requests.get(pdf_url)
                response.raise_for_status()

                email_message = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email="opindustries5@gmail.com",
                    to=[email],
                )

                # Attach PDF in-memory
                email_message.attach(
                    "Mawjood-Onboarding-Guide.pdf",
                    response.content,
                    "application/pdf"
                )
                email_message.send(fail_silently=False)

            except Exception as e:
                # If PDF fetch fails, fallback to link only
                fallback_message = (
                    f"{message}\n\n"
                    f"You can also view the onboarding guide here:\n{pdf_url}"
                )
                EmailMessage(
                    subject=subject,
                    body=fallback_message,
                    from_email="opindustries5@gmail.com",
                    to=[email],
                ).send(fail_silently=False)

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)


@login_required
def show_leads(request):
    leads = Lead.objects.all()
    
    context = {
        "leads": leads
    }

    return render(request, "leads.html", context)

@login_required
def delete_lead(request, id):
    lead = Lead.objects.get(id=id)
    lead.delete()
    return redirect("/")

@login_required
def update_state(request, id, status):
    lead = Lead.objects.get(id=id)
    lead.state = status
    lead.save()
    return redirect("/")

def reset(request):
    if request.GET.get("token") == "secret123":
        return JsonResponse({"status": "success", "message": "Absences reset"})
    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
