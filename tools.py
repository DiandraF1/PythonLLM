
import json


def load_summaries(path="data/book_summaries.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_summary_by_title(title: str) -> str:
    summaries = load_summaries()
    summary = summaries.get(title)
    if summary:
        return summary
    return "Nu am găsit un rezumat pentru titlul dat."
