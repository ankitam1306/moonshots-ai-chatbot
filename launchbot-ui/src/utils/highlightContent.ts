// src/utils/highlightContent.js
import Prism from "prismjs";
import "prismjs/themes/prism.css";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-bash";
import "prismjs/components/prism-json";
import "prismjs/components/prism-python";

export function highlightContent(text, sourceUrls) {
  let highlighted = text;

  // Highlight source terms
  sourceUrls.forEach((url) => {
    try {
      const pathname = new URL(url).pathname;
      const segments = pathname.split("/").filter(Boolean);
      segments.forEach((segment) => {
        const regex = new RegExp(`\b${segment}\b`, "gi");
        highlighted = highlighted.replace(
          regex,
          (match) => `<mark>${match}</mark>`
        );
      });
    } catch {}
  });

  // Apply Prism highlighting to fenced code blocks
  highlighted = highlighted.replace(
    /```(\w+)?\n([\s\S]*?)\n```/g,
    (match, lang, code) => {
      const language = Prism.languages[lang] ? lang : "plaintext";
      const html = Prism.highlight(
        code.trim(),
        Prism.languages[language],
        language
      );
      return `<pre class="language-${language}"><code class="language-${language}">${html}</code></pre>`;
    }
  );

  return highlighted;
}
