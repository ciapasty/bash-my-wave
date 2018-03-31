import java.io.*
import java.nio.charset.Charset

fun main(args: Array<String>) {

    val wavFile = WaveFile()
    wavFile.loadFile("sample2.wav")

}
class WaveFile {

    var chunkID: String = ""
    var chunkSize: Int = 0
    var format: String = ""
    var subchunk1ID: String = ""
    var subchunk1Size: Int = 0
    var audioFormat: Int = 0
    var numChannels: Int = 0
    var sampleRate: Int = 0
    var byteRate: Int = 0
    var blockAlign: Int = 0
    var bitsPerSample: Int = 0
    var extraParamSize: Int = 0
    var extraParams: Any? = null
    var subchunk2ID: String = ""
    var subchunk2Size: Int = 0
    var data: ByteArray? = null

    fun loadFile(filePath: String) {
        val rawByteArray = File(filePath).readBytes()
        println(rawByteArray.size)
        readRIFFHeader(rawByteArray)

        println(rawByteArray.size-46)
    }

    private fun readRIFFHeader(rawBytes: ByteArray) {
        val header = rawBytes.copyOfRange(0, 44)

        var x = 0
        extraParamSize = byteArrayToInt(header.copyOfRange(36, 38), false)
        while(x < 46+extraParamSize) {
            when(x) {
                0 -> chunkID = header.copyOfRange(x, x+4).toString(Charset.forName("US-ASCII"))
                4 -> chunkSize = byteArrayToInt(header.copyOfRange(x, x+4), false)
                8 -> format = header.copyOfRange(x, x+4).toString(Charset.forName("US-ASCII"))
                12 -> subchunk1ID = header.copyOfRange(x, x+4).toString(Charset.forName("US-ASCII"))
                16 -> subchunk1Size = byteArrayToInt(header.copyOfRange(x, x+4), false)
                20 -> audioFormat = byteArrayToInt(header.copyOfRange(x, x+2), false)
                22 -> numChannels = byteArrayToInt(header.copyOfRange(x, x+2), false)
                24 -> sampleRate = byteArrayToInt(header.copyOfRange(x, x+4), false)
                28 -> byteRate = byteArrayToInt(header.copyOfRange(x, x+4), false)
                32 -> blockAlign = byteArrayToInt(header.copyOfRange(x, x+2), false)
                34 -> bitsPerSample = byteArrayToInt(header.copyOfRange(x, x+2), false)
                20+subchunk1Size -> subchunk2ID = header.copyOfRange(x, x+4).toString(Charset.forName("US-ASCII"))
                24+subchunk1Size -> subchunk2Size = byteArrayToInt(header.copyOfRange(x, x+4), false)
            }
            x = x+2
        }

        println("ChunkID: $chunkID")
        println("ChunkSize: $chunkSize")
        println("Format: $format")
        println("Subchunk1ID: $subchunk1ID")
        println("Subchunk1Size: $subchunk1Size")
        println("AudioFormat: $audioFormat")
        println("NumChannels: $numChannels")
        println("SampleRate: $sampleRate")
        println("ByteRate: $byteRate")
        println("BlockAlign: $blockAlign")
        println("BitsPerSample: $bitsPerSample")
        println("ExtraParamSize: $extraParamSize")
        println("Subchunk2ID: $subchunk2ID")
        println("Subchunk2Size: $subchunk2Size")

    }

    private fun byteArrayToInt(bytes: ByteArray, bigEndian: Boolean): Int {
        if (bigEndian)
            return bytes.mapIndexed { i, byte -> byte.toInt() and 0xFF shl bytes.size*8/(i+1) }.reduce { acc, i -> acc or i }

        return bytes.mapIndexed { i, byte -> byte.toInt() and 0xFF shl 8*i }.reduce { acc, i -> acc or i }
    }

}

