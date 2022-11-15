console.log("Sanity check!");

// Get Stripe publishable key
fetch("/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#gold").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/payments/award/gold/price_1Lx8MODySp54NhVdcJPFryhh/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
  document.querySelector("#silver").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/payments/award/silver/price_1Lx8M9DySp54NhVd0ZRf5KaM/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
  document.querySelector("#bronze").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/payments/award/bronze/price_1LvfBxDySp54NhVdXxcRmTg9/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.file-droppable').forEach(function(droppable) {
      var originalText = droppable.querySelector('div').innerHTML;
      var input = droppable.querySelector('input');
      var fileChanged = function() {
        var files = input.files;
        if (files.length) {
          droppable.querySelector('span').style.display = 'block';
          droppable.querySelector('#image-upload-preview').style.display = 'block';
          droppable.querySelector('div').innerHTML = '';
        //           for (var i = 0; i < files.length; i++) {
        //               droppable.querySelector('div').innerHTML += files[i].name + '<br>';
        //   }
          droppable.classList.add('filled');
          
        } else {
          droppable.querySelector('div').innerHTML = originalText;
          droppable.classList.remove('filled');
          droppable.querySelector('span').style.display = 'none';
          droppable.querySelector('#image-upload-preview').style.display = 'none';
        }
      };
      input.addEventListener('change', fileChanged);
      fileChanged(input);
      droppable.querySelector('span').addEventListener('click', function() {
            input.value = '';
          fileChanged(input);
      });
    });
  });

function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        $('#image-upload-preview').attr('src', e.target.result);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }

function hideComment(id) {
    var id = id.slice(11);
    var comment = document.getElementById('comment' + id);
    var info = document.getElementById('infoComment' + id);
    var collapse = document.getElementById('hideComment' + id)
    comment.style.display = "none";
    info.style.display = "block";
    collapse.style.display = "none";
}

function showComment(id) {
    var id = id.slice(11);
    var comment = document.getElementById('comment' + id);
    var info = document.getElementById('infoComment' + id);
    var collapse = document.getElementById('hideComment' + id);
    comment.style.display = "block";
    info.style.display = "none";
    collapse.style.display = "block";
}