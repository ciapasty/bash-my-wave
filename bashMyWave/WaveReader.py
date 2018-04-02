import math
import os

# DEBUG
import sys


class WaveReader():
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

    name = ""
    length = 0

    def loadWavefile(self, filePath):
        def readASCIItext(binaryFile, nBytes):
            return bytes(binaryFile.read(nBytes)).decode('ASCII')

        def readInt(binaryFile, nBytes, endian, signed):
            return int.from_bytes(
                binaryFile.read(nBytes),
                endian,
                signed=signed
                )

        def readHeader(binaryFile):
            self.riffHeader['chunkID'] = readASCIItext(binaryFile, 4)
            self.riffHeader['chunkDataSize'] = readInt(
                binaryFile, 4, 'little', False
                )
            self.riffHeader['riffTypeID'] = readASCIItext(binaryFile, 4)
            self.riffHeader['fmtHeader']['chunkID'] = readASCIItext(
                binaryFile, 4
                )
            self.riffHeader['fmtHeader']['chunkDataSize'] = readInt(
                binaryFile, 4, 'little', False
                )
            self.riffHeader['fmtData'] = readFormatData(
                self.riffHeader['fmtHeader']['chunkDataSize'],
                binaryFile
                )
            # BWF support
            chunkID = bytes(binaryFile.read(4)).decode('ASCII')
            chunkDataSize = int.from_bytes(binaryFile.read(4), 'little')
            while (chunkID != 'data'):
                self.riffHeader[chunkID+'Header'] = {
                    'chunkID': chunkID,
                    'chunkDataSize': chunkDataSize,
                    # Temporary support for BWF and other Chunks
                    chunkID+'Data': {}
                }
                binaryFile.read(chunkDataSize)
                chunkID = bytes(binaryFile.read(4)).decode('ASCII')
                chunkDataSize = int.from_bytes(binaryFile.read(4), 'little')

            self.riffHeader['dataHeader']['chunkID'] = chunkID
            self.riffHeader['dataHeader']['chunkDataSize'] = chunkDataSize

        def readFormatData(lenght, binaryFile):
            fmtData = {}
            fmtData['audioFormat'] = readInt(binaryFile, 2, 'little', False)
            fmtData['channels'] = readInt(binaryFile, 2, 'little', False)
            fmtData['samplingRate'] = readInt(binaryFile, 4, 'little', False)
            fmtData['bytesPerSecond'] = readInt(binaryFile, 4, 'little', False)
            fmtData['blockAlign'] = readInt(binaryFile, 2, 'little', False)
            fmtData['bitsPerSample'] = readInt(binaryFile, 2, 'little', False)
            fmtData['extraBytes'] = readInt(binaryFile, 2, 'little', False)
            if (fmtData['extraBytes'] > 0):
                fmtData['extraFormatInfo'] = readExtraFormatInfo(
                    fmtData['extraBytes'],
                    binaryFile.read(fmtData['extraBytes'])
                    )

            return fmtData

        def readExtraFormatInfo(length, byteArray):
            return {}

        def normalizeSample(sample, bitRate):
            maxValue = 0
            if (bitRate == 8):
                maxValue = 128
            if (bitRate == 16):
                maxValue = 32768
            if (bitRate == 24):
                maxValue = 8388608

            return sample/maxValue

        def mapChannels(binaryFile, audioChannels, bytesPerChannel):
            return [normalizeSample(
                        readInt(binaryFile, bytesPerChannel, 'little', True),
                        self.riffHeader['fmtData']['bitsPerSample']
                        ) for i in range(audioChannels)]

        def readAudioData(binaryFile):
            audioChannels = self.riffHeader['fmtData']['channels']
            audioChunkBytes = self.riffHeader['dataHeader']['chunkDataSize']
            bytesPerChannel = int(
                self.riffHeader['fmtData']['blockAlign']/audioChannels
                )
            audioSamples = int(
                audioChunkBytes/self.riffHeader['fmtData']['blockAlign']
                )

            if (audioChannels == 1):
                self.audioData = [
                    normalizeSample(
                        readInt(binaryFile, bytesPerChannel, 'little', True),
                        self.riffHeader['fmtData']['bitsPerSample']
                        ) for x in range(audioSamples)]
            else:
                self.audioData = [
                    mapChannels(
                        binaryFile,
                        audioChannels,
                        bytesPerChannel
                        ) for x in range(audioSamples)
                    ]

        with open(filePath, 'rb') as binaryFile:
            readHeader(binaryFile)
            self.name = os.path.basename(filePath)
            self.length = (
                self.riffHeader['dataHeader']['chunkDataSize'] /
                self.riffHeader['fmtData']['samplingRate'] /
                self.riffHeader['fmtData']['blockAlign']
                )
            readAudioData(binaryFile)

    def generateWaveformSummary(self, drawPoints):
        # Returns N points for drawing simplified waveform (averges over range)
        audioSamples = len(self.audioData)
        bufferLength = math.ceil(audioSamples/drawPoints)

        if (self.riffHeader['fmtData']['channels']) == 1:
            normalizedSamples = [
                abs(self.audioData[i]) for i in range(len(self.audioData))
                ]
        else:
            normalizedSamples = [
                abs(sum(self.audioData[i]))/len(self.audioData[i])
                for i in range(len(self.audioData))
                ]

        points = [
            sum(normalizedSamples[i*bufferLength:(i+1)*bufferLength]) /
            bufferLength for i in range(drawPoints-1)
            ]
        points.append(
            sum(normalizedSamples[(drawPoints-1)*bufferLength:]) /
            len(normalizedSamples[(drawPoints-1)*bufferLength:])
            )
        return points

# Debug


if __name__ == '__main__':
    wavePath = sys.argv[1]
    waveLoader = WaveReader()
    waveLoader.loadWavefile(wavePath)
    # print(waveLoader.riffHeader)

    print(len(waveLoader.generateWaveformSummary(1000)))
