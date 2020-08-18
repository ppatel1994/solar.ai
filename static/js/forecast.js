function updateDates(){
    var now = moment();
    var today = now.format('MMM Do, YYYY');
    var tomorrow = now.add(1, 'days').format('MMM Do, YYYY');
    var day2 = now.add(1, 'days').format('MMM Do, YYYY');
    var day3 = now.add(1, 'days').format('MMM Do YYYY')
    var dates = [tomorrow, day2, day3];
    var tags = document.getElementsByClassName("date");
    for (var i = 0; i < tags.length; i++){
      tags[i].innerHTML = dates[i];
    }
}

function animateValue(id, start, end, duration) {
    var range = end - start;
    var current = start;
    var increment = 1;
    var stepTime = Math.abs(Math.floor(duration / range));
    var obj = document.getElementById(id);
    var timer = setInterval(function() {
        current += increment;
        obj.innerHTML = current;
        if (current >= end) {
            clearInterval(timer);
        }
    }, stepTime);
}

function plotWeather(id, date, temp, windDir, lat, long){
  var temp_plot = {
    x: date,
    y: temp,
    name: 'Temperature',
    mode: 'lines',
  };

  var windDir_plot = {
    x: date,
    y: windDir,
    yaxis: 'y2',
    name: 'Wind Direction',
    mode: 'lines',
    line: {
      color: '#30c095'
    },
  };

  var layout = {
    title:{
      text: "LAT: " + lat + ", " + "LONG: " + long,
      size: 24,
    },
    autosize: true,
    plot_bgcolor: "#202225",
    paper_bgcolor: "#202225",
    yaxis: {
      title: 'Temperature',
      tickfont: {
        color: 'white',
      },
    },
    yaxis2: {
      title: 'Wind Direction (Degrees)',
      overlaying: 'y',
      side: 'right',
      tickfont: {
        color: 'white',
      },
    },
    xaxis: {
      title: "Time",
      nticks: 5,
      rangeslider: {},
      tickfont: {
        color: 'white',
      },
    },
    legend: {
      'orientation': 'h',
      x: 0.35,
      y:1.3,
    }
  };
  var data = [temp_plot, windDir_plot];
  Plotly.newPlot(id, data, layout);
  window.onresize = function() {
    Plotly.relayout(id, {
        'xaxis.autorange': true,
        'yaxis.autorange': true
    });
  };
};

$(function(){
  $('#forecast').bind('click', function(){
    $.getJSON('/predict', {
      a: $('input[name = "location"]').val()
    }, function(data){
      if (data["day1"] == "ERROR"){
        return;
      }
      animateValue("day1", 0, data["day1"], 1000)
      animateValue("day2", 0, data["day2"], 1000)
      animateValue("day3", 0, data["day3"], 1000)
      var div = document.getElementById('mapid');
      div.innerHTML = "";
      plotWeather("mapid", data['weatherData']['Date'], data['weatherData']['Temp'],
                data['weatherData']['WindDeg'], data['lat-long'][0], data['lat-long'][1]);
      var btn = document.getElementById('forecast');
      btn.disabled = true;
    });
    return false;
  })
})

updateDates();
