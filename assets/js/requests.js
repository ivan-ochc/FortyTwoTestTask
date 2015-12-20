var prevData;
var newRequestsCounter = 0;
var getRequests = function(){
          $.ajax({
              async: true,
              type: "GET",
              url: "/get_requests/",
              success: function(data){
                  if (prevData != data){
                      if (prevData != null){
                          var requests = $.parseJSON('[' + prevData + ']');
                          $.each(JSON.parse(data), function(idx, obj) {
                              var isNew = true
                              for (x in requests[0]) {
                                  if (requests[0][x].pk == obj.pk) {
                                      isNew = false
                                  }
                              }
                              if (isNew){
                                 newRequestsCounter++
                              }
                        })
                      }
                      prevData = data;
                  }
                  var visible = vis();
                  if (visible){
                     document.title = '42 Cups'
                     newRequestsCounter = 0
                  } else {
                     if (newRequestsCounter == 0) {
                         document.title = '42 Cups'
                     } else {
                         document.title =  'There are ' + newRequestsCounter + ' new requests'
                     }
                  }

                  $('#requests > tbody').empty();
                  $.each(JSON.parse(data), function(idx, obj) {
                      $('#requests > tbody').append('<tr><td>' + obj.fields.host + '</td><td>' + obj.fields.path + '</td><td>' + obj.fields.method + '</td><td>' + obj.fields.status_code + '</td></tr>')
                  })
                  setTimeout(getRequests, 2000)
              }
          });
};
getRequests();

var vis = (function(){
    var stateKey, eventKey, keys = {
        hidden: "visibilitychange",
        webkitHidden: "webkitvisibilitychange",
        mozHidden: "mozvisibilitychange",
        msHidden: "msvisibilitychange"
    };
    for (stateKey in keys) {
        if (stateKey in document) {
            eventKey = keys[stateKey];
            break;
        }
    }
    return function(c) {
        if (c) document.addEventListener(eventKey, c);
        return !document[stateKey];
    }
})();
