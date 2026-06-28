"""
services.py

Mine Safety AI Pipeline

Image / Video
      │
      ▼
YOLO Detection
      │
      ▼
Worker Tracking
      │
      ▼
PPE Compliance
      │
      ▼
Alert Generation
      │
      ▼
SQLite Logging
"""

from pathlib import Path

import cv2
import subprocess
from detection.ppe_detector import PPEDetector
from detection.tracker import WorkerTracker
from detection.compliance_checker import PPEComplianceChecker
from detection.alert_engine import AlertEngine
from backend.detectors.fire_alert_engine import FireAlertEngine
from database.event_logger import EventLogger
from backend.detectors.fire_smoke_detector import FireSmokeDetector


class MineSafetyPipeline:

    def __init__(self):

        # ------------------------------------
        # AI Modules
        # ------------------------------------

        self.detector = PPEDetector()
        
        self.fire_detector = FireSmokeDetector()

        self.tracker = WorkerTracker()

        self.compliance = PPEComplianceChecker()

        self.alert_engine = AlertEngine()
        self.fire_alert_engine = FireAlertEngine()
        self.logger = EventLogger()

    # ==========================================================
    # Dashboard Statistics
    # ==========================================================

    def calculate_statistics(self, reports):

        """
        Calculate PPE compliance statistics
        from the current frame / image / video.
        """

        total_workers = len(reports)

        if total_workers == 0:

            return {

                "total_workers": 0,

                "safe_workers": 0,

                "workers_with_violations": 0,

                "helmet_compliance": 0,

                "vest_compliance": 0,

                "gloves_compliance": 0,

                "boots_compliance": 0,

                "goggles_compliance": 0

            }

        safe_workers = sum(

            1

            for report in reports

            if report["status"] == "SAFE"

        )

        workers_with_violations = (

            total_workers -

            safe_workers

        )

        helmet_count = sum(

            int(report["helmet"])

            for report in reports

        )

        vest_count = sum(

            int(report["vest"])

            for report in reports

        )

        gloves_count = sum(

            int(report["gloves"])

            for report in reports

        )

        boots_count = sum(

            int(report["boots"])

            for report in reports

        )

        goggles_count = sum(

            int(report["goggles"])

            for report in reports

        )

        return {

            "total_workers": total_workers,

            "safe_workers": safe_workers,

            "workers_with_violations": workers_with_violations,

            "helmet_compliance": round(

                helmet_count / total_workers * 100,

                2

            ),

            "vest_compliance": round(

                vest_count / total_workers * 100,

                2

            ),

            "gloves_compliance": round(

                gloves_count / total_workers * 100,

                2

            ),

            "boots_compliance": round(

                boots_count / total_workers * 100,

                2

            ),

            "goggles_compliance": round(

                goggles_count / total_workers * 100,

                2

            )

        }
    def convert_to_h264(self, input_video, output_video):
        ffmpeg_path = r"D:\Downloads\ffmpeg\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
        command = [

        ffmpeg_path,

        "-y",

        "-i", str(input_video),

        "-c:v", "libx264",

        "-preset", "fast",

        "-crf", "23",

        "-pix_fmt", "yuv420p",

        "-movflags", "+faststart",

        "-an",

        str(output_video)

    ]
        print("Running FFmpeg...")
        subprocess.run(

        command,

        check=True

    )

    print("FFmpeg Conversion Completed.")
    # ==========================================================
    # Frame Processing
    def run_fire_smoke_detection(self, frame):
        try:
            detections = self.fire_detector.detect(frame)
        except Exception as e:
            print(f"[Fire Detector] {e}")
            detections = []
        fire_found = False
        smoke_found = False
        for detection in detections:
            label = detection["class_name"].lower()
            if label == "fire":
                fire_found = True
            elif label == "smoke":
                smoke_found = True
        return {

        "detections": detections,

        "fire_found": fire_found,

        "smoke_found": smoke_found

    }
    def draw_fire_smoke(
        self,
        annotated_frame,

    fire_detections

):
        for detection in fire_detections:
            x1, y1, x2, y2 = detection["bbox"]
            label = detection["class_name"].upper()
            confidence = detection["confidence"]
            if label == "FIRE":
                color = (0, 0, 255)
            elif label == "SMOKE":
                color = (0, 165, 255)
            else:
                color = (255, 255, 255)
            cv2.rectangle(

            annotated_frame,

            (x1, y1),

            (x2, y2),

            color,

            3

        )
            cv2.putText(

            annotated_frame,

            f"{label} {confidence:.2f}",

            (x1, y1 - 10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            color,

            2

        )
        return annotated_frame
    def draw_warning_banner(
        self,

    annotated_frame,

    fire_found,

    smoke_found

):
        banner_color = None
        banner_text = ""
        if fire_found:
            banner_color = (0, 0, 255)
            banner_text = "FIRE DETECTED - EVACUATE IMMEDIATELY"
        elif smoke_found:
            banner_color = (0, 165, 255)
            banner_text = "SMOKE DETECTED"
        if banner_color is None:
            return annotated_frame
        cv2.rectangle(

        annotated_frame,

        (0, 0),

        (annotated_frame.shape[1], 60),

        banner_color,

        -1

    )
        cv2.putText(

        annotated_frame,

        banner_text,

        (25, 40),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        (255, 255, 255),

        3

    )
        return annotated_frame
    
    def generate_all_alerts(

    self,

    reports,

    fire_detections

):
        ppe_alerts = self.alert_engine.generate_alerts(

        reports

    )
        fire_alerts = self.fire_alert_engine.generate_alerts(

        fire_detections

    )
        return {

        "ppe": ppe_alerts,

        "fire": fire_alerts,

        "all": ppe_alerts + fire_alerts

    }
    def save_all_alerts(

    self,

    alerts

):
        if alerts["ppe"]:
            self.logger.log_events(

            alerts["ppe"]

        )
            if alerts["fire"]:
                self.logger.log_events(

            alerts["fire"]

        )
    # ==========================================================
    def process_frame(self, frame):
        results = self.detector.model.track(

            source=frame,

            persist=True,

            tracker="bytetrack.yaml",

            conf=self.detector.conf,

            imgsz=self.detector.imgsz,

            verbose=False

        )

        result = results[0]

        annotated_frame = result.plot()
        
        # ------------------------------------------
        fire_result = self.run_fire_smoke_detection(

    frame

)
        fire_detections = fire_result["detections"]
        fire_found = fire_result["fire_found"]
        smoke_found = fire_result["smoke_found"]
        
        annotated_frame = self.draw_fire_smoke(

    annotated_frame,

    fire_detections

)
        annotated_frame = self.draw_warning_banner(

    annotated_frame,

    fire_found,

    smoke_found

)

        # ------------------------------------------
        # Extract detections
        # ------------------------------------------

        detections = []

        if result.boxes is not None:

            for box in result.boxes:

                cls = int(box.cls.item())

                detections.append({

                    "class_id": cls,

                    "class_name": result.names[cls],

                    "confidence": float(box.conf.item()),

                    "bbox": [

                        int(v)

                        for v in box.xyxy[0].tolist()

                    ]

                })

        # ------------------------------------------
        # Extract Workers
        # ------------------------------------------

        workers = self.tracker.extract_workers(

            result

        )

        # ------------------------------------------
        # PPE Compliance
        # ------------------------------------------

        reports = self.compliance.check(

            workers,

            detections

        )

        # ------------------------------------------
        # Statistics
        # ------------------------------------------

        statistics = self.calculate_statistics(

            reports

        )

        # ------------------------------------------
        # Generate Alerts
        # ------------------------------------------

        alerts = self.generate_all_alerts(

    reports,

    fire_detections

)
        self.save_all_alerts(

    alerts

)

        # ------------------------------------------
        # Return everything
        # ------------------------------------------

        return {

            "annotated_frame": annotated_frame,

            "workers": workers,

            "detections": detections,
            
            "fire_detections": fire_detections,

            "reports": reports,

            "alerts": alerts["all"],

"ppe_alerts": alerts["ppe"],

"fire_alerts": alerts["fire"],

            "statistics": statistics

        }

    # ==========================================================
    # Image Processing
    # ==========================================================
        # ==========================================================
    # Image Processing
    # ==========================================================

    def process_image(self, image_path, output_path=None):

        """
        Process a single image.

        Parameters
        ----------
        image_path : str
            Input image path

        output_path : str
            Annotated image save path

        Returns
        -------
        dict
        """

        frame = cv2.imread(image_path)

        if frame is None:

            raise RuntimeError(

                f"Unable to read image: {image_path}"

            )

        result = self.process_frame(

            frame

        )

        # -----------------------------------------
        # Save annotated image
        # -----------------------------------------

        if output_path:

            output_path = Path(output_path)

            output_path.parent.mkdir(

                parents=True,

                exist_ok=True

            )

            cv2.imwrite(

                str(output_path),

                result["annotated_frame"]

            )

        # -----------------------------------------
        # Return Image Results
        # -----------------------------------------

        return {

            "workers": result["workers"],

            "detections": result["detections"],

            "reports": result["reports"],

            "alerts": result["alerts"],

            "statistics": result["statistics"],

            "annotated_frame": result["annotated_frame"],

            "output_image": str(output_path) if output_path else None

        }

    # ==========================================================
    # Video Processing
    # ==========================================================
        # ==========================================================
    # Video Processing
    # ==========================================================

    def process_video(

    self,

    video_path,

    output_path,

    job_id=None,

    video_jobs=None

):

        """
        Process an entire video.
        """

        cap = cv2.VideoCapture(video_path)
        import time
        start_time = time.time()

        if not cap.isOpened():

            raise RuntimeError(

                f"Unable to open video: {video_path}"

            )

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(width, height)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("FPS:", fps)

        Path(output_path).parent.mkdir(

            parents=True,

            exist_ok=True

        )
        if fps <= 0 or fps != fps:
            fps = 30
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        temp_video = Path(output_path).with_suffix(".avi")
        writer = cv2.VideoWriter(

    str(temp_video),

    cv2.VideoWriter_fourcc(*"XVID"),

    fps,

    (width, height)

)
        print("Writer opened:", writer.isOpened())
        

        total_frames = int(
            cap.get(

        cv2.CAP_PROP_FRAME_COUNT

    )

)
        processed_frames = 0

        total_alerts = 0

        worker_summary = {}

        while True:

            ret, frame = cap.read()

            if not ret:

                break

            result = self.process_frame(

                frame

            )

            writer.write(

                result["annotated_frame"]

            )
            processed_frames += 1
            elapsed = time.time() - start_time
            fps_processing = (
                processed_frames / elapsed
                if elapsed > 0
                else 0

)
            progress = int(
                processed_frames /
                total_frames *100

)
            eta = (
                total_frames -
                processed_frames

) / fps_processing if fps_processing > 0 else 0
            if job_id and video_jobs:
                video_jobs[job_id].update(

        {

            "status": "processing",

            "progress": progress,

            "frame": processed_frames,

            "total_frames": total_frames,

            "workers": len(result["reports"]),

            "violations": total_alerts,

            "processing_fps": round(

                fps_processing,

                2

            ),

            "eta": round(

                eta,

                1

            )

        }

    )
                total_alerts += len(

                result["alerts"]

            )

            for report in result["reports"]:

                worker_id = report["worker_id"]

                if worker_id not in worker_summary:

                    worker_summary[worker_id] = report.copy()

                else:

                    existing = worker_summary[worker_id]

                    existing["helmet"] |= report["helmet"]

                    existing["vest"] |= report["vest"]

                    existing["gloves"] |= report["gloves"]

                    existing["boots"] |= report["boots"]

                    existing["goggles"] |= report["goggles"]

                    existing["violations"] = list(

                        set(

                            existing["violations"]

                            +

                            report["violations"]

                        )

                    )

                    existing["status"] = (

                        "SAFE"

                        if len(existing["violations"]) == 0

                        else "VIOLATION"

                    )

        writer.release()
        cap.release()
        print("Converting AVI to H264 MP4...")
        self.convert_to_h264(

    temp_video,

    output_path

)
        if temp_video.exists():
            temp_video.unlink()
            print("Finished.")

        unique_reports = list(

            worker_summary.values()

        )

        statistics = self.calculate_statistics(

            unique_reports

        )

        statistics["total_unique_workers"] = len(

            unique_reports

        )
        return {

    "status": "success",

    "frames_processed": total_frames,

    "workers_detected": len(unique_reports),

    "alerts_generated": total_alerts,

    "output_video": str(output_path),

    "statistics": statistics,

    "reports": unique_reports,

    "alerts": [

        alert

        for report in unique_reports

        if report["status"] == "VIOLATION"

        for alert in self.alert_engine.generate_alerts([report])

    ]

}