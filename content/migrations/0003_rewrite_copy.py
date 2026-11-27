"""
New website copy (November 2026): services told as client stories, clearer FAQ
answers and tidier case study titles.

This updates the live database when the site restarts (prepare_site runs
"migrate"). The same text is also in fixtures/initial_content.json, so a brand
new database gets it too. After this, edit the text in the admin as usual.
"""
from django.db import migrations

SERVICES = {
    "lead-generation": {
        "title": "Market Entry Services",
        "icon": "compass",
        "order": 1,
        "summary": "Find out whether Cameroon is right for your business, and where to start, before you invest.",
        "headline": "You see an opportunity in Cameroon. Before you invest, you need to know it is real.",
        "challenge": (
            "Your product works elsewhere and Cameroon looks promising. But the figures you can find "
            "online are old or vague, competitors are hard to read from a distance, and a wrong first "
            "move in a new country is expensive. You need ground truth, not guesswork."
        ),
        "journey": (
            "Agree on the decision: We pin down exactly what you need to decide: which city, which "
            "customers, which price point, or whether to enter at all.\n"
            "Listen to your future customers: Our field team surveys and interviews the people you want "
            "to sell to, in the cities that matter to you.\n"
            "Map the competition: We benchmark the products, prices, channels and positioning of the "
            "players already there.\n"
            "Weigh the risks and costs: We look at demand, pricing, regulation and operating costs, the "
            "factors that make or break an entry plan."
        ),
        "outcome": (
            "A clear go, no-go or go-differently recommendation backed by fresh local data, with the "
            "cities, customers and price points to start with, and the risks to plan for."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<h3>Market feasibility studies</h3>"
            "<p>We analyse demand, competition, pricing and operational challenges to tell you whether "
            "your idea can succeed in Cameroon, and what it will take.</p>"
            "<ul><li>Understand how the Cameroonian market really works.</li>"
            "<li>Spot risks and opportunities before you commit money.</li>"
            "<li>Save time with research focused on your decision.</li></ul>"
            "<h3>Competitive analysis</h3>"
            "<p>See your competitors' strengths, weaknesses and strategies, and where the gap for you "
            "is.</p>"
            "<ul><li>A side-by-side view of competitor products, prices and market share.</li>"
            "<li>How they market themselves and keep their customers.</li>"
            "<li>Clear recommendations to stand out.</li></ul>"
            "<h3>Consumer behaviour research</h3>"
            "<p>Learn what drives your target customers' buying decisions: their habits, preferences "
            "and frustrations.</p>"
            "<ul><li>Marketing that speaks to real needs.</li>"
            "<li>Products shaped around customer expectations.</li>"
            "<li>Stronger, longer customer relationships.</li></ul>"
        ),
    },
    "marketing-research": {
        "title": "Marketing Research",
        "icon": "target",
        "order": 2,
        "summary": "Learn who your customers are, what they want and why they choose a competitor, so every campaign hits the mark.",
        "headline": "Your marketing budget is limited. Every campaign has to reach the right people with the right message.",
        "challenge": (
            "Sales have stalled, or a launch is coming, and you are not sure which customers to target "
            "or what would make them switch to you. Marketing built on assumptions wastes budget and "
            "sends a message nobody hears."
        ),
        "journey": (
            "Understand your goals: We start from the result you want: more customers, a successful "
            "launch, or winning back market share.\n"
            "Segment your market: We group your potential customers by needs, habits and spending "
            "power, and find the groups worth targeting.\n"
            "Ask real customers: Surveys, interviews and focus groups reveal what your customers think, "
            "in their own words.\n"
            "Study your competitors: We look at how competitors position, price and promote, and where "
            "they leave room for you."
        ),
        "outcome": (
            "Clear customer segments, the messages and channels that move each one, and marketing "
            "decisions built on evidence instead of assumptions."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<ul><li>Market segmentation and targeting.</li>"
            "<li>Consumer behaviour and preference studies.</li>"
            "<li>Competitive analysis to sharpen your marketing strategy.</li></ul>"
        ),
    },
    "support-function": {
        "title": "Business Intelligence",
        "icon": "chart",
        "order": 3,
        "summary": "Turn scattered data into clear reports, trend analysis and forecasts you can act on.",
        "headline": "You have data everywhere, but not the answers you need for your next decision.",
        "challenge": (
            "Sales figures sit in different spreadsheets, market news arrives in fragments, and big "
            "decisions end up being made on gut feeling. You need to see what is changing in your "
            "market early enough to act."
        ),
        "journey": (
            "Bring the data together: We combine your own figures with market and industry data.\n"
            "Clean and analyse: We check the data, then look for the patterns, trends and gaps that "
            "matter to your business.\n"
            "Look ahead: We forecast where your market is heading and flag emerging opportunities and "
            "threats.\n"
            "Report clearly: You get visual reports written for decision makers, not for statisticians."
        ),
        "outcome": (
            "Reports your team can read in minutes: how you are performing, what is changing in your "
            "sector, and where the next opportunity or threat is coming from."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<h3>Data analytics</h3>"
            "<ul><li>Sales performance tracking.</li>"
            "<li>Customer segmentation and profiling.</li>"
            "<li>Market trend forecasting.</li></ul>"
            "<h3>Industry trend reports</h3>"
            "<p>We follow the key sectors of the Cameroonian economy so you can anticipate change "
            "instead of reacting to it.</p>"
            "<h3>Custom reports for NGOs, startups and companies</h3>"
            "<ul><li>Insights shaped around your goals.</li>"
            "<li>Data-driven recommendations.</li>"
            "<li>Charts and visuals that make findings easy to share.</li></ul>"
        ),
    },
    "partnership-ecosystem": {
        "title": "Consultation Services",
        "icon": "chat",
        "order": 4,
        "summary": "Talk a big decision through with people who know the Cameroonian market, from one strategy session to a full expansion plan.",
        "headline": "You face a big decision and want an experienced partner to think it through with you.",
        "challenge": (
            "You might be weighing a new region, a new product or a new partner. You may not need a "
            "full study yet. You need straight answers from people who know the local market, and a "
            "plan you can act on."
        ),
        "journey": (
            "Strategy session: A one-on-one conversation about your goals, your situation and what is "
            "holding you back.\n"
            "Diagnosis: We identify the real issue and the information you are missing.\n"
            "Plan: For growth projects, we build an expansion plan: target regions, barriers to expect "
            "and how to get past them.\n"
            "Follow-through: We stay available as you put the plan into action."
        ),
        "outcome": (
            "Clear next steps you can act on straight away, and for growing businesses, an expansion "
            "plan that shows where to grow and how."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<h3>One-on-one strategy sessions</h3>"
            "<ul><li>Advice tailored to your business.</li>"
            "<li>Guidance from experienced consultants.</li>"
            "<li>Practical next steps toward your goals.</li></ul>"
            "<h3>Business expansion plans</h3>"
            "<ul><li>The best regions and opportunities for growth in Cameroon.</li>"
            "<li>Barriers identified and planned for in advance.</li>"
            "<li>A step-by-step route to a bigger market share.</li></ul>"
        ),
    },
    "organizational-audit": {
        "title": "Regulatory Compliance Support",
        "icon": "shield",
        "order": 5,
        "summary": "Get the licences and permits you need and stay on the right side of Cameroonian regulations, without the stress.",
        "headline": "Paperwork should not be the reason your launch is delayed.",
        "challenge": (
            "Licences, permits and changing rules can hold up a new venture for months, and a missed "
            "requirement can mean fines or disruption. Knowing which office to visit and which "
            "documents to file is hard, especially from abroad."
        ),
        "journey": (
            "Map your obligations: We list the licences, permits and rules that apply to your "
            "activity.\n"
            "Prepare the file: We help you gather and prepare the right documents the first time.\n"
            "Guide each application: We walk you through every step of the process.\n"
            "Keep you compliant: We advise you on government policies and rule changes that affect "
            "your operations."
        ),
        "outcome": (
            "The permits and licences your business needs, a clear picture of your legal obligations, "
            "and fewer surprises, so you can focus on running your business."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<h3>Licences and permits</h3>"
            "<ul><li>Step-by-step help with applications.</li>"
            "<li>A smoother process that saves you time.</li>"
            "<li>Advice to avoid common regulatory pitfalls.</li></ul>"
            "<h3>Guidance on government regulations</h3>"
            "<ul><li>Avoid costly penalties and disruptions.</li>"
            "<li>Peace of mind that you are compliant.</li>"
            "<li>More time for your core business.</li></ul>"
        ),
    },
    "marketing-strategy": {
        "title": "Digital Marketing",
        "icon": "megaphone",
        "order": 6,
        "summary": "Get found online and turn visitors into customers with SEO, social media, paid ads and useful content.",
        "headline": "Your customers are online. They should be finding you, not your competitors.",
        "challenge": (
            "You post on social media and perhaps run a few ads, but results are hard to measure and "
            "enquiries are not growing. Without a plan grounded in how your audience actually behaves "
            "online, digital spending is guesswork."
        ),
        "journey": (
            "Audit: We review your website, social media and past campaigns to see what works and what "
            "does not.\n"
            "Plan: We build a strategy around your audience, based on research rather than trends.\n"
            "Launch: We run your SEO, social media, paid advertising and content campaigns.\n"
            "Measure and improve: We track the results and adjust what is not performing."
        ),
        "outcome": (
            "A stronger online presence, campaigns that reach the right people, and results you can "
            "measure in visits, enquiries and sales."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<ul><li>Search engine optimisation (SEO) so customers find you on Google.</li>"
            "<li>Social media marketing that starts conversations.</li>"
            "<li>Pay-per-click (PPC) campaigns that reach precise audiences.</li>"
            "<li>Content marketing that builds authority and trust.</li></ul>"
        ),
    },
    "new-business-innovation": {
        "title": "Research for Nonprofits and NGOs",
        "icon": "heart",
        "order": 7,
        "summary": "Evidence that helps NGOs design better programmes, show their impact and win the funding to keep going.",
        "headline": "Donors want evidence. Communities deserve programmes that meet their real needs.",
        "challenge": (
            "You are designing a programme, writing a proposal or reporting to donors. You need "
            "reliable data from the communities you serve, collected with respect, and turned into "
            "findings that funders trust."
        ),
        "journey": (
            "Understand your mission: We start with your goals, your communities and what your donors "
            "need to see.\n"
            "Listen in the field: Needs assessments and perception surveys capture what communities "
            "experience and expect.\n"
            "Measure impact: We evaluate the reach and effectiveness of your programmes.\n"
            "Find funding partners: Donor mapping identifies the funders whose priorities match yours, "
            "and how to approach them."
        ),
        "outcome": (
            "Donor-ready reports, clear evidence of your impact, a map of the funders most likely to "
            "support you, and recommendations that make your next programme stronger."
        ),
        "body": (
            "<h2>What's included</h2>"
            "<h3>Social impact analysis</h3>"
            "<ul><li>Assess the reach and effectiveness of your programmes.</li>"
            "<li>Find what to improve.</li>"
            "<li>Communicate your impact to donors and stakeholders.</li></ul>"
            "<h3>Donor mapping</h3>"
            "<ul><li>Target the right donors with tailored outreach.</li>"
            "<li>Open up more funding opportunities.</li>"
            "<li>Make your organisation more sustainable.</li></ul>"
            "<h3>Needs assessments and community surveys</h3>"
            "<p>Field research that puts community voices at the centre of your programme design.</p>"
        ),
    },
}

FAQS = {
    1: (
        "Who do you work with?",
        "<p>Startups, established companies and nonprofit organisations, in sectors such as "
        "agriculture, technology, tourism and manufacturing. Whether you are new to Cameroon or "
        "already here and growing, we shape the research around your goals.</p>",
    ),
    2: (
        "How long does a research project take?",
        "<p>It depends on the scope. Smaller projects, such as a competitor analysis, usually take "
        "2 to 4 weeks. In-depth work, such as a feasibility study or an industry report, usually "
        "takes 6 to 12 weeks.</p><p>You get a precise timeline after your first consultation.</p>",
    ),
    3: (
        "How do you make sure your research is accurate?",
        "<p>We combine trusted data sources, our own field data and local knowledge. Findings are "
        "cross-checked by the team, and we use industry-standard tools to collect and analyse "
        "data.</p>",
    ),
    4: (
        "What makes you different from other research firms?",
        "<p>We focus on Cameroon. You get local knowledge and global research standards in one "
        "team, and recommendations built around your decision, not a generic report.</p>",
    ),
    5: (
        "Is the first consultation free?",
        "<p>Yes. Your first consultation is free. We use it to understand your goals and suggest "
        "the research that fits your needs and budget.</p>",
    ),
    6: (
        "Which industries do you know best?",
        "<p>We have worked in:</p><ul><li>Agriculture</li><li>Technology and IT</li>"
        "<li>Tourism and hospitality</li><li>Manufacturing</li><li>NGOs and nonprofits</li></ul>"
        "<p>Don't see your industry? Get in touch. We are happy to talk about your project.</p>",
    ),
    7: (
        "How much does a research project cost?",
        "<p>The price depends on the scope, the complexity and the timeline. After the free "
        "consultation, we send you a detailed proposal with clear pricing, and we work to deliver "
        "real value within your budget.</p>",
    ),
    8: (
        "Do you work outside Cameroon?",
        "<p>Yes. Cameroon is our home market, and our insights also help organisations working in, "
        "or expanding to, other parts of Africa.</p>",
    ),
    9: (
        "How do you protect confidential information?",
        "<p>Your information stays confidential and is handled with care. We are happy to sign a "
        "non-disclosure agreement (NDA) before you share anything sensitive.</p>",
    ),
}

CASE_STUDY_TITLES = {
    "fashion-retailer-market-entry-study": "Entry viability study for an international fashion retailer targeting Yaoundé",
    "competitor-benchmarking-report": "Competitor benchmarking for a South African fast food chain entering Cameroon",
    "consumer-behavior-survey": "Consumer behaviour survey on mobile money use in urban Cameroon",
    "study-on-mineral-water-brands": "Consumer preference study on mineral water brands in Cameroon",
    "community-perception-survey": "Community perception survey for a humanitarian organisation",
    "marketing-research": "Needs assessment for a community health initiative in rural Cameroon",
}

# Placeholder "lorem ipsum" text left over from the old WordPress theme.
FILLER = (
    "<p>Envisioned multimedia based expertise and cross-media growth strategies. Seamlessly "
    "visualize quality intellectual capital without superior collaboration and idea-sharing. "
    "Holistically pontificate installed base portals after maintainable products.</p>\n"
)

# This excerpt was copied by mistake from an unrelated blog post.
ARTICLE_EXCERPTS = {
    "market-entry-challenges-in-cameroon": (
        "The most common obstacles businesses meet when entering Cameroon, and practical ways to "
        "overcome them. Essential reading for investors and startups."
    ),
}


def forwards(apps, schema_editor):
    Service = apps.get_model("content", "Service")
    FAQ = apps.get_model("content", "FAQ")
    CaseStudy = apps.get_model("content", "CaseStudy")
    Article = apps.get_model("content", "Article")

    for slug, fields in SERVICES.items():
        Service.objects.filter(slug=slug).update(**fields)
    for pk, (question, answer) in FAQS.items():
        FAQ.objects.filter(pk=pk).update(question=question, answer=answer)
    for slug, title in CASE_STUDY_TITLES.items():
        CaseStudy.objects.filter(slug=slug).update(title=title)
    for case in CaseStudy.objects.filter(body__contains="Holistically pontificate"):
        case.body = case.body.replace(FILLER, "")
        case.save(update_fields=["body"])
    for slug, excerpt in ARTICLE_EXCERPTS.items():
        Article.objects.filter(slug=slug).update(excerpt=excerpt)


class Migration(migrations.Migration):
    dependencies = [("content", "0002_service_story")]
    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
