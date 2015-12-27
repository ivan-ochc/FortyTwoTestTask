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

                      $('#requests > tbody').empty();
                      $.each(JSON.parse(data), function (idx, obj) {
                          $('#requests > tbody').append('<tr><td>' + obj.fields.host + '</td><td>' + obj.fields.path + '</td><td>' + obj.fields.method + '</td><td>' + obj.fields.status_code + '</td><td>' + obj.fields.priority + '</td></tr>')
                      })
                      $("#requests").trigger("update");
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

setTimeout(function() {
    $('.tablesorter').tablesorter({
        widgets: ["saveSort"],
        widgetOptions: {
            filter_columnFilters : true,
            filter_searchDelay: 100,
            filter_startsWith: false,
            filter_defaultAttrib : 'data-value'
        },
        // *** Appearance ***
        // fix the column widths
        widthFixed: true,

        // *** Functionality ***
        // starting sort direction "asc" or "desc"
        sortInitialOrder: "asc",
        // These are detected by default,
        // but you can change or disable them
        headers: {
            // set "sorter : false" (no quotes) to disable the column
            0: {sorter: false},
            1: {sorter: false},
            2: {sorter: false},
            3: {sorter: false},
            4: {sorter: "digit"},
        },
        // extract text from the table - this is how is
        // it done by default
        textExtraction: {
            0: function (node) {
                return $(node).text();
            },
            1: function (node) {
                return $(node).text();
            }
        },
        // forces the user to have this/these column(s) sorted first
        sortForce: null,
        // initial sort order of the columns
        // [[columnIndex, sortDirection], ... ]
        sortList: [],
        // default sort that is added to the end of the users sort
        // selection.
        sortAppend: null,
        // Use built-in javascript sort - may be faster, but does not
        // sort alphanumerically
        sortLocaleCompare: false,
        // Setting this option to true will allow you to click on the
        // table header a third time to reset the sort direction.
        sortReset: false,
        // Setting this option to true will start the sort with the
        // sortInitialOrder when clicking on a previously unsorted column.
        sortRestart: false,
        // The key used to select more than one column for multi-column
        // sorting.
        sortMultiSortKey: "shiftKey",

        // *** Customize header ***
        onRenderHeader: function () {
            // the span wrapper is added by default
            $(this).find('span').addClass('headerSpan');
        },
        // jQuery selectors used to find the header cells.
        selectorHeaders: 'thead th',

        cssChildRow: "expand-child",
        cssHeader: "header",
        tableClass: 'tablesorter',

        // *** prevent text selection in header ***
        cancelSelection: true,

        // *** send messages to console ***
        debug: false

    });
    }, 500)

