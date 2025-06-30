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
  let userType = "player"; // Default user type for non-specific users

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
        userType = "employee";
        break;
      // No default needed, userType remains 'player'
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

  // Get request information for URL construction
  const headers = getRequestHeaders(event);
  const requestURL = getRequestURL(event);

  // Debug logging for URL construction
  console.error("Debug - Request headers:", {
    origin: headers.origin,
    host: headers.host,
    proto: headers["x-forwarded-proto"],
    referer: headers.referer,
  });
  console.error("Debug - Request URL:", requestURL.toString());

  // Force local development URL when running locally
  const isLocalDev = process.env.NODE_ENV === "development";
  const origin = isLocalDev
    ? "http://localhost:3000" // reel-polytechnic runs on port 3000
    : requestURL.origin !== "null"
    ? requestURL.origin
    : headers.origin ||
      `${headers["x-forwarded-proto"] || "http"}://${headers.host}`;

  console.error("Debug - Using origin:", origin);

  // Construct login URL using the request origin
  const loginUrl = `${origin}/api/auth/verify?token=${token}`;
  console.error("Debug - Final login URL:", loginUrl);

  // Send email
  const msg = {
    to: email,
    from: "noreply@reelpolytechnic.com",
    subject: "Your Security Awareness Online Game Login Link",
    text: `You're receiving this email because you signed up to participate in Seneca Polytechnic's Security Awareness Online Game. If you did not sign up for this game, please disregard this email.\n\nPlease click this link to start the game: ${loginUrl}\n\nThis link can only be used once, so if you are asked to register again, you'll need to request a new link.\n\nPlease note: the security awareness game will track your scores and participation. You will never be asked to enter any other personal information.`,
    html: `
      <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="text-align: center; margin-bottom: 30px;">
          <img src="${origin}/images/reelPolytechnicLogo.png" alt="Reel Polytechnic" style="max-width: 200px;">
          <h2 style="color: #EE3124; margin: 10px 0 5px;">REEL POLYTECHNIC</h2>
          <p style="color: #EE3124; margin: 0;">Security Awareness Online Game</p>
        </div>

        <div style="margin-bottom: 30px;">
          <p>You're receiving this email because you signed up to participate in <span style="background-color: #ffeb3b;">Seneca</span> <span style="color: #6C63FF;">Polytechnic's Security Awareness Online Game</span>. If you did <em>not</em> sign up for this game, please disregard this email.</p>
        </div>

        <div style="margin-bottom: 30px;">
          <p>Please click on the button below to start the game. <strong>This link can only be used once, so if you are asked to register again, you'll need to request a new link.</strong></p>
        </div>

        <div style="text-align: center; margin-bottom: 30px;">
          <a href="${loginUrl}" style="display: inline-block; background-color: #EE3124; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Start Game</a>
        </div>

        <div style="margin-bottom: 30px;">
          <p>Please note: the security awareness game will track your scores and participation. <strong>You will never be asked to enter any other personal information.</strong></p>
        </div>

      </div>
    `,
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
