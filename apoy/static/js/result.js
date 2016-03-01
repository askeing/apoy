var mockTestCaseData = [
  {
    id: "0001",
    text: "Login with correct username and password",
    priority: 1
  },
  {
    id: "0002",
    text: "Login with invalid username",
    priority: 2
  },
  {
    id: "0003",
    text: "Login with invalid password",
    priority: 3
  },
  {
    id: "0004",
    text: "Login with password that contains SQL-injection attack",
    priority: 4
  },
];

var Table = React.createClass({
  render: function() {
    var testcasesElems = this.props.testcases.map(function(testcase){
      var body;
      if (testcase.disabled){
        body = (<td><strike> {testcase.text} </strike></td>)
      }
      else{
        body = (<td> {testcase.text} </td>)
      }
      return (
        <tr key={testcase.index}>
          <td> <button onClick={function(){this.props.removeItem(testcase.index)}.bind(this)}>[x]</button></td>
          <td> {testcase.id}       </td>
          {body}
          <td> {testcase.priority} </td>
        </tr>
      )
    }.bind(this));

    return (
      <table>
        <tbody>
        <tr>
          <th> ID        </th>
          <th> Test Case </th>
          <th> Priority</th>
        </tr>
        {testcasesElems}
        </tbody>
      </table>
    )
  }
});

var Result = React.createClass({
  getInitialState: function(){
    return {
      totalTime: 60,
      testcases: []
    }
  },
  componentDidMount: function(){
    this.loadTestcases();
  },

  loadTestcases: function(){
    //TODO:ajax
    var testcases = mockTestCaseData;
    testcases = testcases.map(function(testcase, index){
      testcase['index'] = index
      return testcase
    })
    this.setState({testcases: testcases})

  },

  //TODO: change this to toggle
  removeItem: function(idx) {
    var newState = this.state.testcases;
    newState[idx]['disabled'] = true;
    this.setState(newState);
  },

  filterTestcaseByTotalTime: function(testcases, totalTime){
    var priority = totalTime / 30; //TODO: improve the algo
    return testcases.filter(function(tc){return tc.priority <= priority});
  },

  generateCsvUrl: function(testcases) {
    
    var enabledTextcases = testcases.filter(function(obj){return !obj.disabled})
    var text = enabledTextcases.map(function(obj){return obj.text}).join('\n');

    var data = new Blob([text], {type: 'text/csv'});

          // If we are replacing a previously generated file we need to
      // manually revoke the object URL to avoid memory leaks.
      // TODO: call revokeObjectURL when needed
      /*
      if (this.state.csv_url !== null) {
        window.URL.revokeObjectURL(this.state.csv_url);
      }
      */

      //this.setState({csv_url: window.URL.createObjectURL(data)});
      return window.URL.createObjectURL(data);
  },

  render: function() {
    var shownTestcases = this.filterTestcaseByTotalTime(this.state.testcases, this.state.totalTime);
    return (
      <div>
        <p> You can use the slider to custmize the desired execution time.</p>
        <input type="range" min="30" max="120" step="30" defaultValue="60" 
               onChange={function(evt){this.setState({totalTime: evt.target.value})}.bind(this)}/>
        <label>Estimated Time: {this.state.totalTime} min</label>
        <br />
        <a download="mozapoy_test_suite.csv" href={this.generateCsvUrl(shownTestcases)} >Download as Excel CSV</a>
        <Table testcases={shownTestcases} removeItem={this.removeItem}/>
      </div>
    )
  }
});

window.Result = Result;
