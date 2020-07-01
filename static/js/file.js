let test_id = "01234";
//let file = JSON.parse('data');

//console.log(file);

function download_file() {
	let url = "/file/" + test_id
    $.ajax({
        type: "GET",
        url: url,
        //data: JSON.stringify([10]), // number of messages to retrieve
        success: function(response)
        {
            //console.log(msgs.length + ' messages retrieved!');
            
            let j = JSON.parse(response);
            console.log(j);
        },
        error: function(data)
        {
            alert('ERROR\n' + data.responseText);
            console.log(data)
        },
    });
}