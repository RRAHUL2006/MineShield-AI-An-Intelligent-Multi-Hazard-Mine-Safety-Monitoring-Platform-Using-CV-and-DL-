"""
Detection Engine

Runs multiple AI detectors on the same frame.
"""

from detectors.ppe_detector import PPEDetector
from detectors.fire_smoke_detector import FireSmokeDetector


class DetectionEngine:

    def __init__(self):

        print("\n==============================")
        print(" Initializing Detection Engine")
        print("==============================")

        self.detectors = [

            PPEDetector(),

            FireSmokeDetector()

        ]

        print(
            f"Loaded {len(self.detectors)} detectors.\n"
        )

    # ---------------------------------------------------------

    def detect(self, frame):

        all_detections = []

        for detector in self.detectors:

            try:

                detections = detector.detect(frame)

                if detections:

                    all_detections.extend(detections)

            except Exception as e:

                print(

                    f"[ERROR] {detector.__class__.__name__}: {e}"

                )

        return all_detections

    # ---------------------------------------------------------

    def statistics(self, detections):

        stats = {

            "ppe": 0,

            "fire": 0,

            "smoke": 0,

            "total": len(detections)

        }

        for detection in detections:

            model = detection.get("model")

            event = detection.get(

                "event_type",

                ""

            ).upper()

            if model == "PPE":

                stats["ppe"] += 1

            elif event == "FIRE":

                stats["fire"] += 1

            elif event == "SMOKE":

                stats["smoke"] += 1

        return stats