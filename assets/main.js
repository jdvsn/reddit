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
