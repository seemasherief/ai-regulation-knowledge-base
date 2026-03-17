from bs4 import BeautifulSoup
import os

def load_document(filename):
    filepath = os.path.join("documents", filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    if filename.endswith(".html"):
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    return content

def load_all_documents():
    docs = {
        "EU AI Act": load_document("eu_ai_act.html"),
        "GDPR": load_document("gdpr.html"),
        "CCPA": load_document("ccpa.html"),
        "UK AI Framework": load_document("uk_ai_framework.html"),
        "UNESCO AI Ethics": load_document("unesco_ai_ethics.html"),
        "US Executive Order on AI": load_document("us_executive_order_ai.html"),
    }
    return docs