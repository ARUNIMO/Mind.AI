import asyncio
import traceback
from graph import graph
from utilities import download_file, print_emotions
from hume import HumeStreamClient
from hume.models.config import FaceConfig
import cv2
import time
filepath =("output.mp4")
def video1(duration=5):
    async def main():
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

        start_time = time.time()
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()
        try:
            client = HumeStreamClient("bAGjOIeqrGTIKYPg4NANLO9Im5x5EmdqlQDJFdrlSigVrUif")
            # Enable face identification to track unique faces over the streaming session
            config = FaceConfig(identify_faces=True)
            async with client.connect([config]) as socket:
                result = await socket.send_file(filepath)
            emotions = result["face"]["predictions"][0]["emotions"]
            emotion=print_emotions(emotions)
            graph()
        except Exception:
         print(traceback.format_exc())
    # When running the streaming API outside of a Jupyter notebook you do not need these lines.
    # Jupyter has its own async event loop, so this merges main into the Jupyter event loop.
    # To run this sample in a script with asyncio you can use `asyncio.run(main())`
    # loop = asyncio.get_event_loop()
    # loop.create_task(main())
    asyncio.run(main())