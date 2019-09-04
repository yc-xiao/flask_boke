$.ajax({
    url: '/path/to/file',
    type: 'POST',
    dataType: 'JSON',
    data: {param1: 'value1'}
})
.done(function() {
    console.log("success");
})
.fail(function() {
    console.log("error");
})
.always(function() {
    console.log("complete");
});
