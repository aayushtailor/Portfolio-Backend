const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 5001;

// Middleware
app.use(cors({
  origin: '*',  // Configure for production with specific origins
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(bodyParser.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'Server is running' });
});

// Nodemailer setup (Gmail in this case)
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
  // Add timeout settings
  connectionTimeout: 10000, // 10 seconds
  greetingTimeout: 5000,    // 5 seconds
  socketTimeout: 10000      // 10 seconds
});

app.post('/send-email', async (req, res) => {
  const { name, email, message } = req.body;

  // Validate input
  if (!email || !message) {
    return res.status(400).json({ error: 'Email and message are required' });
  }

  const mailOptions = {
    from: process.env.EMAIL_USER,
    to: process.env.EMAIL_USER,
    subject: `Portfolio Contact: ${name || 'New Contact'}`,
    text: `From: ${email}\nName: ${name || 'Not provided'}\n\nMessage: ${message}`,
    html: `
      <h2>New Contact Form Submission</h2>
      <p><strong>From:</strong> ${email}</p>
      <p><strong>Name:</strong> ${name || 'Not provided'}</p>
      <p><strong>Message:</strong></p>
      <p>${message.replace(/\n/g, '<br>')}</p>
    `
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent successfully:', info.messageId);
    res.status(200).json({ message: 'Email sent successfully', id: info.messageId });
  } catch (error) {
    console.error('Failed to send email:', error);
    res.status(500).json({ error: 'Failed to send email', details: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});