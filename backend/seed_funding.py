from app.db.database import SessionLocal
from app.models.funding import FundingOpportunity

db = SessionLocal()

funding_data = [
    FundingOpportunity(
        title="AI Research Grant",
        source="Government Research Council",
        description="Funding support for artificial intelligence and machine learning research.",
        eligibility="Researchers, students, university teams, and Researcher",
        domains="Artificial Intelligence, Machine Learning",
        deadline="30 Aug 2026",
        amount="Up to Rs. 5,00,000",
        link="https://www.grants.gov/"
    ),

    FundingOpportunity(
        title="Research Analytics Innovation Grant",
        source="Innovation Fund",
        description="Support for research analytics, data science, and evidence-based innovation projects.",
        eligibility="Researchers, students, university teams, and Researcher",
        domains="Research Analytics, Data Science, Innovation",
        deadline="15 Sep 2026",
        amount="Up to Rs. 7,00,000",
        link="https://www.grants.gov/"
    ),

    FundingOpportunity(
        title="University Innovation Grant",
        source="University Innovation Cell",
        description="Funding for university research projects and innovation initiatives.",
        eligibility="Students, researchers, university teams, and Researcher",
        domains="Innovation, Research Analytics",
        deadline="05 Oct 2026",
        amount="Up to Rs. 3,00,000",
        link="https://www.grants.gov/"
    ),

    FundingOpportunity(
        title="AI and Innovation Fellowship",
        source="Innovation Research Agency",
        description="Research support for early-stage artificial intelligence and innovation projects.",
        eligibility="Researchers, students, and Researcher",
        domains="Artificial Intelligence, Innovation",
        deadline="22 Oct 2026",
        amount="Mentorship + research support",
        link="https://www.grants.gov/"
    ),
]

try:
    existing = db.query(FundingOpportunity).count()

    if existing == 0:
        db.add_all(funding_data)
        db.commit()
        print("Funding data added successfully!")
    else:
        print(f"Funding data already exists: {existing} records.")

finally:
    db.close()