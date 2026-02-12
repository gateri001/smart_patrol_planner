# Smart Patrol Planner AI – Privacy & Data Governance Policy

## Purpose
This policy outlines how Smart Patrol Planner AI handles data to ensure compliance with Kenya’s Data Protection Act (DPA 2019), protect user privacy, and maintain ethical standards in public safety applications.

## Data Collection
- **Sources:** Officer reports, citizen reports, and bulk historical datasets.
- **Synthetic Data:** For demo purposes, anonymized synthetic datasets (200+ records) are used. No real personal identifiers are stored.

## Data Anonymization
- All datasets are stripped of personal identifiers (names, IDs, phone numbers).
- Synthetic data is generated using tools like Python’s Faker library to simulate realistic but non‑identifiable records.
- Location data is generalized to avoid pinpointing individuals.

## Data Storage & Encryption
- Credentials are stored using secure hashing (e.g., bcrypt).
- Database connections use encryption protocols (TLS/SSL).
- Incident records are anonymized before ingestion and stored in encrypted form.

## Access Control
- Role‑based authentication ensures only authorized personnel can access sensitive data.
- Audit logs track all login attempts and data submissions.

## Bias & Fairness
- Basic bias testing scripts check for regional imbalances in datasets.
- Reports highlight skew (e.g., overrepresentation of urban vs. rural incidents).
- Findings are documented to guide ethical improvements.

## Compliance
- Adheres to Kenya’s Data Protection Act (DPA 2019).
- Aligns with institutional ethics frameworks for Innovation Week and hackathon participation.
- Documentation of anonymization, encryption, and fairness testing is maintained in the repository.

## Transparency
- All code, datasets, and documentation are version‑controlled on GitHub.
- Active commits demonstrate ongoing development and accountability.
- Judges and collaborators can trace deliverables directly to this policy.

---
