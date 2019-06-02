var intervalId = null;
window.onload = function() {

  if (poll == true) {

    // Poll the server every 1000 milliseconds
    intervalId = setInterval(function(){
      poll_async_task_status();
    }, 200);
    
  } else {
    // Do not poll, do nothing on the progress
  }
};

var count_true = function(arr_param) {
  var count = 0;
  for (var i = 0; i < arr_param.length; i++) {
    if (arr_param[i] == true) {
      count++;
    }
  }
  return count;
};

var poll_async_task_status = function() {
  var xhr = new XMLHttpRequest();

  xhr.onload = function(e) {
    /*
     * update the progress bar or any indicator
     */
    var results = JSON.parse(xhr.response)['results'];
    var new_progress = Math.floor((count_true(results)/results.length) * 100);

    // Update the UI
    var progress = document.querySelector('#progress');
    progress.setAttribute('aria-valuenow', new_progress);
    progress.setAttribute('style', 'width:' + new_progress.toString() + '%')
    progress.innerHTML = new_progress.toString() + '%';

    if (new_progress >= 100) {
      clearInterval(intervalId);
      // TODO: transfer to new page
      var previous = endpoint.split('/').slice(0, 4);
      previous = previous.join('/') + '/?result=success';
      window.location.href = previous;
    }
  };

  var query = '?job_ids=';
  for (var i = 0; i < job_ids.length; i++) {
    if (i < (job_ids.length - 1)) {
      query += job_ids[i] + ',';
    } else {
      query += job_ids[i];
    }
  }
  xhr.open('GET', endpoint + query + '&' + (new Date()).getTime(), true);
  xhr.send();
};

