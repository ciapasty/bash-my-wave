import math
import os


def read(filePath):
    audioFile = {}

    with open(filePath, 'rb') as binaryFile:
        audioFile['riffHeader'] = readHeader(binaryFile)
        print(audioFile['riffHeader'])
        audioFile['name'] = os.path.basename(filePath)
        audioFile['length'] = (
            audioFile['riffHeader']['dataHeader']['chunkDataSize'] /
            audioFile['riffHeader']['fmtData']['samplingRate'] /
            audioFile['riffHeader']['fmtData']['blockAlign']
            )
        audioFile['audioData'] = readAudioData(
            binaryFile, audioFile['riffHeader']
            )
    
    return audioFile


def generateWaveformSummary(riffHeader, drawPoints, audioData):
    # Returns N points for drawing simplified waveform (averges over range)
    audioSamples = len(audioData)
    bufferLength = math.ceil(audioSamples/drawPoints)

    if (riffHeader['fmtData']['channels']) == 1:
        normalizedSamples = [
            abs(audioData[i]) for i in range(len(audioData))
            ]
    else:
        normalizedSamples = [
            abs(sum(audioData[i]))/len(audioData[i])
            for i in range(len(audioData))
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


def readASCIItext(binaryFile, nBytes):
        return bytes(binaryFile.read(nBytes)).decode('ASCII')


def readInt(binaryFile, nBytes, endian, signed):
    return int.from_bytes(
        binaryFile.read(nBytes),
        endian,
        signed=signed
        )


def readHeader(binaryFile):
    riffHeader = {}
    riffHeader['chunkID'] = readASCIItext(binaryFile, 4)
    riffHeader['chunkDataSize'] = readInt(
        binaryFile, 4, 'little', False
        )
    riffHeader['riffTypeID'] = readASCIItext(binaryFile, 4)

    riffHeader['fmtHeader'] = {}
    riffHeader['fmtHeader']['chunkID'] = readASCIItext(
        binaryFile, 4
        )
    riffHeader['fmtHeader']['chunkDataSize'] = readInt(
        binaryFile, 4, 'little', False
        )
    riffHeader['fmtData'] = readFormatData(
        riffHeader['fmtHeader']['chunkDataSize'],
        binaryFile
        )
    
    # BWF support
    chunkID = bytes(binaryFile.read(4)).decode('ASCII')
    chunkDataSize = int.from_bytes(binaryFile.read(4), 'little')
    while (chunkID != 'data'):  # TODO replace with switch/if
        riffHeader[chunkID+'Header'] = {
            'chunkID': chunkID,
            'chunkDataSize': chunkDataSize,
            # Temporary support for BWF and other Chunks
            chunkID+'Data': {}
        }
        binaryFile.read(chunkDataSize)
        chunkID = bytes(binaryFile.read(4)).decode('ASCII')
        chunkDataSize = int.from_bytes(binaryFile.read(4), 'little')

    riffHeader['dataHeader'] = {
        'chunkID': chunkID,
        'chunkDataSize': chunkDataSize
    }
    
    return riffHeader


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
        fmtData['extraFormatInfo'] = {}  # not supported

    return fmtData


def normalizeSample(sample, bitRate):
    maxValue = 0
    if (bitRate == 8):
        maxValue = 128
    if (bitRate == 16):
        maxValue = 32768
    if (bitRate == 24):
        maxValue = 8388608

    return sample/maxValue


def mapChannels(binaryFile, audioChannels, bytesPerChannel, bitsPerSample):
    return [normalizeSample(
                readInt(binaryFile, bytesPerChannel, 'little', True),
                bitsPerSample
                ) for i in range(audioChannels)]


def readAudioData(binaryFile, riffHeader):
    audioData = []
    audioChannels = riffHeader['fmtData']['channels']
    audioChunkBytes = riffHeader['dataHeader']['chunkDataSize']
    bytesPerChannel = int(
        riffHeader['fmtData']['blockAlign']/audioChannels
        )
    audioSamples = int(
        audioChunkBytes/riffHeader['fmtData']['blockAlign']
        )

    if (audioChannels == 1):
        audioData = [
            normalizeSample(
                readInt(binaryFile, bytesPerChannel, 'little', True),
                riffHeader['fmtData']['bitsPerSample']
                ) for x in range(audioSamples)]
    else:
        audioData = [
            mapChannels(
                binaryFile,
                audioChannels,
                bytesPerChannel,
                riffHeader['fmtData']['bitsPerSample']
                ) for x in range(audioSamples)
            ]
    return audioData
