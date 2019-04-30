window.onload = function(){
    let form = document.querySelector('form');
    form.onsubmit = function(){
        const request = new XMLHttpRequest();
    request.open('POST','/forecast');
    request.onload = function(){
        const data = JSON.parse(request.response);
        console.log(data);
        
    }
    const city = document.querySelector("#city").value;
    const city2 = document.querySelector("#city2").value;
    let data = new FormData();
    data.append('city',city);
    data.append('city2',city2)
    request.send(data);
    return false;
}
}
