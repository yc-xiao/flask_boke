var _url = 'http://localhost:5000'
//上传文件方法
function UpladFile() {
    var fileObj = document.getElementById("file").files[0]; // js 获取文件对象
    search(fileObj);
}

function search(fileObj){
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
            handler_search(data);
        }
        update_process(data);
    }; //请求完成

    xhr.onerror = function(evt){
        console.log("上传失败！");
    }; //请求失败

    xhr.send(); //开始上传，发送form数据
}

var a = 1;
function handler_search(data){
    blocks = data['blocks'];
    console.log(a);
    a+=1;
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

// function handler_searchx(data){
//     blocks = data['blocks'];
//     for(var each in blocks){
//         if(!blocks[each]['status']){
//             var datas = get_datas(each, blocks[each]['start'], blocks[each]['end']);
//             url = "http://localhost:5000/new_upload/";
//             var xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
//             xhr.open('post', url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
//             xhr.onload = function(evt){
//                 //服务断接收完文件返回的结果
//                 var data = JSON.parse(evt.target.responseText);
//
//             }; //请求完成
//             xhr.onerror = function(evt){
//                 console.log("上传失败！");
//             }; //请求失败
//             xhr.send(datas); //开始上传，发送form数据
//
//         }
//     }
// }

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

//上传成功响应
function searchComplete(evt) {
    //服务断接收完文件返回的结果
    var data = JSON.parse(evt.target.responseText);
    if(!data['status']){
        handler_search(data);
    }
}

function update_process(data){
    blocks = data['blocks'];
    var count = 0;
    var total = 0;
    for(var each in blocks){
        total+=1;
        if(blocks[each]['status']){
            count+=1;
        }else{
            console.log(blocks[each]['status'])
        }
    }
    var progressBar = document.getElementById("progressBar");
    var percentageDiv = document.getElementById("percentage");
    progressBar.max = total;
    progressBar.value = count;
    percentageDiv.innerHTML = '上传进度:' + count/total;
}

//上传失败
// function uploadFailed(evt) {
//     console.log("上传失败！");
// }

//取消上传
// function cancleUploadFile(){
//     xhr.abort();
// }

// function http(method, url, data, onprogress){
//     var xhr;
//     xhr = new XMLHttpRequest();  // XMLHttpRequest 对象
//     xhr.open(method, url, true); //post方式，url为服务器请求地址，true 该参数规定请求是否异步处理。
//     xhr.onload = uploadComplete; //请求完成
//     xhr.onerror =  uploadFailed; //请求失败
//     xhr.upload.onprogress = onprogress;//【上传进度调用方法实现】
//     xhr.send(data); //开始上传，发送form数据
// }
//

//上传进度实现方法，上传过程中会频繁调用该方法
// function progressFunction(evt) {
//     var progressBar = document.getElementById("progressBar");
//     var percentageDiv = document.getElementById("percentage");
//     // event.total是需要传输的总字节，event.loaded是已经传输的字节。如果event.lengthComputable不为真，则event.total等于0
//     if (evt.lengthComputable) {//
//         progressBar.max = evt.total;
//         progressBar.value = evt.loaded;
//         percentageDiv.innerHTML = Math.round(evt.loaded / evt.total * 100) + "%";
//     }
//     var time = document.getElementById("time");
//     var nt = new Date().getTime();//获取当前时间
//     var pertime = (nt-ot)/1000; //计算出上次调用该方法时到现在的时间差，单位为s
//     ot = new Date().getTime(); //重新赋值时间，用于下次计算
//     var perload = evt.loaded - oloaded; //计算该分段上传的文件大小，单位b
//     oloaded = evt.loaded;//重新赋值已上传文件大小，用以下次计算
//     //上传速度计算
//     var speed = perload/pertime;//单位b/s
//     var bspeed = speed;
//     var units = 'b/s';//单位名称
//     if(speed/1024>1){
//         speed = speed/1024;
//         units = 'k/s';
//     }
//     if(speed/1024>1){
//         speed = speed/1024;
//         units = 'M/s';
//     }
//     speed = speed.toFixed(1);
//     //剩余时间
//     var resttime = ((evt.total-evt.loaded)/bspeed).toFixed(1);
//     time.innerHTML = '，速度：'+speed+units+'，剩余时间：'+resttime+'s';
//     if(bspeed==0) time.innerHTML = '上传已取消';
// }
