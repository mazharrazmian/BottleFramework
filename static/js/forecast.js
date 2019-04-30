window.onload = function(){
    let form = document.querySelector('form');
    form.onsubmit = function(){
    const request = new XMLHttpRequest();
    request.open('POST','/forecast');
    request.onload = function(){
        const data = JSON.parse(request.response);
        console.log(data);
        let city_data= data[0];
        let city2_data = data[1];
        city_temp= [];
        dates= [];
        city2_temp =[];
        for( item of city_data){
            city_temp.push(item.main.temp);
            dates.push(item.dt_txt);
            //console.log("Peshawars temperature"+item.main.temp);
            
        }
        for(item of city2_data){
            city2_temp.push(item.main.temp)
            //console.log("London temperature"+item.main.temp);
        }
        createPlot(city_temp,city2_temp,dates,city,city2);
        
    }
    const city = document.querySelector("#city").value;
    const city2 = document.querySelector("#city2").value;
    let data = new FormData();
    data.append('city',city);
    data.append('city2',city2)
    request.send(data);
    return false;
}

    function createPlot(city_temp,city2_temp,dates,city,city2){
        var Peshawar = {
            x : dates,
            y : city_temp,
            type : 'scatter',
            name : `${city}`
          };
          
          var London = {
            x: dates,
            y: city2_temp,
            type: 'scatter',
            name : `${city2}`
          };
          
          var data = [Peshawar, London];
          
          Plotly.newPlot('result', data, {}, {showSendToCloud: true});
    }
}
