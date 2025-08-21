# AI Chatbot Widget

A lightweight, embeddable chat widget that provides AI-powered customer support for any website.

## Features

- 🤖 **AI-Powered Responses**: Uses advanced language models to provide contextual answers
- 🔍 **Content-Aware**: Understands your website content and provides relevant responses
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- 🎨 **Customizable**: Easy to customize colors, positioning, and branding
- ⚡ **Lightweight**: Minimal impact on your website's performance
- 🔒 **Secure**: All communications are encrypted and secure

## Quick Start

### 1. Install Dependencies

```bash
cd widget
npm install
```

### 2. Configure Environment

Copy the environment file and update the settings:

```bash
cp env.example .env
```

Update the `.env` file with your backend URL:

```env
VITE_BACKEND_URL=http://localhost:8000
VITE_WIDGET_TITLE=AI Assistant
VITE_WIDGET_SUBTITLE=Ask me anything about this website
```

### 3. Development

Start the development server:

```bash
npm run dev
```

The widget will be available at `http://localhost:5174`

### 4. Build for Production

Build the widget for production:

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Usage

### Basic Implementation

Add this script tag to your website:

```html
<script src="https://your-domain.com/widget.js" data-website-id="YOUR_WEBSITE_ID"></script>
```

### Advanced Configuration

You can also initialize the widget manually with custom configuration:

```html
<script src="https://your-domain.com/widget.js"></script>
<script>
  AIChatbotWidget.init({
    websiteId: 'YOUR_WEBSITE_ID',
    title: 'Custom Assistant',
    subtitle: 'How can I help you?',
    primaryColor: '#3b82f6',
    position: 'bottom-right' // 'bottom-left', 'bottom-center', 'bottom-right'
  });
</script>
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `websiteId` | string | required | Your website's unique identifier |
| `title` | string | 'AI Assistant' | Widget header title |
| `subtitle` | string | 'Ask me anything about this website' | Widget header subtitle |
| `primaryColor` | string | '#3b82f6' | Primary color for the widget |
| `position` | string | 'bottom-right' | Widget position on the page |
| `backendUrl` | string | from env | Backend API URL |

## Widget Positions

- `bottom-right` (default): Bottom right corner
- `bottom-left`: Bottom left corner  
- `bottom-center`: Bottom center of the page

## Development

### Project Structure

```
widget/
├── src/
│   ├── components/
│   │   ├── ChatWidget.jsx      # Main widget component
│   │   ├── ChatButton.jsx      # Floating chat button
│   │   ├── ChatWindow.jsx      # Chat window container
│   │   ├── MessageList.jsx     # Message list component
│   │   ├── Message.jsx         # Individual message component
│   │   ├── LoadingMessage.jsx  # Loading indicator
│   │   └── MessageInput.jsx    # Message input component
│   ├── widget.js               # Widget entry point
│   └── index.css               # Global styles
├── dist/                       # Built files
├── index.html                  # Demo page
└── package.json
```

### Building

The widget is built using Vite and configured to output both IIFE and ES module formats:

- `dist/widget.iife.js` - Immediately Invoked Function Expression (for direct browser use)
- `dist/widget.es.js` - ES Module (for bundlers)

### Customization

#### Styling

The widget uses Tailwind CSS for styling. You can customize the appearance by:

1. Modifying the `tailwind.config.js` file
2. Adding custom CSS in `src/index.css`
3. Using inline styles in the components

#### Functionality

To add new features:

1. Create new components in `src/components/`
2. Import and use them in the main `ChatWidget.jsx`
3. Update the widget configuration as needed

## API Integration

The widget communicates with your backend API through the following endpoints:

- `POST /api/chat` - Send messages and receive responses
- `GET /api/websites/{id}` - Get website information

### Message Format

```javascript
{
  message: "User's question",
  website_id: "website-id",
  conversation_id: "optional-conversation-id"
}
```

### Response Format

```javascript
{
  message: "AI response",
  conversation_id: "conversation-id",
  sources: ["url1", "url2"],
  confidence: 0.95
}
```

## Deployment

### CDN Deployment

1. Build the widget: `npm run build`
2. Upload the `dist/` files to your CDN
3. Update the script src to point to your CDN URL

### Self-Hosted

1. Build the widget: `npm run build`
2. Serve the `dist/` directory from your web server
3. Update the script src to point to your server URL

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

MIT License - see LICENSE file for details

## Support

For support and questions, please open an issue on GitHub or contact the development team. 