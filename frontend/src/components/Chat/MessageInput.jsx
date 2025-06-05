import { useState } from "react";
import { useAppContext } from "../../context/AppContext";
import { sendMessage } from "../../api/chat"; // Assuming you have an API function to send messages

const MessageInput = () => {
  const { currentSelection, chatHistory, setChatHistory } = useAppContext();
  const [message, setMessage] = useState("");

  const handleSendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages

    try {
      await sendMessage(
        "USR0001", // Assuming this is a hardcoded user ID for now
        currentSelection?.reference_id,
        currentSelection?.reference_type,
        message
      );
      setMessage(""); // Clear the input after sending
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="flex items-center p-4 border-t">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 p-2 border rounded"
      />
      <button
        onClick={handleSendMessage}
        className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Send
      </button>
    </div>
  );
};

export default MessageInput;
