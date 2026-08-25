from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine


# Create Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


# Indian Vehicle Registration / RC
rc_pattern = Pattern(
    name="indian_rc",
    regex=r"\b[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,3}\s?\d{1,4}\b",
    score=0.8,
)

rc_recognizer = PatternRecognizer(
    supported_entity="INDIAN_RC",
    patterns=[rc_pattern],
)


# Indian Driving Licence
dl_pattern = Pattern(
    name="indian_dl",
    regex=r"\b[A-Z]{2}[- ]?\d{4,6}[- ]?\d{5,10}\b",
    score=0.7,
)

dl_recognizer = PatternRecognizer(
    supported_entity="INDIAN_DL",
    patterns=[dl_pattern],
)


# VIN / Chassis number
vin_pattern = Pattern(
    name="vehicle_vin",
    regex=r"\b[A-HJ-NPR-Z0-9]{17}\b",
    score=0.85,
)

vin_recognizer = PatternRecognizer(
    supported_entity="VEHICLE_VIN",
    patterns=[vin_pattern],
)


# Register custom recognizers
analyzer.registry.add_recognizer(rc_recognizer)
analyzer.registry.add_recognizer(dl_recognizer)
analyzer.registry.add_recognizer(vin_recognizer)


def mask_pii(text: str) -> str:
    """
    Detect and anonymize Indian vehicle and personal identifiers.
    """

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
    )

    return anonymized_text.text