$('body').ready(function(){
    console.log("enroll.js");
    get_data();
})

function get_data(){
    url = enrollApiUrl;
    fetch(url, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        }
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        console.log(data.context[0].name);
        console.log(data.context.length);
        // console.log(data_got);
        //data table starts
        var k=1;
        $(`#StudentTable`).empty()
        for ( var i = 0; i<data.context.length;i++){
            $(`#StudentTable`).append(`
            <tr>
                    <td>${k++}</td>
                    <td>${data.context[i].SID}</td>
                    <td>${data.context[i].name}</td>
                    <td>${data.context[i].mobile}</td>
                    <td>${data.context[i].email}</td>
                    <td>${data.context[i].password}</td>
                  </tr>       
            `)
        }
        //data table ends
      });
}




