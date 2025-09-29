$(document).ready(function () {
    var table = $('#view_sen').DataTable( {
        scrollY:        "500px",
        scrollX:        true,
        scrollCollapse: true,
        paging:         true,
        fixedColumns:   {
            heightMatch: 'none'
        },
        language: {
            url:"static/js/pt_br.json"
        }
    } );
});

function handleClick(cb,id){
    var topic = "";
    if (id == "control"){
      topic= "/atuadores";
    }

    var data = "";
    if (cb.checked){
      data = "1";
    }else{
      data = "0";
    }
    $.ajax({
        url: "{{ url_for('publish_message') }}",
        contentType: 'application/json;charset=UTF-8',
        cache: false,
        method: 'POST',
        dataType: 'json',
        data: JSON.stringify({
            message: data,
            topic: topic
        }),
        success: function(data) {
            console.log(data);
        }
    });
  }
  