"use strict";

$("form").on("submit", handleAddCupcake);

const $cupCakeContainer = $(".cupcake-container");

async function handleAddCupcake(event) {
  event.preventDefault();

  const $flavor = $("#flavor").val();
  const $size = $("#size").val();
  const $rating = $("#rating").val();
  const $imageURL = $("#image_url").val();

  const response = await axios.post(`/api/cupcakes`, {
    flavor: $flavor,
    size: $size,
    rating: $rating,
    image_url: $imageURL,
  });

  const cupcakes = await axios.get("/api/cupcakes");
  console.log("CUPCAKES", cupcakes.data.cupcakes);

  cupcakes.data.cupcakes.map((cupcake) => renderCupcake(cupcake));
}

function renderCupcake(cupCake) {
  let $cupCake = $(
    `<div>
        <img src="${cupCake.image_url}" alt="picture of cupCake">
        <p>This ${cupCake.flavor} cupCake is a ${cupCake.size} and has a rating of ${cupCake.rating} out of 10</p>
        </div>`
  );

  $cupCakeContainer.append($cupCake);
}
