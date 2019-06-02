/*
 * upload.js
 * front-end behavior code
 *
 */
var hideDiv = function() {
  var type = document.querySelector("#data_select").value;
  var stravaDiv = document.querySelector("#strava-upload");
  var runtasticDiv = document.querySelector("#runtastic-upload");

  if (type === "strava") {
    // show strava div form
    stravaDiv.hidden = false;
    runtasticDiv.hidden = true;
  } else if (type === "runtastic") {
    // show runtastic div form
    stravaDiv.hidden = true;
    runtasticDiv.hidden = false;
  } else {
    // hide both
    stravaDiv.hidden = true;
    runtasticDiv.hidden = true;
  }
};

var uploadSubmit = function(e) {
  // TODO: process the files on the frontend
  // rather than on the backend

  // e.preventDefault();   // do not submit!
  // // process the files
  // // create data to be posted
  // // update view? 
  // var uploadForm = new FormData(document.querySelector("#upload-form"));
  // var dataType = uploadForm.get("data_type");

  // if (dataType === "runtastic") {
  //   // Process runtastic form
  //   console.log("runtastic");
  //   var activities = uploadForm.getAll("runtastic-activities");
  //   var points = uploadForm.getAll("runtastic-points");
  //   // generate the json file?
  // } else {
  //   // Process strava form
  //   console.log("strava");
  //   var activities = uploadForm.getAll("strava-activities");
  //   var points = uploadForm.getAll("strava-points");
  //   // generate the json file?
  // }
}

window.onload = function() {
  // Add event listener to the selector
  hideDiv();
  var typeSelector = document.querySelector("#data_select");
  var formSubmit = document.querySelector("#submit-run");

  typeSelector.addEventListener("input", hideDiv);
  formSubmit.addEventListener("click", uploadSubmit);
}
