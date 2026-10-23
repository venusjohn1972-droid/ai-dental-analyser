import unittest

from global_prevalence import (
    GLOBAL_PREVALENCE_ESTIMATES,
    get_global_prevalence_estimates,
)


class GlobalPrevalenceTests(unittest.TestCase):
    def test_caries_explanation_returns_both_caries_estimates(self):
        estimates, matched = get_global_prevalence_estimates(
            "### 3. Possible explanations\n"
            "This could be associated with dental caries.\n"
            "### 4. What the image cannot determine\n"
            "A photograph cannot confirm caries."
        )

        self.assertEqual(len(estimates), 2)
        self.assertEqual(
            matched,
            [
                "Untreated caries in permanent teeth",
                "Untreated caries in primary teeth",
            ],
        )

    def test_periodontitis_explanation_returns_periodontal_estimate(self):
        estimates, matched = get_global_prevalence_estimates(
            "### 3. Possible explanations\n"
            "One possibility is periodontitis.\n"
            "### 4. What the image cannot determine\n"
            "A photograph cannot determine severity."
        )

        self.assertEqual(len(estimates), 1)
        self.assertEqual(
            estimates[0]["condition"],
            "Severe periodontal disease",
        )
        self.assertEqual(matched, ["Severe periodontal disease"])

    def test_unmatched_or_unstructured_report_returns_general_context(self):
        estimates, matched = get_global_prevalence_estimates(
            "### 3. Possible explanations\n"
            "Tooth sensitivity is a symptom, not a diagnosis."
        )

        self.assertEqual(estimates, list(GLOBAL_PREVALENCE_ESTIMATES))
        self.assertEqual(matched, [])

    def test_mentioned_condition_outside_possible_explanations_is_not_matched(self):
        estimates, matched = get_global_prevalence_estimates(
            "### 3. Possible explanations\n"
            "Sensitivity may have several causes.\n"
            "### 4. What the image cannot determine\n"
            "This does not confirm caries."
        )

        self.assertEqual(estimates, list(GLOBAL_PREVALENCE_ESTIMATES))
        self.assertEqual(matched, [])


if __name__ == "__main__":
    unittest.main()
