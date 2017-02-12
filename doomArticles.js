$("#doomBtn").click(function(){
  var searchRandom = ["Doomsday", "Donald Trump", "Iran", "Earthquakes", "Hurricanes", "War", "Fear", "Communism", "Fascism", "International Relations"];
  var searchTerm = searchRandom[Math.floor(Math.random()*10)];

  window.alert("Doom Button clicked!");
  // searchTerm = $("#searchInput")[0].value;
  if (!searchTerm) {
    window.alert("No Search Query Detected");
    return;
  }

  $.ajax({
    url: 'https://en.wikipedia.org/w/api.php',
    dataType: 'jsonp',
    data: {
      action: 'opensearch',
      search: searchTerm,
      limit: 10
      },
    success: function(data) {
      $("#dataDiv").html('');
      if(!data[1][0]){
        $("#dataDiv").append('<div class="fadeInUp displayBox"><h2>' + 'No Data Returned' + ' </h2><p>' + 'Nothing related to this search term was found in the Wikipedia database. Please try a different search term.' + '</p></div></a>');
      }

      /* Troubleshooting
      console.log(data); //
      console.log(data[1][0]); //Title
      console.log(data[2][0]); //Summary
      console.log(data[3][0]); //Link */

      // Creates information boxes with data
      for (var i = 0; i < data[1].length; i++) {
        $("#dataDiv").append('<a href="' + data[3][i] + '" target="_blank"><div class="fadeInUp displayBox"><h2>' + data[1][i] + ' </h2><p>' + data[2][i] + '</p></div></a>');
      }
    }
  });
// end of search button function
  });
