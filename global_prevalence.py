import re


GLOBAL_PREVALENCE_ESTIMATES = (
    {
        "condition": "Untreated caries in permanent teeth",
        "people_affected_billions": 2.0,
        "estimate": "About 2.0 billion people",
        "source": "WHO Global oral health status report (2022)",
        "url": "https://www.who.int/publications/i/item/9789240061484",
        "keywords": ("caries", "tooth decay", "cavity", "cavities"),
    },
    {
        "condition": "Untreated caries in primary teeth",
        "people_affected_billions": 0.514,
        "estimate": "About 514 million children",
        "source": "WHO Global oral health status report (2022)",
        "url": "https://www.who.int/publications/i/item/9789240061484",
        "keywords": ("caries", "tooth decay", "cavity", "cavities"),
    },
    {
        "condition": "Severe periodontal disease",
        "people_affected_billions": 1.0,
        "estimate": "More than 1.0 billion cases",
        "source": "WHO Oral health fact sheet",
        "url": "https://www.who.int/news-room/fact-sheets/detail/oral-health",
        "keywords": ("periodontitis", "severe periodontal disease"),
    },
)


def get_global_prevalence_estimates(analysis_text):
    """Return WHO estimates related to possible explanations in an AI report."""
    possible_explanations = re.search(
        r"(?is)###\s*3\.\s*Possible explanations(.*?)(?=###\s*4\.|$)",
        analysis_text,
    )

    if possible_explanations is None:
        return list(GLOBAL_PREVALENCE_ESTIMATES), []

    explanation_text = possible_explanations.group(1).lower()
    matched_conditions = []
    matching_estimates = []

    for estimate in GLOBAL_PREVALENCE_ESTIMATES:
        if any(keyword in explanation_text for keyword in estimate["keywords"]):
            matching_estimates.append(estimate)
            if estimate["condition"] not in matched_conditions:
                matched_conditions.append(estimate["condition"])

    if matching_estimates:
        return matching_estimates, matched_conditions

    return list(GLOBAL_PREVALENCE_ESTIMATES), []
