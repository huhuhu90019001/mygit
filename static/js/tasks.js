/*
job execute
 */
// console.log('tasks,' + site_url + ',' + static_url)
function execute_task (obj) {
    if ($(obj).hasClass('king-disabled')) {
        return false
    }
    $('div[tips]').text('')
    var business_id = $('input[name=tag_s_cc_business_id]').val()
    var iplist = $('input[name=tag_s_cc_ip]').val()
    if (!business_id) {
        $('div[tips=tag_s_cc_business_id]').text('Please select the business')
        return
    }
    if (!iplist) {
        $('div[tips=tag_s_cc_ip]').text('Please select the ip')
        return
    }
    console.log(business_id, iplist)
    var job_task_id = $('input[name=tag_job_id]').val()
    if (!job_task_id) {
        $('div[tips=tag_job_id]').text('Please select the job')
        return
    }
    console.log(job_task_id)
    var url = site_url + "task/excute_ijob_task/"
    var param = {
        'business_id': business_id,
        'job_task_id': job_task_id,
        'iplist': iplist
    }
    $(obj).addClass('king-disabled')
    $(obj).html('<img alt="loadding" style="margin-right:3px;" src="' + static_url + 'img/loading.gif">提交中')
    $.post(url, param, function (res) {
        console.log(res)
        if (res.result) {
            get_task_status(res.task_instance_id, obj)
        } else {
            console.log(res.msg)
            $("#excute_task_tips").html(res.msg)
        }
    }, 'json')
}

function get_task_status (task_instance_id, sumbit_obj) {
    $.post(site_url + "task/get_task_status/", { 'task_instance_id': task_instance_id }, function (res) {
        if (res.result) {
            $(sumbit_obj).html('<img alt="loadding" style="margin-right:3px;" src="' + static_url + 'img/loading.gif">执行中')
            console.log(res.end)
            if (!res.end) {
                setTimeout(function () { get_task_status(task_instance_id, sumbit_obj) }, 1 * 1000)
            } else {
                $(sumbit_obj).removeClass('king-disabled')
                $(sumbit_obj).html('submit')
            }
            $("#task_flow").html(res.data)
        } else {
            console.log('failed：' + res.data)
            $(sumbit_obj).html('submit')
            $(sumbit_obj).removeClass('king-disabled')
        }
    }, 'json')
}


/*
Game data
 */
function _refresh_data (url, datatype, obj) {
    var _chart = $(obj).data("kendoChart")
    $.ajax({
        url: url,
        type: 'GET',
        dataType: datatype,
        jsonpCallback: 'lineChartCallback',
        success: function (res) {
            console.log(res)
            try {
                var new_data = _chart.options.series[0].data.concat(res.data.series[0].data)
                var new_time = _chart.options.categoryAxis.categories.concat(res.data.categories)
                var len = _chart.options.categoryAxis.categories.length
                if (len > 30) {
                    new_data.shift()
                    new_time.shift()
                }
                _chart.options.categoryAxis.categories = new_time
                _chart.options.series[0].data = new_data
                _chart.options.categoryAxis.labels.step = 3
                _chart.refresh()
            } catch (err) {
                console.log(err)
            }
        }
    })
}

function refresh_gamedata (url, obj) {
    setInterval(function () {
        _refresh_data(url, 'json', obj)
    }, 1 * 1000)
}

function _refresh_gamedata_rank (url, datatype, obj) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: datatype,
        jsonpCallback: 'rangerCallback',
        success: function (res) {
            var _html = ''
            var list = res.data
            if (list.length == 0) {
                _html = '<tr><td colspan="3">No Data</td></tr>'
            } else {
                for (var i = 0, len = list.length; i < len; i++) {
                    var item = list[i]
                    _html += '<tr><td style="width:42px;">' + item.index + '</td><td style="width:40%;">' + item.name + '</td><td>' + item.score + '</td></tr>'
                }
            }
            $(obj).html(_html)
        }
    })

}

function refresh_gamedata_rank (url, obj) {
    setInterval( function () {
        _refresh_gamedata_rank(url, 'json', obj)
    }, 1 * 1000)
}

$( function () {
    refresh_gamedata(site_url + 'game_data/get_online/', '#online')
    refresh_gamedata(site_url + 'game_data/get_gold/', '#gold')
    refresh_gamedata_rank(site_url + 'game_data/get_ranking/', '#ranking .ranger-box tbody')
})