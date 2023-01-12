const swiper_product = new Swiper(".swiper_product", {
  zoom: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});


const swiper_main_product = new Swiper(".swiper_main_product", {
    watchSlidesProgress: true,
    lazy: true,
    slidesPerView: 5,
    spaceBetween: 30,
    slidesPerGroup: 1,
    loop: true,
    navigation: {
      nextEl: ".swiper-button-slick-next",
      prevEl: ".swiper-button-slick-prev"
    }
});


const swiper_main_product_mobile = new Swiper(".swiper_main_product_mobile", {
    watchSlidesProgress: true,
    lazy: true,
    slidesPerView: 2,
    spaceBetween: 30,
    slidesPerGroup: 1,
    loop: true,
    navigation: {
      nextEl: ".swiper-button-slick-next",
      prevEl: ".swiper-button-slick-prev"
    }
});


const swiper_main = new Swiper(".swiper_main", {
  autoplay: {
    delay: 3000,
    disableOnInteraction: true,
  },
  effect: "fade",
  loop: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
