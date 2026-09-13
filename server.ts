import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { GoogleGenAI, Type } from "@google/genai";

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.json());

// Serve static assets from /static and root
app.use("/static", express.static(path.join(__dirname, "static")));
app.use(express.static(path.join(__dirname, "static")));

// Lazy-initialize Gemini AI client
let aiClient: GoogleGenAI | null = null;
function getGenAI(): GoogleGenAI {
  if (!aiClient) {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error(
        "GEMINI_API_KEY is not set. Please provide your Gemini API key in Settings > Secrets."
      );
    }
    aiClient = new GoogleGenAI({
      apiKey,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
  }
  return aiClient;
}

// Health check endpoint
app.get("/api/health", (req, res) => {
  res.json({ status: "ok" });
});

// Primary UI route
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "templates", "index.html"));
});

// Chat generation endpoint
app.post("/generate", async (req, res) => {
  const { message, model } = req.body;

  if (!message || typeof message !== "string" || !message.trim()) {
    return res.status(400).json({ error: "Missing message" });
  }

  const selectedModel = model || "gemini";
  if (selectedModel !== "gemini" && selectedModel !== "llama3") {
    return res.status(400).json({ error: "Invalid model selection" });
  }

  const startTime = Date.now();

  try {
    const ai = getGenAI();

    const promptResponse = await ai.models.generateContent({
      model: "gemini-3.8-flash",
      contents: message.trim(),
      config: {
        systemInstruction:
          "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response. " +
          "Analyze the user's message and return a JSON object with: " +
          "1. 'summary': A short summary of what the user said. " +
          "2. 'sentiment': An integer between 0 and 100 (0 = very negative, 50 = neutral, 100 = very positive). " +
          "3. 'response': A helpful, polite, and natural response to the user.",
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            summary: {
              type: Type.STRING,
              description: "A short summary of the user's message",
            },
            sentiment: {
              type: Type.INTEGER,
              description:
                "Sentiment score from 0 (very negative) to 100 (very positive)",
            },
            response: {
              type: Type.STRING,
              description: "A helpful response to the user's message",
            },
          },
          required: ["summary", "sentiment", "response"],
        },
        temperature: 0.2,
        maxOutputTokens: 1024,
      },
    });

    const duration = (Date.now() - startTime) / 1000;
    const responseText = promptResponse.text?.trim() || "{}";

    let parsedResult: { summary: string; sentiment: number; response: string };
    try {
      parsedResult = JSON.parse(responseText);
    } catch {
      parsedResult = {
        summary: message.slice(0, 60),
        sentiment: 50,
        response: responseText,
      };
    }

    return res.json({
      summary: parsedResult.summary || message.slice(0, 60),
      sentiment: typeof parsedResult.sentiment === "number" ? parsedResult.sentiment : 50,
      response: parsedResult.response || "No response generated.",
      duration,
    });
  } catch (error: any) {
    console.error("Error generating response:", error);
    const duration = (Date.now() - startTime) / 1000;
    return res.status(500).json({
      error: error?.message || "Failed to generate response",
      duration,
    });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`AI Assistant server running on http://0.0.0.0:${PORT}`);
});
