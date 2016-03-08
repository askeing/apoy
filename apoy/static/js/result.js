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
    var testcasesElems = this.props.testcases.map(function(testcase, index){
      var body;
      //var text = "";
      console.log(testcase)
      var text = testcase.steps.map(function(step){
        var expected;
        if (step.expected) {
          expected = (<p> >>> {step.expected}</p>)
        }
        return (
          <div>
            <p>{step.step}</p>
            {expected}
          </div>
        )
      })
      /*
      testcase[stepidx].step + "\n>>>" + testcase[stepidx].expected + "\n"
      for (var stepidx in testcase){
        text += testcase[stepidx].step + "\n>>>" + testcase[stepidx].expected + "\n"
      }
      console.log(text)
      */
      //FIXME: fake priority:
      if (testcase.disabled){
        body = (<td><strike> {text} </strike></td>)
      }
      else{
        body = (<td> {text} </td>)
      }
      return (
        <tr key={testcase.index}>
          <td> <button className="btn btn-default" onClick={function(){this.props.removeItem(testcase.index)}.bind(this)}><span className="glyphicon glyphicon-ban-circle"></span></button></td>
          <td> {index/*testcase.id*/}       </td>
          {body}
          <td> {testcase.priority} </td>
        </tr>
      )
    }.bind(this));

    return (
      <table className="table table-striped">
        <thead>
          <tr>
            <th> Disable   </th>
            <th> ID        </th>
            <th> Test Case </th>
            <th> Priority</th>
          </tr>
        </thead>
        <tbody>
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
      testcases: [{'steps':[{'step': 'loading...'}]}]
    }
  },
  componentDidMount: function(){
    this.loadTestcases();
  },

  loadTestcases: function(){
    //TODO:ajax
    if (typeof(fetch) == undefined){
      alert('We are using the latest Fetch API, you need to update your browser or wait for us to implement a backward compatiable version')
    }

    var a = new RegExp("taskid=([0-9]+)");
    var taskid = decodeURIComponent(a.exec(window.location.search)[1]);
    //TODO: check for invalid id

    var timer = setInterval(function(){
      fetch('/rest/task/' + taskid).then(function(resp){
        console.log(this)
        if (resp.status !== 200) {
          console.log('failed, ' + resp.status)
          return
        }
        resp.json().then(function(data){
          console.log(this)
          if (data.status == "done"){
            clearInterval(timer);
            var keys = Object.keys(data.results);
            console.log(keys)
            if (keys.length !== 1){
              alert('Bad formatted test cases, please contact the site administrator for this issue.')
            }
            
            var testcases = data.results[keys[0]].map(function(testcase, index){
              testcase['index'] = index
              return testcase
            })
            this.setState({testcases: testcases})
          }
          console.log("Still in progress")
        }.bind(this))
      }.bind(this))
    }.bind(this), 3000);

    /*
    var testcases = mockTestCaseData;
    testcases = testcases.map(function(testcase, index){
      testcase['index'] = index
      return testcase
    })
    this.setState({testcases: testcases})
    */

  },

  //TODO: change this to toggle
  removeItem: function(idx) {
    var newState = this.state.testcases;
    newState[idx]['disabled'] = true;
    this.setState(newState);
  },

  filterTestcaseByTotalTime: function(testcases, totalTime){
    //FIXME: a workaround before we have priority in the generated result
    if (typeof(testcases[0].priority) == "undefined"){
      return testcases
    }
    //XXX: get the max from range 
    //FIXME: hardcoded 5
    var level = 5 - totalTime / 30; //TODO: improve the algo
    console.log(level)
    var priorities = testcases.map(function(tc){return tc.priority});
    console.log(priorities)
    //XXX: 4 is hardcoded
    var targetPriority = (Math.max.apply(null, priorities) - Math.min.apply(null, priorities)) / 4 * level + Math.min.apply(null, priorities);
    console.log(targetPriority)
    return testcases.filter(function(tc){return tc.priority >= targetPriority});
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
      <div className="container">
        <div className="row">
          <h1>MozApoy Test Cases</h1>
        </div>
        <div className="row well">
          <div className="col-xs-6">
            <p> You can use the slider to custmize the desired execution time.</p>
            <input type="range" min="30" max="120" step="30" defaultValue="60" 
                   onChange={function(evt){this.setState({totalTime: evt.target.value})}.bind(this)}/>
            <label>Estimated Time: {this.state.totalTime} min</label>
          </div>
          <div className="col-xs-6">
            <a className="btn btn-success" download="mozapoy_test_suite.csv" href={this.generateCsvUrl(shownTestcases)} >Download as Excel CSV</a>
          </div>
        </div>
        <div className="row">
          <Table testcases={shownTestcases} removeItem={this.removeItem}/>
        </div>
      </div>
    )
  }
});

window.Result = Result;
