import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { useState } from "react";

export default function Chat() {
    const initialMessages = [
        { message: "Hello", sender: "bot", direction: "incoming" },
        { message: "How can I help you?", sender: "bot", direction: "incoming" }
    ];
    const [messages, setMessages] = useState(initialMessages)

    const onSend = async (innerHtml, textContent, innerText, nodes) => {
        const newMessage = { message: textContent, sender: "user", direction: "outgoing" };
        setMessages([...messages, newMessage]);
        
        try {
            const history = messages.map(msg => ({
                role: msg.sender === "user" ? "user" : "system",
                content: msg.message
            }));
            history.push({ role: "user", content: textContent });
            
            const payload = {
                question: textContent,
                history: history
            };
            
            const response = await fetch("http://localhost:8000/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            const botMessage = {
                message: data.answer || data.message || "No response from server",
                sender: "bot",
                direction: "incoming"
            };
            setMessages(prev => [...prev, botMessage]);
            
        } catch (error) {
            console.error("Error sending message:", error);
            const errorMessage = {
                message: "Sorry, I couldn't process your request. Please try again.",
                sender: "bot",
                direction: "incoming"
            };
            setMessages(prev => [...prev, errorMessage]);
        }
    };

    return (
        <MainContainer style={{ height: "500px" }}>
        <ChatContainer>
            <MessageList>
                {messages.map((msg, index) => (
                    <Message key={index} model={{ message: msg.message, direction: msg.direction, sender: msg.sender }} />
                ))}
            </MessageList>
            <MessageInput placeholder="Type message..." onSend={onSend} />
        </ChatContainer>
        </MainContainer>
    );
}
