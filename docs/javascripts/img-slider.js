$( document ).ready(function() {
    load_image_before_after_slider();
});

function load_image_before_after_slider()
{
    $(".background-img, .foreground-img").each(function() {
        img = $(this).attr("data");
        $(this).css('background-image', "url('../../assets/images/" + img + "')");
    });

    $(".img-slider").on("input change", (e)=>{
      const sliderPos = e.target.value;
      // Update the width of the foreground image
      $( e.target ).prev('.foreground-img').css('width', `${sliderPos}%`);
      // Update the position of the slider button
      $( e.target ).next('.slider-button').css('left', `calc(${sliderPos}% - 16px)`);
      // Update the position of the slider button
      $( e.target ).next('.slider-bar').css('left', `calc(${sliderPos}% - 4px)`);
    });
}

document$.subscribe(() => { load_image_before_after_slider(); })