import { useState, useEffect } from "react";
import { useLaunchbotQuery } from "./hooks/useLaunchbotQuery";
import MessageBubble from "./components/MessageBubble";
import ChatInput from "./components/ChatInput";
import "./stylesheets/Launchbot.css";

export default function Launchbot() {
  const { askQuestion, loading, highlightedAnswer, sources } =
    useLaunchbotQuery();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSubmit = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { type: "user", text: input }]);
    setInput("");

    await askQuestion(input);
  };

  useEffect(() => {
    if (!loading && highlightedAnswer) {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: highlightedAnswer, sources },
      ]);
    }
  }, [loading, highlightedAnswer]);

  console.log("highlightedAnswer", highlightedAnswer);
  console.log("messages", messages);

  return (
    <div className="launchbot-container">
      <header className="launchbot-header">
        <h2>🚀 Launchbot</h2>
      </header>

      <div className="launchbot-thread">
        {messages.map((msg, idx) => (
          <MessageBubble
            key={idx}
            type={msg.type}
            text={msg.text}
            sources={msg.sources}
          />
        ))}
        {loading && <MessageBubble type="bot" text="..." />}
      </div>

      <ChatInput
        value={input}
        onChange={setInput}
        onSubmit={handleSubmit}
        disabled={loading}
      />
    </div>
  );
}
