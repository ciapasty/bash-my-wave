import React, { Component } from 'react';
// import AudioPlayer from './AudioPlayer';
import AudiofileView from './AudiofileView';
import logo from './logo.svg';
import playIcon from './play.png';
import pauseIcon from './pause.png';
import './App.css';

class App extends Component {
  render() {
    return (
      <AudiofileCommentView />
    );
  }
}

class AudiofileCommentView extends Component {
  constructor(props) {
    super(props);
    this.state = { audio: "" };
  }

  filesLoaded = (fileList) => {
    var audioFile = fileList[0];
    this.setState({ audio: audioFile }); //URL.createObjectURL(audioFile)});
  }

  render() {
    return(
      <div className="App">
        <input onChange={ (e) => this.filesLoaded(e.target.files)} type="file" ref={(input) => {this.inputDialog=input }} />
        <AudiofileView audio={this.state.audio} audioFile={AUDIOFILE}/>
        <CommentTable comments={AUDIOFILE.comments} />
      </div>
    )
  }
}

class CommentTable extends Component {
  render() {
    const rows = [];
    
    this.props.comments.forEach((comment) => {
      rows.push(
        <CommentRow comment={comment} key={comment.time} />
      )
    })

    return(
      <table>
        <tbody>{rows}</tbody>
      </table>
    )
  }
}

class CommentRow extends Component {
  render() {
    const comment = this.props.comment;
    return (
      <tr>
        <td>{comment.time}</td>
        <td>{comment.text}</td>
      </tr>
    )
  }
}

const AUDIOFILE = {
  source: '/Users/mattijah/Downloads/sample.mp3',
  comments: [
    {time: 0.2, text: 'Comment 1'},
    {time: 0.8, text: 'Comment 2'}
  ]
}

export default App;
