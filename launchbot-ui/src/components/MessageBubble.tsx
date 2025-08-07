import "./MessageBubble.css";

export default function MessageBubble({ type, text, sources }) {
  const isHTMLString = typeof text === "string";
  return (
    <div className={`message-bubble ${type}`}>
      {isHTMLString ? (
        <div
          className="bubble-content"
          dangerouslySetInnerHTML={{ __html: text }}
        />
      ) : (
        <div className="bubble-content">{text}</div>
      )}
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
