import numpy as np
##from multiprocessing import shared_memory
from PySide6.QtCore import QBuffer, QIODeviceBase, Slot, QSharedMemory, QDataStream, qVersion
import sys
from PySide6.QtWidgets import QApplication
# from dialog import Dialog


if __name__ == "__main__":
    application = QApplication()
    # dialog = Dialog()
    # dialog.show()
    sys.exit(application.exec())

    
_shared_memory = QSharedMemory("nbodyState")

# shm_a = shared_memory.SharedMemory("nbodyState", create=True, size=10)

testData = np.array([[0.0,1.0 , 2, 3, 4, 5], [4,5, 6, 7, 8, 9], [10, 11, 12, 13, 2, 3]])

# buffer = shm_a.buf

# buffer[:4] = bytearray([22, 33, 44, 55])


def load_from_memory(data):
    if not _shared_memory.isAttached() and not _shared_memory.attach():
        print("Unable to attach to shared memory segment.\n"
                              "Load an image first.")
        return

    _shared_memory.lock()
    mv = memoryview(_shared_memory.constData())
    buffer = QBuffer()
    buffer.setData(mv.tobytes())
    buffer.open(QBuffer.ReadWrite)
    _out = QDataStream(buffer)
    image = QImage()
    buffer.close()


load_from_memory(testData)



# buffer = shm_a.buf
# >>> len(buffer)
# 10
# >>> buffer[:4] = bytearray([22, 33, 44, 55])  # Modify multiple at once
# >>> buffer[4] = 100                           # Modify single byte at a time
# >>> # Attach to an existing shared memory block
# >>> shm_b = shared_memory.SharedMemory(shm_a.name)
# >>> import array
# >>> array.array('b', shm_b.buf[:5])  # Copy the data into a new array.array
# array('b', [22, 33, 44, 55, 100])
# >>> shm_b.buf[:5] = b'howdy'  # Modify via shm_b using bytes
# >>> bytes(shm_a.buf[:5])      # Access via shm_a
# b'howdy'
# >>> shm_b.close()   # Close each SharedMemory instance
# >>> shm_a.close()