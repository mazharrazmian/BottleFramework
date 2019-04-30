window.onload = function(){
    let form = document.querySelector('form');
    form.onsubmit = function(){
        const request = new XMLHttpRequest();
    request.open('POST','/');
    request.onload = function(){
        const data = JSON.parse(request.response);
        console.log(data);
        if(data[0] && data[1]){
            if (data[0].cod != 200 || data[1].cod != 200){
                console.log(data.cod);
                alert("Please enter correct city names");
                return false;
            }
        }
        else{
            alert("Please enter correct city names");
                return false;
        }
        
        let city_names = [];
        let temperatures = [];
        let pressures = [];
        let wind_speed= [];
        let humidity = [];
        for (item of data){
            console.log(item);
            city_names.push(item.name);
            temperatures.push(item.temp);
            pressures.push(item.pressure);
            wind_speed.push(item.wind_speed);
            humidity.push(item.humidity);
        }
        createCharts(city_names,temperatures,pressures,wind_speed,humidity);
    };
    const city = document.querySelector("#city").value;
    const city2 = document.querySelector("#city2").value;
    let data = new FormData();
    data.append('city',city);
    data.append('city2',city2)
    request.send(data);
    return false;
    }


    function createCharts(city_names,temperatures,pressures,wind_speed,humidity){
        // Extract JSON data from request
        //console.log(request.responseText);
         createBarGraph(city_names,temperatures,wind_speed,humidity);
         createScatterPlot(city_names,pressures);
     }

     function createScatterPlot(city_names,pressures){
        var data = [{
            type: 'bar',
            x: [pressures[0],pressures[1]],
            y: [city_names[0],city_names[1]],
            orientation: 'h'
          }];
          
          Plotly.newPlot('result1', data);
     }

 
     function createBarGraph(city_names,temperatures,wind_speed,humidity){
        var trace1 = {
            x: ['TEMPERATURE(F)','Wind Speed(MpH)','humidity'], 
            y: [temperatures[0],wind_speed[0],humidity[0]], 
            name: `${city_names[0]}`, 
            type: 'bar'
          };
          
          var trace2 = {
            x: ['TEMPERATURE(F)','Wind Speed(MpH)','humidity'], 
            y: [temperatures[1],wind_speed[1],humidity[1]], 
            name: `${city_names[1]}`, 
            type: 'bar'
          };
          
          var data = [trace1, trace2];
          var layout = {barmode: 'group'};
          
          Plotly.newPlot('result', data, layout, {}, {showSendToCloud:true});
     }
}