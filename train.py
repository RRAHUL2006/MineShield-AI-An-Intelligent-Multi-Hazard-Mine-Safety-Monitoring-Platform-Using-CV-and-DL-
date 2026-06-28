from ultralytics import YOLO

def main():

    model = YOLO("models/ppe_detector/weights/last.pt")

    model.train(
        resume=True
    )

if __name__ == "__main__":
    main()