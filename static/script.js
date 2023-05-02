"use strict"

$('form').on('submit', handleAddCupcake)

async function handleAddCupcake(event) {
    event.preventDefault();

    const $flavor = $('#flavor').val()
    const $size = $('#size').val()
    const $rating = $('#rating').val()
    const $imageURL = $('#image_url').val()


    const response = await axios.post(
        `/api/cupcakes`,
        {
            flavor: $flavor,
            size: $size,
            rating: $rating,
            image_url: $imageURL 
        }
      );
}