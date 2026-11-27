"""
Adds the "Field Data Collection" service (for international research agencies and
local clients) and a matching FAQ.

Only runs on a database that already has content (the live site). A brand new
database gets the same text from fixtures/initial_content.json instead.
"""
from django.db import migrations

SERVICE = {
    "slug": "field-data-collection",
    "title": "Field Data Collection",
    "icon": "clipboard",
    "order": 8,
    "summary": "Your team on the ground in Cameroon. We collect reliable field data for international "
               "research agencies and local organisations, to your specifications.",
    "headline": "Your agency has a study to run in Cameroon, but no team on the ground.",
    "challenge": (
        "You have won a multi-country project, or a client needs answers from Cameroon. Flying a "
        "team in is expensive, the terrain and the culture are unfamiliar, and your client still "
        "expects clean data, on time and on budget. You need a local partner you can trust with "
        "your methodology."
    ),
    "journey": (
        "Review your study: We go through your questionnaire, sample and timeline with you, and "
        "suggest adjustments so they work in the Cameroonian context.\n"
        "Prepare the field: We recruit and brief interviewers for your project and plan the "
        "fieldwork across the locations you need.\n"
        "Collect the data: Our team carries out the interviews, surveys or group discussions you "
        "specify, and keeps you updated on progress as fieldwork moves forward.\n"
        "Check and deliver: We check the quality of the data as it comes in, then deliver it in "
        "the format you need."
    ),
    "outcome": (
        "Reliable data from Cameroon, collected to your specifications and delivered on schedule, "
        "without the cost of setting up your own local operation. Your agency keeps the client "
        "relationship and the analysis; we take care of the field."
    ),
    "body": (
        "<h2>What's included</h2>"
        "<h3>For international research agencies</h3>"
        "<ul><li>A local field partner for single-country or multi-country studies.</li>"
        "<li>Adaptation of questionnaires and sampling plans to local realities.</li>"
        "<li>Recruitment, briefing and supervision of field teams.</li>"
        "<li>Quality checks during fieldwork and clean data at delivery.</li>"
        "<li>Confidentiality: we are happy to sign your NDA.</li></ul>"
        "<h3>For local companies and NGOs</h3>"
        "<p>Already have a research design and only need the fieldwork done? We collect the "
        "data for you, so your team can focus on the analysis and the decisions.</p>"
        "<p><em>Tell us about your study, including the methods, locations, sample size and "
        "timeline, and we will send you a detailed fieldwork proposal.</em></p>"
    ),
}

FAQ_ITEM = {
    "question": "Do you work with research agencies based outside Cameroon?",
    "answer": (
        "<p>Yes. International research agencies use us as their field partner in Cameroon. We "
        "adapt your questionnaire to the local context, run the fieldwork and deliver clean data "
        "to your specifications. <a href=\"/services/field-data-collection/\">See how field data "
        "collection works</a>.</p>"
    ),
    "order": 9,
}


def forwards(apps, schema_editor):
    Service = apps.get_model("content", "Service")
    FAQ = apps.get_model("content", "FAQ")

    if Service.objects.exists() and not Service.objects.filter(slug=SERVICE["slug"]).exists():
        Service.objects.create(**SERVICE)

    if FAQ.objects.exists() and not FAQ.objects.filter(question=FAQ_ITEM["question"]).exists():
        # Put it just before the last question (confidentiality).
        FAQ.objects.filter(order__gte=FAQ_ITEM["order"]).update(order=10)
        FAQ.objects.create(**FAQ_ITEM)


class Migration(migrations.Migration):
    dependencies = [("content", "0004_service_icon_clipboard")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
