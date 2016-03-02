var App = React.createClass({
  getInitialState: function() {
    return {
      step: 1, // Form is handled in previous pages
      //projAttributes:{}
    }

  },
  nextState: function(evt){
    evt.preventDefault();
    if (this.state.step == 0){
      //console.log(evt)
      //TODO: collect values and do ajax here
      console.log(evt.target.githuburl.value)
    }
    this.setState({
      step: this.state.step + 1,
    });
  },
  render: function() {
    if (this.state.step == 0) {
      return <Form nextState={this.nextState}/>
    }
    else if (this.state.step == 1){
      return <Result />
    }
    else {
      return <div>Unknown State: {this.state.step} </div>
    }
  }
});


ReactDOM.render(
  <App content={"Hello world"} />,
  document.getElementById('container')
);
