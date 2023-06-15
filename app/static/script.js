var myArray = JSON.parse('{{ data_json | safe }}');
    // Now, the 'data' variable in JavaScript will contain your table data as an array of objects
console.log(myArray);

buildTable(myArray)

$('#search-input').on('keyup',function(){
    var value = $(this).val()
    console.log('Value: ', value)
    var data = searchTable(value,myArray)
    buildTable(data)

})

function searchTable(value, data){
    var filteredData =[]
    for(var i = 0;i< data.length;i++){
        value = value.toLowerCase()
        var name = data[i].name.toLowerCase()

        if(name.includes(value)){
            filteredData.push(data[i])
        }

    }
    return filteredData
}

function buildTable(data){
  var table = document.getElementById('myTable')
  table.innerHTML = ''
  for (var i = 0; i < data.length; i++){
      var colcre_id = `cre_id-${i}`
      var colmarca = `marca-${i}`
      var colregular = `regular-${i}`
      var colpremium = `premium-${i}`
      var coldiesel = `diesel-${i}`

      var row = `<tr>
                      <td>${data[i].cre_id}</td>
                      <td>${data[i].marca}</td>
                      <td>${data[i].regular}</td>
                      <td>${data[i].premium}</td>
                      <td>${data[i].diesel}</td>
                 </tr>`
      table.innerHTML += row
  }
}