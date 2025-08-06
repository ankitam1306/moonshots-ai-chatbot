import { useState } from "react";

export function useLaunchbotQuery() {
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");

  const askQuestion = async (question) => {
    setLoading(true);
    setAnswer(""); // clear previous result
    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (data.answer) {
        setAnswer(data.answer);
      } else {
        setAnswer("No answer returned from Launchbot.");
      }
    } catch (err) {
      console.error("❌ Failed to query Launchbot:", err);
      setAnswer("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    answer,
    askQuestion,
  };
}
