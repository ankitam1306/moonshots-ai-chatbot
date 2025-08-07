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
      <button onClick={onSubmit} disabled={disabled}>
        Send
      </button>
    </div>
  );
}
