import numpy
import sys

class WaveLoader():
    riffHeader = {
        'chunkID': "",
        'chunkDataSize': 0,
        'riffTypeID': "",
        'fmtHeader': {
            'chunkID': "",
            'chunkDataSize': 0
        },
        'fmtData': {
            'audioFormat': 0,
            'channels': 0,
            'samplingRate': 0,
            'bytesPerSecond': 0,
            'blockAlign': 0,
            'bitsPerSample': 0,
            'extraBytes': 0,
            'extraFormatInfo': None
        },
        'dataHeader': {
            'chunkID': "",
            'chunkDataSize': 0
        }
    }

    audioData = []

    def loadWavefile(self, filePath):
        def readFormatData(byteArray):
            fmtData = {}
            fmtData['audioFormat'] = int.from_bytes(byteArray[:2], 'little')
            fmtData['channels'] = int.from_bytes(byteArray[2:4], 'little')
            fmtData['samplingRate'] = int.from_bytes(byteArray[4:8], 'little')
            fmtData['bytesPerSecond'] = int.from_bytes(byteArray[8:12], 'little')
            fmtData['blockAlign'] = int.from_bytes(byteArray[12:14], 'little')
            fmtData['bitsPerSample'] = int.from_bytes(byteArray[14:16], 'little')
            fmtData['extraBytes'] = int.from_bytes(byteArray[16:18], 'little')
            if (fmtData['extraBytes'] > 0):
                fmtData['extraFormatInfo'] = readExtraFormatInfo(fmtData['extraBytes'], byteArray[18:])

            return fmtData

        def readExtraFormatInfo(length, byteArray):
            return {}

        def readHeader(binaryFile):
            self.riffHeader['chunkID'] = bytes(binaryFile.read(4)).decode('ASCII')
            self.riffHeader['chunkDataSize'] = int.from_bytes(binaryFile.read(4), 'little')
            self.riffHeader['riffTypeID'] = bytes(binaryFile.read(4)).decode('ASCII')
            self.riffHeader['fmtHeader']['chunkID'] = bytes(binaryFile.read(4)).decode('ASCII')
            self.riffHeader['fmtHeader']['chunkDataSize'] = int.from_bytes(binaryFile.read(4), 'little')
            self.riffHeader['fmtData'] = readFormatData(binaryFile.read(self.riffHeader['fmtHeader']['chunkDataSize']))
            self.riffHeader['dataHeader']['chunkID'] = bytes(binaryFile.read(4)).decode('ASCII')
            self.riffHeader['dataHeader']['chunkDataSize'] = int.from_bytes(binaryFile.read(4), 'little')

        with open(filePath, 'rb') as binaryFile:
            readHeader(binaryFile)

        

#### Debug

if __name__ == '__main__':
    wavePath = sys.argv[1]
    
    wavLoader = WaveLoader()
    wavLoader.loadWavefile(wavePath)
    print(wavLoader.riffHeader)

