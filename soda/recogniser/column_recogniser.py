from typing import Optional, List

from presidio_analyzer import LocalRecognizer, RecognizerResult, EntityRecognizer, AnalysisExplanation
from presidio_analyzer.nlp_engine import NlpArtifacts
from soda.profiling.analyzer import Analyzer


class HobbiesRecognizer(LocalRecognizer):
    """Recognize titles like Mr, Mrs, Dr, etc.

    This recognizer identifies if a column contains titles based on predefined patterns and context words.
    :param context: Base context words for enhancing the assurance scores.
    :param supported_language: Language this recognizer supports.
    """

    SCORE = 0.3
    CONTEXT = ["hobbies", "interests", "passions"]
    TITLES = ["Poker", "Writing", "Dance", "Exercise", "Juggling", "Hunting", "Cycling",
              "Blogging", "Gardening", "Baking", "Handicraft", "Hiking", "Cooking",
              "Scuba Diving", "Painting", "Singing", "Photography", "Origami"]

    def __init__(
        self,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
    ):
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entities=self.get_supported_entities(),
            supported_language=supported_language,
            context=context,
        )

    def load(self) -> None:  # noqa D102
        pass

    def get_supported_entities(self):  # noqa D102
        return ["HOBBIES"]

    def analyze(
        self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:
        """Analyzes text to detect titles.

        Iterates over predefined titles and matches them against the text.
        :param text: Text to be analyzed
        :param entities: Entities this recognizer can detect
        :param nlp_artifacts: Additional metadata from the NLP engine
        :return: List of title RecognizerResults
        """
        results = []
        for title in self.TITLES:
            start_index = text.find(title)
            while start_index != -1:
                end_index = start_index + len(title)
                results.append(
                    RecognizerResult(
                        entity_type="HOBBIES",
                        start=start_index,
                        end=end_index,
                        score=self.SCORE,
                        analysis_explanation=self._get_analysis_explanation(title),
                        recognition_metadata={
                            RecognizerResult.RECOGNIZER_NAME_KEY: self.name,
                            RecognizerResult.RECOGNIZER_IDENTIFIER_KEY: self.id,
                        },
                    )
                )
                start_index = text.find(title, end_index)

        return EntityRecognizer.remove_duplicates(results)

    def _get_analysis_explanation(self, title):
        return AnalysisExplanation(
            recognizer=HobbiesRecognizer.__name__,
            original_score=self.SCORE,
            textual_explanation=f"Recognized as title '{title}' using TitleRecognizer",
        )


# Set Recognizer in analyzer
Analyzer.add_recognizer(HobbiesRecognizer())
