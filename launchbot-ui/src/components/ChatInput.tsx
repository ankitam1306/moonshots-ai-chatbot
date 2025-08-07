import { FaArrowUp } from "react-icons/fa";
import "./ChatInput.css";

export default function ChatInput({ value, onChange, onSubmit, disabled }) {
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="chat-input">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask anything about LaunchDarkly..."
        rows={1}
        disabled={disabled}
      />
      <button
        className={`chat-input-icon ${value.trim() ? "visible" : "hidden"}`}
        onClick={onSubmit}
        disabled={disabled}
        aria-label="Send"
      >
        <FaArrowUp />
      </button>
    </div>
  );
}
