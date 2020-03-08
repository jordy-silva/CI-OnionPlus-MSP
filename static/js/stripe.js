// Copyright (c) 2019- Stripe, Inc. (https://stripe.com)

// Original file: https://github.com/stripe-samples/accept-a-card-payment/blob/master/using-webhooks/client/web/script.js

// Some changes have been done to this file by the student to adapt it to the use case, specially to allow the user of the webapp to enter an amount to pay by themselves and add the amount to the previous funding amount without requiring a reload of the page.

// A reference to Stripe.js
var stripe;

var orderData = {
  amount: (document.getElementById("amount").value) * 100,
  currency: "eur",
  ticket: (document.getElementById("ticket").value)
};

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

fetch("/payments/create-payment-intent", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(orderData)
})
  .then(function (result) {
    return result.json();
  })
  .then(function (data) {
    return setupElements(data);
  })
  .then(function ({ stripe, card, clientSecret, intentID }) {
    document.querySelector("button").disabled = false;
    // Handle form submission.
    var form = document.getElementById("payment-form");
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      // Update intent amount and initiate payment when the submit button is clicked
      var orderData = {
        amount: (document.getElementById("amount").value) * 100,
        intentID: intentID
      };
      fetch("/payments/update-payment-intent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(orderData)
      })
        .then(function (result) {
          return result.json();
        })
        .then(function () {
          // Initiate payment
          pay(stripe, card, clientSecret);
        });
    });
  });

// Set up Stripe.js and Elements to use in checkout form
var setupElements = function (data) {
  stripe = Stripe(data.publishableKey);
  var elements = stripe.elements();
  var style = {
    base: {
      color: "#32325d",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4"
      }
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a"
    }
  };

  var card = elements.create("card", { style: style, hidePostalCode: true });
  card.mount("#card-element");

  return {
    stripe: stripe,
    card: card,
    clientSecret: data.clientSecret,
    intentID: data.intentID
  };
};

/*
 * Calls stripe.confirmCardPayment which creates a pop-up modal to
 * prompt the user to enter extra authentication details without leaving your page
 */
var pay = function (stripe, card, clientSecret) {
  changeLoadingState(true);

  // Initiate the payment.
  // If authentication is required, confirmCardPayment will automatically display a modal
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function (result) {
      if (result.error) {
        // Show error
        showError(result.error.message);
      } else {
        // The payment has been processed
        orderComplete(clientSecret);
      }
    });
};

/* ------- Post-payment helpers ------- */

/* Shows a success / error message when the payment is complete */
var orderComplete = function (clientSecret) {
  // We update the total amount of funding shown on the page, but database is updated securely via webhook
  stripe.retrievePaymentIntent(clientSecret).then(function (result) {
    var paymentIntent = result.paymentIntent;

    let amount = document.getElementById("funding").innerHTML;
    amount = parseFloat(amount.slice(0, -2));
    amount += (paymentIntent.amount/100);

    document.getElementById("funding").innerHTML = amount + ' €';

    document.querySelector(".sr-payment-form").classList.add("hidden");

    document.querySelector(".sr-result").classList.remove("hidden");

    changeLoadingState(false);
  });
};

var showError = function (errorMsgText) {
  changeLoadingState(false);
  var errorMsg = document.querySelector(".sr-field-error");
  errorMsg.textContent = errorMsgText;
  setTimeout(function () {
    errorMsg.textContent = "";
  }, 5000);
};

// Show a spinner on payment submission
var changeLoadingState = function (isLoading) {
  if (isLoading) {
    document.querySelector("button").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("button").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
};