const express = require("express");
const bodyParser = require("body-parser");
const Razorpay = require("razorpay");

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

require('dotenv').config();

// Razorpay configuration
const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID, // Replace with your Razorpay Key ID
    key_secret: process.env.RAZORPAY_KEY_SECRET, // Replace with your Razorpay Key Secret
});

// Serve the feedback form

app.get("/", (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Star Rating Form</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap');
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }
    html, body {
      display: grid;
      height: 100%;
      place-items: center;
      background: #000;
    }
    .form-container {
      width: 400px;
      background: white;
      padding: 20px 30px;
      border: 1px solid #444;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
    }
    .form-container h1 {
      font-size: 25px;
      color: black;
      font-weight: 500;
      margin-bottom: 20px;
    }
    .stars {
      display: flex;
      justify-content: center;
      margin-bottom: 20px;
    }
    .stars input {
      display: none;
    }
    .stars label {
      font-size: 40px;
      color: #444;
      cursor: pointer;
      transition: color 0.2s ease, transform 0.2s ease;
    }
    .stars label:hover,
    .stars label:hover + label {
      color: #fd4;
      transform: scale(1.2);
    }
    .stars input:checked + label {
      color: #444;
    }
    .stars input:checked + label,
    .stars input:checked + label ~ label {
      color: #fd4;
    }
    .input-container {
      width: 100%;
      margin-bottom: 20px;
    }
    input[type="number"] {
      width: 100%;
      padding: 10px;
      border: 1px solid #333;
      background: white;
      color: black;
      border-radius: 5px;
      font-size: 16px;
    }
    input[type="number"]:focus {
      border-color: #444;
      outline: none;
    }
    .btn {
      width: 100%;
      margin-top: 15px;
      
    }
    button {
      width: 100%;
      padding: 10px;
      border: 1px solid #444;
      background: rgb(156, 219, 248);
      border-radius: 20px;
      color: black;
      font-size: 16px;
      font-weight: 500;
      text-transform: uppercase;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    button:hover {
      background: rgb(25, 120, 146);
    }
  </style>
</head>
<body>
  <div class="form-container">
    <h1>Rate Our Service</h1>
    <form action="/submitFeedback" method="POST">
      <div class="stars">
        <input type="radio" id="star5" name="rating" value="5">
        <label for="star5" class="fas fa-star"></label>
        <input type="radio" id="star4" name="rating" value="4">
        <label for="star4" class="fas fa-star"></label>
        <input type="radio" id="star3" name="rating" value="3">
        <label for="star3" class="fas fa-star"></label>
        <input type="radio" id="star2" name="rating" value="2">
        <label for="star2" class="fas fa-star"></label>
        <input type="radio" id="star1" name="rating" value="1" required>
        <label for="star1" class="fas fa-star"></label>
      </div>
      <div class="input-container">
        <input type="number" name="amount" placeholder="Enter amount (₹)" required>
      </div>
      <div class="btn">
        <button type="submit">Pay Now</button>
      </div>
    </form>
  </div>

  <script>
    // Select all the radio buttons
    const stars = document.querySelectorAll('.stars input');
    const labels = document.querySelectorAll('.stars label');

    // Add event listeners to each radio button to animate the stars from left to right
    stars.forEach((star, index) => {
      star.addEventListener('change', () => {
        // For each radio button checked, move from left to right
        for (let i = 0; i <= index; i++) {
          labels[i].style.color = "#fd4"; // Highlight the stars from left to right
        }
        for (let i = index + 1; i < labels.length; i++) {
          labels[i].style.color = "#444"; // Reset the color for unselected stars
        }
      });
    });
  </script>
</body>
</html>

  `);
});

// Handle feedback submission and create Razorpay order
app.post("/submitFeedback", async (req, res) => {
    const { rating, amount } = req.body;

    // Log feedback
    console.log("User Feedback:", rating);
    console.log("Payment Amount:", amount);

    // Convert amount to paise (Razorpay requires the amount in paise)
    const amountInPaise = parseInt(amount) * 100;

    // Create a Razorpay order
    const options = {
        amount: amountInPaise,
        currency: "INR",
        receipt: `receipt_${Math.floor(Math.random() * 1000)}`,
    };

    try {
        const order = await razorpay.orders.create(options);

        // Send payment page to user
        res.send(`
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment Page</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
    }
    body {
      background-color: #f4f4f4;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 30px;
      text-align: center;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
      width: 90%;
      max-width: 400px;
    }
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
    p {
      color: #666;
      font-size: 16px;
      margin-bottom: 20px;
    }
    .razorpay-payment-button {
      display: inline-block;
      background-color: #007bff;
      color: #fff;
      padding: 10px 20px;
      font-size: 16px;
      font-weight: bold;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-transform: uppercase;
      transition: background-color 0.3s ease;
    }
    .razorpay-payment-button:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Thank You for Your Feedback!</h1>
    <p>Click the button below to proceed with payment:</p>
    <form action="/verifyPayment" method="POST">
      <script
        src="https://checkout.razorpay.com/v1/checkout.js"
        data-key="${razorpay.key_id}" // Key ID from Razorpay dashboard
        data-amount="${order.amount}" // Amount in paise
        data-currency="${order.currency}"
        data-order_id="${order.id}" // Razorpay order ID
        data-buttontext="Pay Now"
        data-name="Chats Corner"
        data-description="Chats"
        data-theme.color="#007bff"
      ></script>
    </form>
  </div>
</body>
</html>

    `);
    } catch (err) {
        console.error("Error creating Razorpay order:", err);
        res.status(500).send("Error creating payment order.");
    }
});

// Verify payment
app.post("/verifyPayment", (req, res) => {
    const crypto = require("crypto");

    const { razorpay_order_id, razorpay_payment_id, razorpay_signature } = req.body;

    const hmac = crypto.createHmac("sha256", process.env.RAZORPAY_KEY_SECRET); // Replace with your Razorpay Key Secret
    hmac.update(razorpay_order_id + "|" + razorpay_payment_id);
    const generatedSignature = hmac.digest("hex");

    if (generatedSignature === razorpay_signature) {
        res.send(`
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Payment Successful</title>
                <style>
                  * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                  }
                  body {
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                  }
                  .container {
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 30px;
                    text-align: center;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    width: 90%;
                    max-width: 400px;
                  }
                  h1 {
                    color: #28a745;
                    font-size: 24px;
                    margin-bottom: 10px;
                  }
                  p {
                    color: #555;
                    font-size: 16px;
                  }
                </style>
              </head>
              <body>
                <div class="container">
                  <h1>Payment Successful!</h1>
                  <p>Thank you for your payment.</p>
                </div>
              </body>
            </html>
          `);

    } else {
        res.status(400).send(`            
            <!DOCTYPE html>
            <html lang="en">
              <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Payment Successful</title>
                <style>
                  * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                  }
                  body {
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                  }
                  .container {
                    background: #fff;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    padding: 30px;
                    text-align: center;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                    width: 90%;
                    max-width: 400px;
                  }
                  h1 {
                    color: red;
                    font-size: 24px;
                    margin-bottom: 10px;
                  }
                  p {
                    color: #555;
                    font-size: 16px;
                  }
                </style>
              </head>
              <body>
                <div class="container">
                  <h1>Payment Failed!</h1>
                  <p>In case money is debited, it will be refunded within 7 days.</p>
                </div>
              </body>
            </html>`);
    }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
