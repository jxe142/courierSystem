var breakpoint = {
  refreshValue: function() {
    this.value = window.getComputedStyle(document.querySelector('body'), ':before').getPropertyValue('content').replace(/\"/g, '');
  }
};

$(window).resize(function() {
  breakpoint.refreshValue();
}).resize();


// This for dev, show breakpoint to title
/*var doc_title = document.title;
$(window).resize(function() {
  document.title = '('+breakpoint.value+') '+doc_title;
}).resize();*/

$(function() {
  // make dropdown behaviour like select element
  $('[data-select]').each(function() {
    var This     = $(this);
    var Select   = $('#'+This.data('select'));
    var Toggle   = This.parent().find('.dropdown-toggle');
    var Item     = This.find('.dropdown-item');
    var Selected = This.find('[data-value="'+Select.val()+'"]');
  
    Toggle.html(Selected.html()); // set dropdown toggle based on selected value
  
    Item.click(function(){
      if ($(this).data('value') != Select.val()) {
        Toggle.html($(this).html()); // update dropdown-toggle content
        Select.val($(this).data('value')).trigger('change'); // update value, trigger change event
      }
      Toggle.focus(); // Keep focused
    });
  
    // Focused selected item when dropdown shown
    This.parent().on('shown.bs.dropdown', function () {
      This.find('[data-value="'+Select.val()+'"]').trigger('focus');
    });
  });
  // make header 'sticky' using fixed position for cross browser compatibility
  var header  = $('.middle-header');
  var wrapper = $('<div id="wrapper"></div>'); header.before(wrapper);
  var ost     = wrapper.offset().top;
  var fixtop  = 'fixed-top';
  var last    = $(window).scrollTop();
  
  $(window).on('load scroll resize', function() {
    var headerHeight = header.outerHeight(), scrollTop = $(this).scrollTop();
    if (scrollTop < last) {
      if (scrollTop <= ost) {
        header.hasClass(fixtop) && header.removeClass(fixtop);
        wrapper.height(0);
      }
    } else {
      if (scrollTop >= ost + headerHeight + 20) {
        header.addClass(fixtop);
        wrapper.height(headerHeight);
      };
    };
    last = scrollTop;
  });
  // Show dropdown on hover
  $('.main-nav .nav-item.dropdown').hover(function() {
    $(this).addClass('show').find('> .dropdown-menu').addClass('show');
  }, function() {
    $(this).removeClass('show').find('> .dropdown-menu').removeClass('show');
  });
  toggleSearch = function() {
    $('.input-search-wrapper').toggleClass('invisible');
    $('#input-search').typeahead('val', '').focus();
  }
  
  $('.toggle-search').click(function(e) {
    toggleSearch();
    e.preventDefault();
    e.stopPropagation();
  });
  
  $('#input-search').keyup(function(e) {
    if (e.keyCode === 27) {
      toggleSearch(); // close with esc key
    }
  });
  var cat1 = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: 'https://raw.githubusercontent.com/mimity-example/json/master/cat1.json?token='+Math.random()
  });
  
  var cat2 = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: 'https://raw.githubusercontent.com/mimity-example/json/master/cat2.json?token='+Math.random()
  });
  
  $('#input-search').typeahead({
    highlight: true
  },
  {
    name: 'category-1',
    display: 'name',
    source: cat1,
    templates: {
      header: '<h6 class="dropdown-header">Category 1</h6>'
    }
  },
  {
    name: 'category-2',
    display: 'name',
    source: cat2,
    templates: {
      header: '<h6 class="dropdown-header">Category 2</h6>'
    }
  });
  
  if ($('#inputCountry').length) {
    var countries = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: {
        url: 'https://raw.githubusercontent.com/mimity-example/json/master/countries.json?token='+Math.random()
      }
    });
  
    countries.initialize();
  
    $('#inputCountry').typeahead({
        highlight: true
    }, {
        displayKey: 'name',
        source: countries.ttAdapter()
    });
  }
  
  // Setup for responsive image height
  var swiperCover = function() {
    $('[data-cover]').each(function() {
      var swiperCover = $(this);
      swiperCover.css('background-image', 'url(' + decodeURIComponent(swiperCover.data('cover')) + ')');
      swiperCover.attr('data-height') && swiperCover.css('height', swiperCover.data('height'));
      switch (breakpoint.value) {
        case 'xs': swiperCover.attr('data-xs-height') && swiperCover.css('height', swiperCover.data('xs-height')); break;
        case 'sm': swiperCover.attr('data-sm-height') && swiperCover.css('height', swiperCover.data('sm-height')); break;
        case 'md': swiperCover.attr('data-md-height') && swiperCover.css('height', swiperCover.data('md-height')); break;
        case 'lg': swiperCover.attr('data-lg-height') && swiperCover.css('height', swiperCover.data('lg-height')); break;
        case 'xl': swiperCover.attr('data-xl-height') && swiperCover.css('height', swiperCover.data('xl-height')); break;
      }
    });
  }
  $(window).resize(function() {
    swiperCover();
  });
  swiperCover();
  
  
  // Home Slider
  if ($('.home-slider').length && typeof Swiper !== 'undefined') {
    var homeSlider = new Swiper ('.home-slider', {
      loop: true,
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        prevEl: '#home-slider-prev',
        nextEl: '#home-slider-next',
      },
      autoplay: {
        delay: 2500,
        disableOnInteraction: false,
      },
      on: {
        init: function() {
          setTimeout(function() {
            $('.home-slider').find('.swiper-slide-active .animate').each(function() {
              $(this).addClass($(this).data('animate')).addClass('visible');
            });
          }, 100);
        },
      }
    });
    homeSlider.on('slideChange', function() {
      homeSlider.slides.find('.animate').each(function() {
        $(this).removeClass($(this).data('animate')).removeClass('visible');
      });
      $(homeSlider.slides[homeSlider.activeIndex]).find('.animate').each(function() {
        $(this).addClass($(this).data('animate')).addClass('visible');
      });
    });
  }
  
  
  // Brand Slider
  if ($('#brand-slider').length && typeof Swiper !== 'undefined') {
    var brandSlider = new Swiper('#brand-slider', {
      navigation: {
        prevEl: '#brand-slider-prev',
        nextEl: '#brand-slider-next',
      },
      slidesPerView: 5,
      spaceBetween: 15,
      slidesPerColumn: 2,
      breakpoints: {
        767: {
          // sm
          slidesPerView: 2,
        },
        991: {
          // md
          slidesPerView: 3,
        },
        1199: {
          // lg
          slidesPerView: 4,
        }
      }
    });
  }
  
  
  // New In Slider
  if ($('#newIn-slider').length && typeof Swiper !== 'undefined') {
    var newInSlider = new Swiper('#newIn-slider', {
      navigation: {
        prevEl: '#newInPrev',
        nextEl: '#newInNext',
      },
      slidesPerView: 6,
      spaceBetween: 30,
      breakpoints: {
        575: {
          // xs
          slidesPerView: 2,
          spaceBetween: 8,
        },
        767: {
          // sm
          slidesPerView: 3,
          spaceBetween: 8,
        },
        991: {
          // md
          slidesPerView: 4,
          spaceBetween: 8,
        },
        1199: {
          // lg
          slidesPerView: 5,
        }
      }
    });
  }
  
  // Quickview Slider
  if ($('#quickview-slider').length && typeof Swiper != undefined) {
    var quickviewSlider = new Swiper ('#quickview-slider', {
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        prevEl: '#quickview-prev',
        nextEl: '#quickview-next',
      },
      lazy: true
    });
    $('#quickviewModal').on('shown.bs.modal', function (e) {
      quickviewSlider.update();
    });
  }
  
  
  // Price Range Slider
  if ($('#price-range-slider').length && typeof Swiper !== 'undefined') {
    var priceRange = document.getElementById('price-range-slider');
    noUiSlider.create(priceRange, {
      start: [20, 80],
      connect: true,
      range: {
        'min': 0,
        'max': 100
      }
    });
    priceRange.noUiSlider.on('update', function(values, handle) {
      var value = values[handle];
      handle ? $('#max-price').val(Math.round(value)).attr('value', Math.round(value)) : $('#min-price').val(Math.round(value)).attr('value', Math.round(value));
    });
    $('#max-price').on('change', function() {
      priceRange.noUiSlider.set([null, this.value]);
    });
    $('#min-price').on('change', function() {
      priceRange.noUiSlider.set([this.value, null]);
    });
  }
  
  
  // Rating Range Slider
  if ($('#rating-range').length && typeof Swiper !== 'undefined') {
    var ratingRange = document.getElementById('rating-range');
    noUiSlider.create(ratingRange, {
      start: [$('#min-range').val(), $('#max-range').val()],
      connect: true,
      orientation: 'vertical',
      snap: true,
      direction: 'rtl',
      range: {
        'min': 1,
        '25%': 2,
        '50%': 3,
        '75%': 4,
        'max': 5,
      },
      pips: {
        mode: 'values',
        values: [1, 2, 3, 4, 5]
      }
    });
    ratingRange.noUiSlider.on('update', function(values, handle) {
      var ratingDom = $('#rating-range');
      ratingDom.find('.noUi-value[style="bottom: 100%;"]').html('<div class="rating"><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i></div>');
      ratingDom.find('.noUi-value[style="bottom: 75%;"]').html('<div class="rating"><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i></div>');
      ratingDom.find('.noUi-value[style="bottom: 50%;"]').html('<div class="rating"><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i></div>');
      ratingDom.find('.noUi-value[style="bottom: 25%;"]').html('<div class="rating"><i class="material-icons md-1 align-text-top">star_border</i><i class="material-icons md-1 align-text-top">star_border</i></div>');
      ratingDom.find('.noUi-value[style="bottom: 0%;"]').html('<div class="rating"><i class="material-icons md-1 align-text-top">star_border</i></div>');
      var value = values[handle];
      handle ? $('#max-range').val(Math.round(value)).attr('value', Math.round(value)) : $('#min-range').val(Math.round(value)).attr('value', Math.round(value));
      var min_range = $('#min-range').val();
      var max_range = $('#max-range').val();
      var max_range = max_range == '' ? min_range : max_range;
      for (var i = min_range; i < parseInt(max_range) + 1; i++) {
        switch(i) {
          case 5: case '5': var percent = '100%'; break;
          case 4: case '4': var percent = '75%'; break;
          case 3: case '3': var percent = '50%'; break;
          case 2: case '2': var percent = '25%'; break;
          case 1: case '1': var percent = '0%'; break;
        }
        ratingDom.find('.noUi-value[style="bottom: '+percent+';"]').find('.material-icons').text('star');
      }
    });
    $('#max-range').on('change', function() {
      ratingRange.noUiSlider.set([null, this.value]);
    });
    $('#min-range').on('change', function() {
      ratingRange.noUiSlider.set([this.value, null]);
    });
  }
  // example countdown 6 hours from now for flash sale
  var countdown = new Date(); countdown.setHours(countdown.getHours() + 6);
  if ($('#flash-sale-countdown').length) {
    $('#flash-sale-countdown').countdown(countdown, function(event) {
      $(this).text(event.strftime('%H:%M:%S'));
    });
  }
  $('.input-group-qty').each(function() {
    var that = $(this),
        input = that.find('input[type="text"]'),
        down = that.find('.btn-down'),
        up = that.find('.btn-up'),
        min = input.data('min'),
        max = input.data('max'),
        min = (min == undefined) || (min == '') || (min < 0) ? 0 : min,
        max = (max == undefined) || (max == '') || (max < 0) ? 1000 : max; // maximum 1000 qty
    input.change(function() {
      if (!$.isNumeric($(this).val()) || $(this).val() < min) {
        $(this).val(min);
      } else if ($(this).val() > max) {
        $(this).val(max);
      }
    });
    up.click(function() {
      input.val(parseInt(input.val()) + 1).trigger('change');
    });
    down.click(function() {
      input.val(parseInt(input.val()) - 1).trigger('change');
    });
  });
  
  // select all on focus
  $('.input-group-qty input').on('focus', function() {
      $(this).one('mouseup', function() {
        $(this).select();
        return false;
      }).select();
  });
  // Detail Slider
  if ($('#detail-slider').length && typeof Swiper != undefined) {
    var detailSlider = new Swiper ('#detail-slider', {
      on: {
        init: function() {
          setTimeout(function() {
            $('.detail-gallery .swiper-slide:first-child .img-thumbnail').addClass('active');
          }, 100);
        },
      }
    });
    detailSlider.on('slideChange', function() {
      detailGallery.slideTo(detailSlider.activeIndex);
      $('.detail-gallery .swiper-slide .img-thumbnail').removeClass('active');
      $('.detail-gallery .swiper-slide').eq(detailSlider.activeIndex).find('.img-thumbnail').addClass('active');
    });
  }
  
  
  // Detail Gallery
  if ($('#detail-gallery').length && typeof Swiper != undefined) {
    var detailGallery = new Swiper ('#detail-gallery', {
      slidesPerView: 4,
      spaceBetween: 5,
      navigation: {
        prevEl: '#detail-gallery-prev',
        nextEl: '#detail-gallery-next',
      }
    });
    if ($('.detail-gallery .swiper-slide').length <= 4) {
      $('#detail-gallery-prev, #detail-gallery-next').remove();
    }
  }
  
  $('.detail-gallery .swiper-slide a').click(function(event) {
    detailSlider.slideTo( $('.detail-gallery .swiper-slide a').index(this) );
    event.preventDefault();
  });
  
  
  var parseThumbnailElements = function() {
    var items = [];
    $('#detail-slider img').each(function(index, el) {
      item = {
        src: el.getAttribute('src'),
        w: parseInt(el.getAttribute('data-width'), 10),
        h: parseInt(el.getAttribute('data-height'), 10)
      };
      items.push(item);
    });
    return items;
  }
  
  
  var openPhotoSwipe = function(activeIndex) {
    activeIndex = typeof activeIndex !== 'undefined' ? activeIndex : 0;
    var pswpElement = document.querySelectorAll('.pswp')[0];
    var items = parseThumbnailElements();
    var options = {
        index: activeIndex
    };
    var gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
    gallery.init();
  }
  
  
  $('.btn-zoom').click(function(event) {
    openPhotoSwipe(detailSlider.activeIndex);
    event.preventDefault();
  });
  
  // Back to Top
  $(window).scroll(function() {
    if ($(this).scrollTop() > 200) {
      $('.back-top').fadeIn();
    } else {
      $('.back-top').fadeOut();
    }
  });
  $('#back-top').click(function(e) {
  	$('body, html').animate({
  		scrollTop:0
  	}, 500);
  	e.preventDefault();
  });
  if ($('.rating-review').length) {
    $('.rating-review').raty({
      half: true,
      scoreName: 'rating-review',
      path: 'img/raty'
    });
  }
  $('[data-toggle="tooltip"]').tooltip();

  // show static quickview for demo purpose
  $('.show-quickview').click(function(event) {
    $('#quickviewModal').modal('show');
  });
});