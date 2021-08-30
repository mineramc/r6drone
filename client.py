import io
import time
import picamera
import socket
from threading import Condition, Thread


class StreamingOutput:
    """Compiles buffered data from the Pi Camera into individual frames."""

    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, data):
        """
        Writes DATA to the buffer. Copies buffer contents to SELF.FRAME if received a new frame.
        :param data:    The data to write.
        :return:        Number of bytes written.
        """

        if data.startswith(b'\xff\xd8'):
            self.buffer.truncate()      # Truncates buffer to current stream position
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()     # Notify all threads that new data is available
            self.buffer.seek(0)
        return self.buffer.write(data)


class Client:
    """A client class for sending video data to the host computer and receiving commands."""

    HOST_ADDR = '10.0.0.210'
    PORT = 65432

    def __init__(self):
        self.connection = None
        self.output = StreamingOutput()
        self.receive_thread = Thread(target=self._receive)
        self.receive_thread.daemon = True

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Client.HOST_ADDR, Client.PORT))
            print(f'Connected to host at {Client.HOST_ADDR}')
            self.connection = s

            # self.receive_thread.start()
            self._send()

    def _send(self):
        """
        Constantly sends image data to the host.
        :return:    None
        """

        with self.connection:
            with picamera.PiCamera(resolution='640x480', framerate=60) as camera:
                print('Initialized PiCamera')
                camera.start_recording(self.output, format='mjpeg')
                try:
                    print('Starting send loop')
                    while True:
                        with self.output.condition:
                            # self.output.condition.wait()
                            frame = self.output.frame
                            if frame:
                                result = bytearray(len(frame).to_bytes(16, 'big'))
                                result.extend(frame)
                                self.connection.sendall(frame)
                finally:
                    camera.close()

    def _receive(self):
        """
        Receives commands from the host.
        :return:    None
        """

        with self.connection:
            print('Starting receive loop')
            while True:
                time.sleep(0.1)


client = Client()
client.start()
