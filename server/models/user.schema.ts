import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  type: {
    type: String,
    enum: ["student", "employee", "governor", "gammaspace", "player"],
    required: true,
  },
  bestScore: { type: Number, default: 0 },
  latestScore: { type: Number, default: 0 },
  lastLoginAt: Date,
  lastPlayedAt: Date,
});

export default mongoose.model("User", userSchema);
