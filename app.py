"""
app.py

FastAPI Backend for Mine Safety AI
"""

from pathlib import Path
import shutil
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.services import MineSafetyPipeline
from threading import Thread
from uuid import uuid4
from fastapi.responses import FileResponse
from backend.exports.report_generator import ReportGenerator
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.multi_camera_manager import MultiCameraManager
from backend.live_camera import LiveCamera
from backend.admin_reset import AdminResetService
from backend.auth_routes import router as auth_router
# ----------------------------------------------------
# FastAPI
# ----------------------------------------------------
class CameraRequest(BaseModel):

    source: str | int = 0
app = FastAPI(
    title="Mine Safety AI API",
    description="AI Powered Mine Safety Monitoring System",
    version="2.0.0"
)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Pipeline
# ----------------------------------------------------

pipeline = MineSafetyPipeline()
live_camera = LiveCamera()
multi_camera = MultiCameraManager()
report_generator = ReportGenerator()
admin_reset = AdminResetService(

    logger=pipeline.logger,

    live_camera=live_camera,

    multi_camera=multi_camera

)
# ===========================================
# Background Video Jobs
# ===========================================

video_jobs = {}
def process_video_job(job_id, input_path, output_path):

    try:

        result = pipeline.process_video(

            input_path,

            output_path,

            job_id,

            video_jobs

        )

        video_jobs[job_id]["status"] = "completed"

        video_jobs[job_id]["progress"] = 100

        video_jobs[job_id]["result"] = result

    except Exception as e:

        video_jobs[job_id]["status"] = "failed"

        video_jobs[job_id]["error"] = str(e)
# ----------------------------------------------------
# Directories
# ----------------------------------------------------

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_IMAGE_DIR = Path("outputs/images")
OUTPUT_VIDEO_DIR = Path("outputs/videos")

OUTPUT_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)


app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)
# ----------------------------------------------------
# Home
# ----------------------------------------------------

@app.get("/")
def home():

    return {

        "project": "Mine Safety AI",

        "version": "2.0.0",

        "status": "Running"

    }

# ----------------------------------------------------
# Health
# ----------------------------------------------------

@app.get("/health")
def health():

    return {

        "status": "healthy"

    }

# ----------------------------------------------------
# Upload Image
# ----------------------------------------------------

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    return {

        "message": "Image uploaded successfully",

        "path": str(filepath)

    }

# ----------------------------------------------------
# Detect Image
# ----------------------------------------------------

@app.post("/detect-image")
async def detect_image(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    output_path = OUTPUT_IMAGE_DIR / file.filename

    result = pipeline.process_image(

        str(filepath),

        str(output_path)

    )
    return {

        "status": "success",

        "workers_detected": len(result["workers"]),

        "ppe_objects": len(result["detections"]),

        "violations": len(result["alerts"]),

        "reports": result["reports"],

        "alerts": result["alerts"],

        "statistics": result["statistics"],

        "output_image": str(output_path)

    }

# ----------------------------------------------------
# Upload Video
# ----------------------------------------------------

@app.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    return {

        "message": "Video uploaded successfully",

        "path": str(filepath)

    }

# ----------------------------------------------------
# Detect Video
# ----------------------------------------------------

@app.post("/detect-video")

async def detect_video(file: UploadFile = File(...)):

    filepath = UPLOAD_DIR / file.filename

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    output_path = OUTPUT_VIDEO_DIR / file.filename

    job_id = str(uuid4())

    video_jobs[job_id] = {

        "status": "processing",

        "progress": 0,

        "frame": 0,

        "total_frames": 0,

        "workers": 0,

        "violations": 0,

        "processing_fps": 0,

        "eta": 0,

        "result": None

    }

    Thread(

        target=process_video_job,

        args=(

            job_id,

            str(filepath),

            str(output_path)

        ),

        daemon=True

    ).start()

    return {

        "status": "accepted",

        "job_id": job_id

    }

# ----------------------------------------------------
# Alerts
# ----------------------------------------------------
@app.get("/alerts")
def get_alerts():

    alerts = pipeline.logger.fetch_recent()

    return {

        "status": "success",

        "count": len(alerts),

        "alerts": alerts

    }


# ----------------------------------------------------
# Events
# ----------------------------------------------------

@app.get("/events")
def get_events():

    events = pipeline.logger.fetch_all()

    return {

        "status": "success",

        "count": len(events),

        "events": events

    }

# ----------------------------------------------------
# Statistics
# ----------------------------------------------------
@app.get("/statistics")
def statistics():

    logger = pipeline.logger

    return {

        "status": "success",

        "total_events": logger.total_events(),

        "total_workers": logger.total_workers(),

        "total_violations": logger.total_violations(),

        "high_alerts": logger.high_alerts(),

        "medium_alerts": logger.medium_alerts(),

        "low_alerts": logger.low_alerts()

    }

# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

@app.get("/dashboard")
def dashboard():

    logger = pipeline.logger

    return {

        "status": "success",

        "statistics":{

    "total_workers": logger.total_workers(),

    "total_violations": logger.total_violations(),

    "high_alerts": logger.high_alerts(),

    "medium_alerts": logger.medium_alerts(),

    "fire_alerts": logger.fire_alerts(),

    "smoke_alerts": logger.smoke_alerts(),

    "critical_alerts": logger.critical_alerts()

},

        "compliance": logger.compliance_statistics(),

        "recent_events": [

            dict(row)

            for row in logger.recent_events()

        ],

        "recent_alerts": [

            dict(row)

            for row in logger.fetch_recent()

        ]

    }
# ==========================================================
# Export CSV Report
# ==========================================================

@app.get("/export/csv")
def export_csv():

    logger = pipeline.logger

    events = logger.fetch_all()

    file_path = report_generator.export_csv(events)

    return FileResponse(

        path=file_path,

        filename="Mine_Safety_Report.csv",

        media_type="text/csv"

    )
@app.get("/export/excel")
def export_excel():

    logger = pipeline.logger

    events = logger.fetch_all()

    file_path = report_generator.export_excel(events)

    return FileResponse(

        path=file_path,

        filename="Mine_Safety_Report.xlsx",

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
@app.get("/export/pdf")
def export_pdf():

    logger = pipeline.logger

    events = logger.fetch_all()

    file_path = report_generator.export_pdf(events)

    return FileResponse(

        path=file_path,

        filename="Mine_Safety_Report.pdf",

        media_type="application/pdf"

    )
@app.post("/camera/start")
def start_camera(request: CameraRequest):

    source = request.source

    try:

        if isinstance(source, str):

            if source.isdigit():

                source = int(source)

    except:

        pass

    success = live_camera.start(source)

    if success:

        return {

            "status": "started",

            "source": source

        }

    return {

        "status": "failed",

        "message": "Unable to open camera."

    }
@app.post("/camera/stop")
def stop_camera():

    live_camera.stop()

    return {

        "status": "stopped"

    }
@app.get("/camera/status")
def camera_status():

    return live_camera.status()
@app.get("/alerts/live")
def live_alerts():

    return {

        "alerts":

        live_camera.get_live_alerts()

    }
@app.get("/camera/stream")
def camera_stream():

    return StreamingResponse(

        live_camera.mjpeg_generator(),

        media_type="multipart/x-mixed-replace; boundary=frame"

    )
# ----------------------------------------------------
# Recent Events
# ----------------------------------------------------

@app.get("/recent-events")
def recent_events():

    return {

        "status": "success",

        "events": pipeline.logger.recent_events()

    }
    
@app.get("/video-status/{job_id}")

def video_status(job_id):

    if job_id not in video_jobs:

        return {

            "status": "invalid_job"

        }

    return video_jobs[job_id]
@app.post("/cameras/add")
def add_camera(request: CameraRequest):

    camera_id = multi_camera.add_camera(request.source)

    if camera_id is None:

        return {

            "status": "failed",

            "message": "Unable to open camera."

        }

    return {

        "status": "success",

        "camera_id": camera_id

    }
@app.delete("/cameras/{camera_id}")
def remove_camera(camera_id: str):

    ok = multi_camera.remove_camera(camera_id)

    return {

        "status":

            "success"

            if ok

            else

            "failed"

    }
@app.get("/cameras")
def list_cameras():

    return {

        "total_cameras":

            multi_camera.total_cameras(),

        "total_workers":

            multi_camera.total_workers(),

        "total_violations":

            multi_camera.total_violations(),

        "cameras":

            multi_camera.list_cameras()

    }
@app.get("/camera/{camera_id}/status")
def camera_status(camera_id: str):

    camera = multi_camera.get_camera(camera_id)

    if camera is None:

        return {

            "status": "Camera Not Found"

        }

    return camera.status()
@app.get("/camera/{camera_id}/stream")
def camera_stream(camera_id: str):

    camera = multi_camera.get_camera(camera_id)

    if camera is None:

        return {

            "status": "Camera Not Found"

        }

    return StreamingResponse(

        camera.mjpeg_generator(),

        media_type="multipart/x-mixed-replace; boundary=frame"

    )
@app.post("/cameras/stop_all")
def stop_all():

    multi_camera.stop_all()

    return {

        "status": "success"

    }
# ==========================================================
# ADMIN RESET
# ==========================================================

@app.post("/admin/reset")
def reset_dashboard():

    return admin_reset.reset()

# ----------------------------------------------------
# Shutdown
# ----------------------------------------------------

@app.on_event("shutdown")
def shutdown():

    pipeline.logger.close()