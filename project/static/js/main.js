
function chk_update()
{

    var select_update = document.getElementById('job')
    var btn_group = document.getElementById('word')

    if (select_update.value == 'auto')
    {
        data('auto')
        btn_group.style.display = "";
        return 'auto';
    }
    else if (select_update.value =='news')
    {
        data('news')
        btn_group.style.display = "";
        return 'news';
    }
    else if (select_update.value == 'dealer')
    {
        data('dealer')
        btn_group.style.display = "";
        return 'dealer';
    }
    else if (select_update.value =='xiala')
    {
        data('xiala')
        btn_group.style.display = "";
        return 'xiala';
    }
    else if (select_update.value == 'emao')
    {
        data('emao')
       btn_group.style.display = "";
       return 'emao';
    }

}

function data(branch)
{
    $.ajax({
    type: "POST",
    url: "http://127.0.0.1:5000/brush",
    //contentType: "application/json;charset=utf-8",
    dataType: "json",
    data:{'location': branch},
    success: function(data){
        //handle data
    }
});
}


function search(type)
{


    var keyword = $("keyword").val()
    var url = $("url").val()
    //var buttonValue= document.getElementById('insertBtn').value;
    //var searchtime = document.getElementById('searchtime')
    if (type == 'confirm' && (keyword == "none" || url == "none"))
        alert('必须输入搜索关键词和URL')
        return false
    return true

    //$.ajax({
    //    type: "POST",
    //    url: "http://127.0.0.1:5000/reports/detail",
    //    //contentType: "application/json;charset=utf-8",
    //    dataType: "json",
    //    data: {'usertype': JSON.stringify(usertype), 'searchtype': searchtype, 'searchtime': searchtime},
    //    success: function (data) {
    //        //handle data
    //    }
    //});

}