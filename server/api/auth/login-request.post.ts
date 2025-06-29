import type { H3Event } from "h3";
import User from "~/server/models/user.schema";
import sgMail from "@sendgrid/mail";
import crypto from "crypto";

sgMail.setApiKey(process.env.SENDGRID_API_KEY || "");

export default defineEventHandler(async (event: H3Event) => {
  const { email } = await readBody(event);

  if (!email) {
    throw createError({
      statusCode: 400,
      message: "Email is required",
    });
  }

  // Basic email format validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    throw createError({
      statusCode: 400,
      message: "Please enter a valid email address.",
    });
  }

  // Determine user type based on domain (optional, for analytics)
  const domain = email.split("@")[1];
  let userType = "external"; // Default user type for non-specific users

  // Optional: Still categorize specific users if needed for analytics
  if (domain) {
    switch (domain) {
      case "myseneca.ca":
        userType = "student";
        break;
      case "senecapolytechnic.ca":
      case "senecacollege.ca":
        userType = "employee";
        break;
      case "reelpolytechnic.com":
        userType = "admin";
        break;
      // No default needed, userType remains 'external'
    }
  }

  // Find or create user
  let user = await User.findOne({ email });
  if (!user) {
    user = new User({ email, type: userType });
    await user.save();
  }

  // Generate login token
  const token = crypto.randomBytes(32).toString("hex");
  await setUserSession(event, { loginToken: token, email });

  // Send email
  const loginUrl = `${process.env.BASE_URL}/api/auth/verify?token=${token}`;

  const msg = {
    to: email,
    from: "noreply@reelpolytechnic.com",
    subject: "Your Reel Polytechnic Login Link",
    text: `Click this link to log in: ${loginUrl}`,
    html: `<p>Click <a href="${loginUrl}">here</a> to log in to Reel Polytechnic.</p>`,
  };

  try {
    await sgMail.send(msg);
    // Email sent successfully
  } catch (error) {
    console.error(error);
    throw createError({
      statusCode: 500,
      message: "Failed to send login email. Please try again later.",
    });
  }

  return { message: "Login link sent to your email" };
});
