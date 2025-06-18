import React from 'react';
import AgentMessage from './AgentMessage';

export default function MarkdownDemo() {
	const sampleMarkdown = `# Markdown Rendering Demo

This demonstrates the new markdown rendering capabilities in chat messages.

## Features

### Text Formatting
- **Bold text** for emphasis
- *Italic text* for subtle emphasis
- \`inline code\` for technical terms
- ~~Strikethrough~~ for corrections

### Code Blocks

Here's a JavaScript example:

\`\`\`javascript
function greetUser(name) {
    console.log(\`Hello, \${name}!\`);
    return \`Welcome to PIKE, \${name}\`;
}

// Usage
const message = greetUser("Developer");
\`\`\`

And a Python example:

\`\`\`python
def process_data(data):
    """Process the input data and return results."""
    results = []
    for item in data:
        if item.is_valid():
            results.append(item.transform())
    return results
\`\`\`

### Lists

**Unordered list:**
- First item
- Second item
  - Nested item
  - Another nested item
- Third item

**Ordered list:**
1. Step one
2. Step two
3. Step three

### Tables

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown | ✅ | Fully supported |
| Code highlighting | ✅ | Multiple languages |
| Tables | ✅ | GitHub flavored |
| Links | ✅ | [Example link](https://example.com) |

### Blockquotes

> This is an important note that stands out from the regular text.
> It can span multiple lines and provides emphasis.

### Multiline Content

This message demonstrates that line breaks
are preserved properly, so when you write
multiple lines in your message, they will
display correctly in the chat interface.

---

That's the end of the markdown demo! 🎉`;

	const mockMessage = {
		content: sampleMarkdown,
		type: 'ai'
	};

	return (
		<div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
			<h2>Markdown Rendering Demo</h2>
			<p>This component demonstrates the new markdown rendering capabilities:</p>
			<div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '10px' }}>
				<AgentMessage message={mockMessage} />
			</div>
		</div>
	);
}
