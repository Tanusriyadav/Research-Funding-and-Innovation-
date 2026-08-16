import re
from collections import defaultdict

from sqlalchemy.orm import Session
from app.models.publication import Publication
from app.models.patent import Patent
from app.models.research_profile import ResearchProfile

STOPWORDS = {
    "the", "and", "for", "with", "using", "based", "from", "into", "study",
    "analysis", "review", "approach", "towards", "via", "of", "on", "in",
    "to", "a", "an", "is", "are", "new", "novel", "improved", "toward",
    "system", "systems", "model", "models", "method", "methods", "framework",
    "device", "devices", "apparatus"
}


def _extract_words(title: str):
    words = re.findall(r"[a-zA-Z]+", title.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def get_technology_intelligence(db: Session, top_n: int = 10):
    """
    Cross-references research publications and patents to identify
    technology areas and classify their maturity.

    If no publication/patent data exists, uses research profile domains
    as profile-based technology signals.
    """

    pub_titles = db.query(Publication.title).all()
    patent_titles = db.query(Patent.title).all()

    pub_counts = defaultdict(int)
    patent_counts = defaultdict(int)

    for (title,) in pub_titles:
        if not title:
            continue

        for word in _extract_words(title):
            pub_counts[word] += 1

    for (title,) in patent_titles:
        if not title:
            continue

        for word in _extract_words(title):
            patent_counts[word] += 1

    all_words = set(pub_counts.keys()) | set(patent_counts.keys())

    results = []

    for word in all_words:
        research_mentions = pub_counts.get(word, 0)
        patent_mentions = patent_counts.get(word, 0)

        # Ignore technology words with no actual data
        if research_mentions == 0 and patent_mentions == 0:
            continue

        total = research_mentions + patent_mentions

        if total >= 5:
            maturity = "Mature"
        elif total >= 2:
            maturity = "Growing"
        else:
            maturity = "Emerging"

        results.append({
            "technology": word,
            "research_mentions": research_mentions,
            "patent_mentions": patent_mentions,
            "total_mentions": total,
            "cross_domain": (
                research_mentions > 0
                and patent_mentions > 0
            ),
            "maturity": maturity,
        })

    # If there is no publication/patent data,
    # use the user's research profile domains.
    if not results:
        profiles = db.query(ResearchProfile).all()

        profile_domains = set()

        for profile in profiles:
            if not profile.research_domains:
                continue

            domains = profile.research_domains.split(",")

            for domain in domains:
                domain = domain.strip()

                if domain:
                    profile_domains.add(domain)

        for domain in profile_domains:
            results.append({
                "technology": domain,
                "research_mentions": 0,
                "patent_mentions": 0,
                "total_mentions": 0,
                "cross_domain": False,
                "maturity": "Emerging",
                "source": "Research Profile",
            })

    results.sort(
        key=lambda r: (
            r["cross_domain"],
            r["total_mentions"]
        ),
        reverse=True
    )

    return results[:top_n]