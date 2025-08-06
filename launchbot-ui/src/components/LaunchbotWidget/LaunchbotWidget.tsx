import { useState } from "react";
import "./LaunchbotWidget.css";
import { useLaunchbotQuery } from "../../hooks/useLaunchbotQuery";

export default function LaunchbotWidget() {
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("");
  const { answer, loading, askQuestion } = useLaunchbotQuery();

  const handleSubmit = async () => {
    if (!question.trim()) return;
    await askQuestion(question);
  };
  return (
    <>
      <button className="launchbot-button" onClick={() => setOpen(true)}>
        💬 Ask Launchbot
      </button>
      ;
      {open && (
        <div className="modal-overlay">
          <div className="modal">
            <h2 className="title">Ask Launchbot</h2>
            <button className="close-btn" onClick={() => setOpen(false)}>
              &times;
            </button>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., How do I create a feature flag?"
              className="input"
            />

            <button
              onClick={handleSubmit}
              disabled={loading}
              className="submit"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>

            {answer && <div className="answer-section">{answer}</div>}
          </div>
        </div>
      )}
    </>
  );
}
