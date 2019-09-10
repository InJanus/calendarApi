var web = "http://127.0.0.1:5000/";

function getTasks(){
    //get element by id for paragraph
    var xhttp = new XMLHttpRequest();
    var params = "table=" + document.getElementById("selectbox").value;
    xhttp.open("GET", web + "api/1.0/tasksget/" + "?" + params, true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("output").innerHTML = this.responseText; //this sets the api request
      }
    };
}

function newTask(){
  // new task to add to the data base
  var xhttp = new XMLHttpRequest();
  xhttp.open("PUT", web + "api/1.0/tasksput/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  var param = "title=" + document.getElementById('title').value + 
  "&disc=" + document.getElementById('disc').value + 
  "&date=" + document.getElementById('date').value + 
  "&done=" + "false" + "&table=" + document.getElementById('selectbox').value;
  xhttp.send(param);
  xhttp.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        document.getElementById("output").innerHTML = this.responseText;
    }
  };
}

function deleteAll(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", web + "api/1.0/taskdeleteAll/" + "?" + "table=" + document.getElementById('selectbox').value, true);
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        document.getElementById("output").innerHTML = this.responseText;
    }
  };
}

function update_list(){
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", web + "api/1.0/tablenames/", true);
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      var select = document.getElementById("selectbox");
      var length = JSON.parse(this.responseText).length;
      console.log(this.responseText);
      select.options.length = length;
      for(var i =0; i < length; i++){
        select.options[i] = new Option(JSON.parse(this.responseText).lists[i], JSON.parse(this.responseText).lists[i]);
      }
    }
  };
}