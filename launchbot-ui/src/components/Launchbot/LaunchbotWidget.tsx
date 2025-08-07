import { useState } from "react";
import "./LaunchbotWidget.css";
import { useLaunchbotQuery } from "../../hooks/useLaunchbotQuery";

export default function LaunchbotWidget() {
  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("how to integrate sdk in nodejs");
  const { answer, loading, askQuestion, sources, highlightedAnswer } =
    useLaunchbotQuery();

  const handleSubmit = async (e) => {
    e.preventDefault();
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
            <form onSubmit={handleSubmit}>
              <div className="title">
                <h2>Ask Launchbot</h2>
                <button className="close-btn" onClick={() => setOpen(false)}>
                  &times;
                </button>
              </div>

              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g., How do I create a feature flag?"
                className="input"
                id="input"
              />

              <button
                onClick={handleSubmit}
                disabled={loading}
                className="submit"
                type="submit"
              >
                {loading ? "Thinking..." : "Ask"}
              </button>
            </form>

            {answer && (
              <div
                className="answer-section"
                dangerouslySetInnerHTML={{
                  __html: highlightedAnswer,
                }}
              ></div>
            )}
            {sources.length > 0 && (
              <div className="sources-section">
                <h4>📚 Sources:</h4>
                <ul>
                  {sources.map((url, i) => (
                    <li key={i}>
                      <a href={url} target="_blank" rel="noopener noreferrer">
                        {new URL(url).hostname + new URL(url).pathname}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}
