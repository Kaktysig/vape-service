function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ChangeLiquidsList(e){
    var lain_id = $(e).val();
    if (lain_id == 0){
        var url = "/liquids/api/liquids/list";
    }
    else {
        var url = "/liquids/api/liquids/list?id=" + lain_id;
    }
    var row = $(e).parents('.outs-item');
    var liquids = row.find('select[name="name_ex"]');
    $.ajax({
        type: "GET",
        url: url,
        dataType: 'json',
        success: function (data) {
            for (var index in liquids.children().get()){
                if (index > 0){
                    $(liquids.children().get(1)).remove();
                }
            }
            for (var index in data){
                liquids.append('<option value="' + data[index].id  +'">' + data[index].name_ex + '</option>')
            }
        }
    });
}


$(document).ready(function () {
    $('.send-outs').click(function () {
        var btn_outs = $(this);
        var outs = $('.out-card');
        var o_form = $('.out-form');

        var formdata = o_form.serializeArray();
        var outs_post = {};
        $(formdata ).each(function(index, obj){
            outs_post[obj.name] = obj.value;
        });

        var o_inputs = o_form.find("input[type='checkbox']");
        o_inputs.attr('disabled','disabled');
        btn_outs.attr('disabled','disabled');

        var delivery = $('.delivery-card');
        var div_delivery = $('.divbtn-delivery');
        var btn_delivery = div_delivery.find('button');
        delivery.removeClass('d-none');
        delivery.addClass('animated').addClass('bounceInDown');
        div_delivery.removeClass('d-none');
        div_delivery.addClass('animated').addClass('bounceInDown');

        btn_delivery.click(function () {
            var d_inputs = delivery.find('input, select');
            var delivery_form = delivery.find('form');
            var formdata = delivery_form.serializeArray();
            var delivery_post = {};
            $(formdata ).each(function(index, obj){
                delivery_post[obj.name] = obj.value;
            });


            d_inputs.attr('disabled','disabled');
            $(this).attr('disabled','disabled');

            $.ajax({
                type: "POST",
                url: "/order/delivery",
                headers: {"X-CSRFToken": csrftoken},
                dataType: 'json',
                data: {
                    'id': o_form.data('id'),
                    'outs' : JSON.stringify(outs_post),
                    'delivery': JSON.stringify(delivery_post),
                },
                success:  function (data, textStatus, jqXHR) {
                if (jqXHR.status == 200){
                    outs.addClass('animated').addClass('bounceOutUp');
                    btn_outs.addClass('animated').addClass('bounceOutUp');
                    delivery.addClass('bounceOutUp');
                    div_delivery.addClass('bounceOutUp');
                    setTimeout(function () {
                        outs.addClass('d-none');
                        btn_outs.addClass('d-none');
                        delivery.addClass('d-none');
                        div_delivery.addClass('d-none');
                        $('.card-ok').removeClass('d-none');
                    },750);
                }
            }

            });
        });
    });
    $('.add-another-row').click(function () {
        var row = $('.d-none.outs-item');
        var outs = $('.outs-rows');
        var new_row = row.clone();
        new_row.removeClass('d-none');
        new_row.appendTo(outs);
    });
    $('.btn-create-order').click(function () {
        $(this).attr('disabled','disabled');
        $('.d-none.outs-item').removeClass('outs-item');
        var outs = $('.outs-item');
        outs_data = {};
        var index = 1;
        outs.each(function () {
            var row={};
            $(this).find('input,select,textarea').each(function(){
                row[$(this).attr('name')]=$(this).val();
            });
            outs_data[index]=row;
            index++;
        });
        var order_post = {};
        var order_form = $('.order-form').serializeArray();
        $(order_form).each(function(index, obj){
            order_post[obj.name] = obj.value;
        });
        data = {};
        data['outs'] = outs_data;
        data['order'] = order_post;
        $.ajax({
            type: "POST",
            url: "/order/add",
            headers: {"X-CSRFToken": csrftoken},
            dataType: 'json',
            data: {
                'data': JSON.stringify(data),
            },
            success: function (data, textStatus, jqXHR) {
                if (jqXHR.status == 200){
                    window.location.replace("/order/detail/" + data['order_id']);
                }
            }
        });
    });
});
