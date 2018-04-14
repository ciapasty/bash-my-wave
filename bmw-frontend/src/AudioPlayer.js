import React, { Component } from 'react';
import playIcon from './play.png';
import pauseIcon from './pause.png';

class AudioPlayer extends Component {
  constructor(props) {
    super(props);
    this.state = { playing: false };
  }

  componentDidMount() {
    this.audio.addEventListener("timeupdate", () => {
      let ratio = this.audio.currentTime / this.audio.duration;
      let position = this.timeline.offsetWidth * ratio;
      this.positionHandle(position);
    });
  };

  componentWillReceiveProps(props) {
    this.setState({ playing: true });
  }

  play = () => {
    if (this.state.playing) {
      this.setState({ playing: false });
      this.audio.pause();
    } else {
      this.setState({ playing: true });
      this.audio.play();
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
    this.audio.currentTime = (e.pageX / this.timeline.offsetWidth) * this.audio.duration;
  };

  mouseDown=(e) => {
    window.addEventListener('mousemove', this.mouseMove);
    window.addEventListener('mouseup', this.mouseUp);
    // Rework!
    if (this.audio.playing) {
      this.audio.pause();
    }
  };

  mouseUp=(e) => {
    window.removeEventListener('mousemove', this.mouseMove);
    window.removeEventListener('mouseup', this.mouseUp);
    // Rework!
    if (this.audio.playing) {
      this.audio.play();
    }
  };

  render() {
    return (
      <div className="AudioPlayer">
        <audio src={this.props.audio} ref={(audio) => { this.audio=audio }} />
        <img onClick={this.play} className="Icon" src={!this.state.playing? playIcon:pauseIcon} alt={!this.state.playing? "Play":"Pause"} />
        <div className="Timeline" onClick={this.mouseMove} ref={(timeline) => { this.timeline=timeline }} >
          <div className="Handle" onMouseDown={this.mouseDown} ref={(handle) => { this.handle=handle }} />
        </div>
      </div>
    )
  }
}

export default AudioPlayer;
