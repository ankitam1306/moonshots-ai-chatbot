import "./MessageBubble.css";

export default function MessageBubble({ type, text, sources }) {
  return (
    <div className={`message-bubble ${type}`}>
      <div
        className="bubble-content"
        dangerouslySetInnerHTML={{ __html: text }}
      />
      {type === "bot" && sources?.length > 0 && (
        <div className="launchbot-sources">
          <span>📚 Sources:</span>
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
  );
}
