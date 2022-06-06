/*!
 * Start Bootstrap - Stylish Portfolio v5.1.0 (https://startbootstrap.com/theme/stylish-portfolio)
 * Copyright 2013-2021 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-stylish-portfolio/blob/master/LICENSE)
 */
$(document).ready(function() {
    $('a[name=modal]').click(function(e) {
        e.preventDefault();
        var id = $(this).attr('href');
        var winH = $(window).height();
        var winW = $(window).width();
        $(id).css('top', winH / 2 - $(id).height() / 2);
        $(id).css('left', winW / 2 - $(id).width() / 2);
        $(id).fadeIn(500);
    });

    $('.modalwindow .close').click(function(e) {
        e.preventDefault();
        $('.modalwindow').fadeOut(500);
    });
    $('.modalwindow .buy-btn').click(function(e) {
        e.preventDefault();
        $('.modalwindow').fadeOut(500);
    });
});
$('input.input-qty').each(function() {
        var $this = $(this),
            qty = $this.parent().find('.is-form'),
            min = Number($this.attr('min')),
            max = Number($this.attr('max'))
        if (min == 0) {
            var d = 0
        } else d = min
        $(qty).on('click', function() {
            if ($(this).hasClass('minus')) {
                if (d > min) d += -1
            } else if ($(this).hasClass('plus')) {
                var x = Number($this.val()) + 1
                if (x <= max) d += 1
            }
            $this.attr('value', d).val(d)
        })
    })
    /*! Xoa SL da chon */
    /*! Mua bap nuoc */
function BuyBapMy() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Bắp Mỹ: ';
    html += document.getElementById('BapMy').value;
    // Gán kết quả vào div#result
    document.getElementById('result1').innerHTML = html;
}

function BuyBapNuong() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Bắp Nướng: ';
    html += document.getElementById('BapNuong').value;
    // Gán kết quả vào div#result
    document.getElementById('result2').innerHTML = html;
}

function BuySuoi() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Nước suối: ';
    html += document.getElementById('suoi').value;
    // Gán kết quả vào div#result
    document.getElementById('result4').innerHTML = html;
}

function BuyBapSay() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Bắp sấy: ';
    html += document.getElementById('BapSay').value;
    // Gán kết quả vào div#result
    document.getElementById('result3').innerHTML = html;
}

function Buypepsi() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'Pepsi: ';
    html += document.getElementById('pepsi').value;
    // Gán kết quả vào div#result
    document.getElementById('result5').innerHTML = html;
}

function BuyCoca() {
    // // Biến lưu trữ các chuyên mục đa chọn
    var html = 'CoCa CoLa: ';
    html += document.getElementById('Coca').value;
    // Gán kết quả vào div#result
    document.getElementById('result6').innerHTML = html;
}
/*! */
(function($) {
    "use strict"; // Start of use strict

    // Closes the sidebar menu
    $(".menu-toggle").click(function(e) {
        e.preventDefault();
        $("#sidebar-wrapper").toggleClass("active");
        $(".menu-toggle > .fa-bars, .menu-toggle > .fa-times").toggleClass("fa-bars fa-times");
        $(this).toggleClass("active");
    });

    // Smooth scrolling using anime.js
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').on('click', function() {
        if (
            location.pathname.replace(/^\//, "") ==
            this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length ?
                target :
                $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                anime({
                    targets: 'html, body',
                    scrollTop: target.offset().top,
                    duration: 1000,
                    easing: 'easeInOutExpo'
                });
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").on('click', function() {
        $(".navbar-collapse").collapse("hide");
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('#sidebar-wrapper .js-scroll-trigger').click(function() {
        $("#sidebar-wrapper").removeClass("active");
        $(".menu-toggle").removeClass("active");
        $(".menu-toggle > .fa-bars, .menu-toggle > .fa-times").toggleClass("fa-bars fa-times");
    });

    // Scroll to top button appear
    $(document).scroll(function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });

})(jQuery); // End of use strict


// Disable Google Maps scrolling
// See http://stackoverflow.com/a/25904582/1607849
// Disable scroll zooming and bind back the click event
var onMapMouseleaveHandler = function(event) {
    var that = $(this);
    that.on('click', onMapClickHandler);
    that.off('mouseleave', onMapMouseleaveHandler);
    that.find('iframe').css("pointer-events", "none");
}
var onMapClickHandler = function(event) {
        var that = $(this);
        // Disable the click handler until the user leaves the map area
        that.off('click', onMapClickHandler);
        // Enable scrolling zoom
        that.find('iframe').css("pointer-events", "auto");
        // Handle the mouse leave event
        that.on('mouseleave', onMapMouseleaveHandler);
    }
    // Enable map zooming with mouse scroll when the user clicks the map
$('.map').on('click', onMapClickHandler);