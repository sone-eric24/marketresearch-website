"""Fixed text used on the home and about pages.

Edit the wording here, then restart the site. Lists marked "FILL IN" are empty
on purpose: the section that uses them stays hidden until you add real content.
"""

# The four steps of every project (home and about pages).
PROCESS_STEPS = [
    ("Listen",
     "A free first conversation about your goals, your questions and the decision you need to make."),
    ("Research",
     "We collect and analyse the data, in the field and from trusted sources, to uncover trends, "
     "opportunities and risks."),
    ("Recommend",
     "You get clear findings and practical recommendations, not a pile of raw data."),
    ("Support",
     "Our work doesn’t stop at the report. We stay with you as you put the recommendations into "
     "action."),
]

# Who we help (home page). Each audience is told as a short "you" story.
AUDIENCES = [
    {
        "icon": "compass",
        "title": "Investors and international companies",
        "story": "You are considering Cameroon and need to know if the opportunity is real, which "
                 "city to start in and who you will compete with.",
        "link_text": "Market entry services",
        "slug": "lead-generation",
    },
    {
        "icon": "rocket",
        "title": "Local startups and growing businesses",
        "story": "You want to launch a product, win more customers or expand to a new region, "
                 "without betting your budget on guesswork.",
        "link_text": "Marketing research",
        "slug": "marketing-research",
    },
    {
        "icon": "heart",
        "title": "NGOs and development partners",
        "story": "You need reliable community data to design programmes, prove your impact and "
                 "convince donors.",
        "link_text": "Research for nonprofits",
        "slug": "new-business-innovation",
    },
    {
        "icon": "globe",
        "title": "International research agencies",
        "story": "You have a study to run in Cameroon but no team on the ground. You need a local "
                 "partner who can collect reliable data to your specifications.",
        "link_text": "Field data collection",
        "slug": "field-data-collection",
    },
]

# About page: our story in three short chapters (problem, answer, promise).
ABOUT_STORY = [
    ("The problem we saw",
     "Cameroon is full of opportunity. Yet too many good projects start on guesswork: old "
     "statistics, second-hand opinions, or a model copied from another country. When the "
     "assumptions are wrong, businesses lose money and NGO programmes miss the people they are "
     "meant to serve."),
    ("What we set out to do",
     "Winning Solutions Market Research was created to close that gap. We go to the field, listen "
     "to real customers and communities, and combine what we hear with international research "
     "methods. Then we turn it into recommendations people can act on."),
    ("Where we are going",
     "Our ambition is to be the most trusted market research partner in Africa, starting at home "
     "in Cameroon. Every project we deliver is a step toward that promise."),
]

CORE_VALUES = [
    ("check", "Integrity", "Honest, unbiased findings, even when they are not what you hoped to hear."),
    ("star", "Excellence", "Careful methods and high-quality work you can rely on and defend."),
    ("bulb", "Innovation", "We use new tools and fresh thinking to answer your questions better."),
    ("people", "Client first", "Your goals guide every step. Your success is how we measure ours."),
]

DIFFERENTIATORS = [
    ("pin", "Local knowledge, global standards",
     "We are based in Cameroon and know its markets from the inside, and we apply internationally "
     "recognised research methods."),
    ("tools", "Built around your decision",
     "No two organisations are alike. Every study is designed around your goals, your questions "
     "and your budget."),
    ("layers", "Everything in one place",
     "From feasibility studies to competitor benchmarking and consumer research, one team covers "
     "the full journey."),
    ("clipboard", "Your field partner in Cameroon",
     "International research agencies rely on us to run their fieldwork locally, to their "
     "methodology and standards."),
    ("flag", "Focused on results",
     "We don’t just hand over data. We give you clear recommendations and help you act on them."),
]

# FILL IN: key figures shown on the home page, e.g. ("40+", "studies delivered").
# Only add numbers you can prove. The section stays hidden while this list is empty.
KEY_FIGURES = [
    # ("[number]", "projects completed"),
    # ("[number]", "people surveyed"),
    # ("[number]", "sectors covered"),
]

# Client testimonials, kept word for word from the old website.
# FILL IN: confirm each one is from a real client who agreed to be quoted, and add
# a name or company where the client allows it.
TESTIMONIALS = [
    {
        "quote": "WS Market Research delivered exactly what we needed to make an informed investment "
                 "decision in Cameroon. Their market entry analysis was clear, actionable, and far more "
                 "detailed than we expected. Their understanding of local markets is exceptional. We are "
                 "now moving forward confidently thanks to their guidance.",
        "name": "Foreign Investor",
        "role": "Director of Expansion, Regional Investment Firm",
    },
    {
        "quote": "Working with WS Market Research was one of the best strategic decisions we made. Their "
                 "feasibility study helped us refine our business model and understand our target market "
                 "better. Their professionalism, speed, and depth of insight are outstanding. Highly "
                 "recommended for any startup in Cameroon.",
        "name": "Local Startup Founder",
        "role": "Founder, Technology Startup in Douala",
    },
    {
        "quote": "The needs assessment conducted by WS Market Research provided invaluable data that shaped "
                 "our entire health intervention program. Their field team was thorough, respectful, and "
                 "culturally sensitive. The final report was donor-ready and exceeded our expectations. We "
                 "will definitely work with them again.",
        "name": "NGO / Development Partner",
        "role": "Program Manager, International NGO Operating in Cameroon",
    },
    {
        "quote": "WS Market Research helped us understand Cameroonian consumers in a way no other firm has. "
                 "The insights from their consumer behavior survey guided our product launch strategy and "
                 "significantly improved our marketing decisions. They are truly the leading research "
                 "partner in Cameroon.",
        "name": "Corporate Client",
        "role": "Marketing Manager, FMCG Company in West Africa",
    },
]
