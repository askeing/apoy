var Form = React.createClass({
  render: function() {
    return (
      <div>
        <p>Please provide us some information about your project, so we can create a customized test suite for you</p>
        <form onSubmit={this.props.nextState}>
          <label>GitHub URL</label>
          <input type='text' name="githuburl" placeholder="https://www.github.com/your_username/your_repo"/>
          <button type='submit'>Submit</button>
        </form>
      </div>
    )
  }
});

window.Form = Form;
