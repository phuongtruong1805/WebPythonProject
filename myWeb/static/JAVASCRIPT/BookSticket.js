$(document).ready(function() {
    $(".outer-seat").on("click", function() {
        var x=''
        $(this).toggleClass('selected-outerColor');

        var qty = $('.selected-outerColor').length;
        $(".count-selected span").text(qty);

        var tx = $('.selected-outerColor').text();
        $(".text-selected span").text(tx);
        x=x+$(".text-selected span").text(tx);
    });

    $(".inner-seat").on("click", function() {
        $(this).toggleClass('selected-innerColor');
    });


});

function validateSelectBox0(obj) {

    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Chọn ngày xem: ';
    html += document.getElementById('dateshow').value;
    // Gán kết quả vào div#result
    document.getElementById('result0').innerHTML = html;
}

function validateSelectBox1(obj) {
    // Lấy danh sách các options
    var options = obj.children;

    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Rạp phim: ';

    // // lặp qua từng option và kiểm tra thuộc tính selected
    for (var i = 0; i < options.length; i++) {
        if (options[i].selected) {
            html += options[i].text;
        }
    }
    // Gán kết quả vào div#result
    document.getElementById('result1').innerHTML = html;
}
