import React, { Component } from 'react';
import playIcon from './play.png';
import pauseIcon from './pause.png';
import stopIcon from './stop.png';
import sampleAudio from './sample.mp3';

// class AudiofileView extends Component {
//   render() {
//     return(
//       <div>
//         <WaveformTopBar />
//         {/* <WaveformView /> */}
//         <AudioPlayer audio={sampleAudio}/>
//       </div>
//     )
//   }
// }

class AudiofileView extends Component {
  constructor(props) {
    super(props);
    this.state = { playing: false };
  }

  componentDidMount() {
    this.audioPlayer.addEventListener("timeupdate", () => {
      let ratio = this.audioPlayer.currentTime / this.audioPlayer.duration;
      let position = this.timeline.offsetWidth * ratio;
      this.positionHandle(position);
    });
  };

  componentWillReceiveProps(nextProps) {
    console.log(nextProps.audio);
    this.audioPlayer.src = URL.createObjectURL(nextProps.audio);
  }

  play = () => {
    if (this.state.playing) {
      this.setState({ playing: false });
      this.audioPlayer.pause();
    } else {
      this.setState({ playing: true });
      this.audioPlayer.play();
    }
  }

  stop = () => {
    if (this.state.playing) {
      this.setState({ playing: false });
      this.audioPlayer.pause();
      this.audioPlayer.currentTime = 0;
    }
  }

  positionHandle = (position) => {
    let timelineWidth = this.timeline.offsetWidth - this.handle.offsetWidth;
    let handleLeft = position - this.timeline.offsetLeft;
    if (handleLeft >= 0 && handleLeft <= timelineWidth) {
      this.handle.style.marginLeft=handleLeft + "px";
    }
    if (handleLeft < 0) {
      this.handle.style.marginLeft = "0px";
    }
    if (handleLeft > timelineWidth) {
      this.handle.style.marginLeft = timelineWidth + "px";
    }
  };

  mouseMove=(e) => {
    this.positionHandle(e.pageX);
    this.audioPlayer.currentTime = (e.pageX / this.timeline.offsetWidth) * this.audioPlayer.duration;
  };

  mouseDown=(e) => {
    window.addEventListener('mousemove', this.mouseMove);
    window.addEventListener('mouseup', this.mouseUp);
    // Rework!
    if (this.audioPlayer.playing) {
      this.audioPlayer.pause();
    }
  };

  mouseUp=(e) => {
    window.removeEventListener('mousemove', this.mouseMove);
    window.removeEventListener('mouseup', this.mouseUp);
    // Rework!
    if (this.audioPlayer.playing) {
      this.audioPlayer.play();
    }
  };

  render() {
    return (
      <div className="AudioPlayer">
        <audio ref={(audio) => { this.audioPlayer=audio }} />
        <div>
          <img onClick={this.play} className="Icon" src={!this.state.playing? playIcon:pauseIcon} alt={!this.state.playing? "Play":"Pause"} />
          <img onClick={this.stop} className="Icon" src={stopIcon} alt="Stop" />
        </div>
        <div className="Timeline" onClick={this.mouseMove} ref={(timeline) => { this.timeline=timeline }} >
          {/* <WaveformView audioFile={this.props.audio} /> */}
          <div className="Handle" onMouseDown={this.mouseDown} ref={(handle) => { this.handle=handle }} />
        </div>
      </div>
    )
  }
}

// class WaveformTopBar extends Component {
//   render() {
//     return(
//       <div>
//         This is a toolbar above the waveform
//       </div>
//     )
//   }
// }

// class WaveformCommentView extends Component {
//   render() {
//     return(
//       <div>
        
//       </div>
//     )
//   }
// }

class WaveformView extends Component {
  constructor(props) {
    super(props)
  }

  getAudioData = (url, time) => {
    return new Promise(function (resolve, reject) {
        var audioArray = [];
        var context = new AudioContext();
        var track = new Audio(url);
        var bufferLength = time * context.sampleRate;
        var buffer = new Float32Array(bufferLength);
        var collector = context.createScriptProcessor(0, 1);
        var audioSource = context.createMediaElementSource(track);
        var samplesCollected = 0;

        function cleanup () {
            track.pause();
            collector.disconnect(context.destination);
            audioSource.disconnect(collector);
            audioArray.splice(audioArray.indexOf(collector), 1);
        }

        collector.onaudioprocess = function collectAudio (event) {
            var samplesToCollect = bufferLength - samplesCollected;
            var inputData = event.inputBuffer.getChannelData(0).subarray(0, samplesToCollect);
            buffer.set(inputData, samplesCollected);

            samplesCollected += inputData.length;
            if ( samplesCollected >= bufferLength ) {
                cleanup();
                resolve(buffer);
            }
        };

        track.onerror = reject;

        audioSource.connect(collector);
        collector.connect(context.destination);
        track.play();

        audioArray.push(collector);
    });
}

getAmplitudes = (attack, decay) => {
    return function collectAmplitudes (buffer) {
        var previousSample = 0;
        for ( var i = 0; i < buffer.length; i++ ) {
            var factor = 1 + (buffer[i] > previousSample ? attack : decay);
            buffer[i] = Math.abs(factor * (previousSample - buffer[i]));
        }

        return buffer;
    };
}

drawWaveform = (width, height, canvas) => {
    return function drawFromBuffer (buffer) {
        canvas.width = width;
        canvas.height = height;
        var context = canvas.getContext("2d");

        var halfHeight = Math.floor(height / 2);
        var middleY = halfHeight;

        context.beginPath();

        var x = 0;

        context.moveTo(x, middleY - buffer[0] * halfHeight);

        for ( x = 1; x < width; x++ ) {
            context.lineTo(x, middleY - buffer[Math.round(x / width * buffer.length)] * halfHeight);
        }

        for ( x = width; x-- > 0; ) {
            context.lineTo(x, middleY + buffer[Math.round(x / width * buffer.length)] * halfHeight);
        }

        context.closePath();
        context.fill();
    };
}

componentWillReceiveProps(nextProps) {
  this.getAudioData(nextProps.audioFile, 10)
    .then(this.getAmplitudes(0.1, 0.1))
    .then(this.drawWaveform(800, 600, this.canvas))
    .catch(function (error) {
        console.error(error);
  });
}
  
  render() {
    return(
      <div>
        <canvas ref={(canvas) => { this.canvas = canvas }} />
      </div>
    )
  }
}

export default AudiofileView;
