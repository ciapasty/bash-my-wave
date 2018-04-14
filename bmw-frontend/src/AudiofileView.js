import React, { Component } from 'react';
import playIcon from './play.png';
import pauseIcon from './pause.png';
import stopIcon from './stop.png';

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

export default AudiofileView;
