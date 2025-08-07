import { useState } from "react";
import { highlightContent } from "../utils/highlightContent";

export function useLaunchbotQuery() {
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [highlightedAnswer, setHighlightedAnswer] = useState("");

  const boldHeadings = (text) => {
    return text.replace(
      /\*\*(.*?)\*\*/gm,
      (match, p1) => `<strong>${p1}</strong>`
    );
  };

  const askQuestion = async (question, onStreamUpdate) => {
    setLoading(true);
    setAnswer("");
    setSources([]);
    setHighlightedAnswer("");

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok || !res.body) {
        throw new Error("Network response was not ok.");
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let result = "";
      let finalSources = [];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });

        try {
          const parsed = JSON.parse(chunk);
          if (parsed.type === "sources") {
            finalSources = parsed.sources || [];
            setSources(finalSources);
            break;
          }
        } catch {
          // const cleanedChunk = chunk.replace(/^\s*\n+/, "");
          result += chunk;
          setAnswer(result);
          if (onStreamUpdate) {
            onStreamUpdate(result);
          }
        }
      }

      // Generate final highlighted answer after all chunks are received
      const withBold = boldHeadings(result);
      const withHighlight = highlightContent(withBold, finalSources);
      setHighlightedAnswer(withHighlight);
    } catch (err) {
      console.error("Streaming error:", err);
      setAnswer("❌ Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    answer,
    sources,
    highlightedAnswer,
    askQuestion,
  };
}
