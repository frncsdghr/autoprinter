import time
import os
import win32print
import win32ui
from PIL import Image, ImageWin
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            # Get the file extension
            _, ext = os.path.splitext(event.src_path)
            # Check if the file is an image
            if ext.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}:
                print(f'Printing image: {os.path.basename(event.src_path)}')
                time.sleep(1)  # Wait a moment before trying to print
                self.print_image(event.src_path)

    def print_image(self, image_path):
        try:
            # Check if the file exists
            if not os.path.isfile(image_path):
                print(f'File not found: {image_path}')
                return

            # Open the image
            img = Image.open(image_path)

            # Convert the image to RGB mode if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            printer_name = win32print.GetDefaultPrinter()  # Get the default printer

            # Create a printer device context
            hdc = win32ui.CreateDC()
            hdc.CreatePrinterDC(printer_name)

            # Set the size of the image
            width, height = img.size
            hdc.StartDoc(image_path)
            hdc.StartPage()

            # Convert the image to a bitmap
            dib = ImageWin.Dib(img)
            dib.draw(hdc.GetHandleOutput(), (0, 0, width, height))

            hdc.EndPage()
            hdc.EndDoc()
            hdc.DeleteDC()
            print('Image sent to printer successfully.')

        except Exception as e:
            print(f'Error printing image: {e}')

def monitor_folder(folder_path):
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)

    observer.start()
    print(f'Monitoring folder: {folder_path} for new images...')

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Change this to the folder you want to monitor
    folder_to_monitor = "C:\\qrcodes"
    monitor_folder(folder_to_monitor)
