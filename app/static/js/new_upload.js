var _url = 'http://localhost:5000'
//上传文件方法
function log_time() {
    var a = new Date();
    console.log(a);
    console.log(a.getSeconds());
}

function UpladFile() {
    log_time()
    var fileObj = document.getElementById("file").files[0]; // js 获取文件对象
    search(fileObj, false);
}

function UpladFileAsycio() {
    log_time()
    var fileObj = document.getElementById("file").files[0]; // js 获取文件对象
    search(fileObj, true);
}

function search(fileObj, flag){
    var url =  _url + "/new_upload/?"; // 接收上传文件的后台地址
    url = url + 'file_name' + '='+ fileObj.name + '&';
    url = url + 'file_size' + '='+ fileObj.size + '&';
    url = url + 'last_time' + '='+ fileObj.lastModified;
    // 查询文件状态
    var xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
    xhr.open('get', url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
    xhr.onload = function(evt){
        //服务断接收完文件返回的结果
        var data = JSON.parse(evt.target.responseText);
        if(!data['status']){
            if(flag){
                console.log('handler_searchx');
                handler_searchx(data);
            }else{
                console.log('handler_search');
                handler_search(data);
            }

        }
        update_process(data);
    }; //请求完成
    xhr.onerror = function(evt){
        console.log("上传失败！");
    }; //请求失败

    xhr.send(); //开始上传，发送form数据
}

function handler_searchx(data){
    blocks = data['blocks'];
    console.log(blocks)
    for(var each in blocks){
        if(!blocks[each]['status']){
            console.log(each);
            var datas = get_datas(each, blocks[each]['start'], blocks[each]['end']);
            url = "http://localhost:5000/new_upload/";
            var xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
            xhr.open('post', url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
            xhr.onload = function(evt){
                //服务断接收完文件返回的结果
                var data = JSON.parse(evt.target.responseText);
                console.log(data);
                update_process(data);
            }; //请求完成
            xhr.onerror = function(evt){
                console.log("上传失败！");
            }; //请求失败
            xhr.send(datas); //开始上传，发送form数据

        }
    }
}

function get_datas(split_file_name, start, end){
    var fileObj = document.getElementById("file").files[0];
    files = fileObj.slice(start, end);
    var form = new FormData(); // FormData 对象
    form.append("files", files); // 文件对象
    form.append("file_name", fileObj.name); // 文件对象
    form.append("split_file_name", split_file_name); // 文件对象
    form.append("last_time", fileObj.lastModified); // 文件对象
    return form
}

function update_process(data){
    blocks = data['blocks'];
    var count = 0;
    var total = 0;
    for(var each in blocks){
        total+=1;
        if(blocks[each]['status']){
            count+=1;
        }
    }
    var progressBar = document.getElementById("progressBar");
    var percentageDiv = document.getElementById("percentage");
    progressBar.max = total;
    progressBar.value = count;
    percentageDiv.innerHTML = '上传进度:' + count/total;
    log_time();
}

function handler_search(data){
    blocks = data['blocks'];
    var datas;
    for(var each in blocks){
        if(!blocks[each]['status']){
            var datas = get_datas(each, blocks[each]['start'], blocks[each]['end']);
            url = _url+ "/new_upload/";
            var xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
            xhr.open('post', url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
            xhr.onload = function(evt){
                //服务断接收完文件返回的结果
                var data = JSON.parse(evt.target.responseText);
                if(!data['status']){
                    handler_search(data);
                    update_process(data);
                }
                update_process(data);
            }; //请求完成
            xhr.onerror = function(evt){
                console.log("上传失败！");
            }; //请求失败
            xhr.send(datas); //开始上传，发送form数据
            break;
        }
    }
}