// components/Chat/MessageList.jsx
import { useEffect, useRef } from "react";
import { useAppContext } from "../../context/AppContext";
import { fetchChatHistory } from "../../api/chat";

export default function MessageList() {
  const { currentSelection, chatHistory, setChatHistory } = useAppContext();
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const loadHistory = async () => {
      if (!currentSelection) {
        setChatHistory([]);
        return;
      }
      try {
        const history = await fetchChatHistory(
          "USR0001",
          currentSelection?.reference_id,
          currentSelection?.reference_type
        );

        setChatHistory(history || []); // Ensure history is an array
      } catch (error) {
        setChatHistory([]); // Reset to an empty array on error
        console.error("Failed to fetch chat history:", error);
      }
    };
    loadHistory();
  }, [currentSelection]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {chatHistory.map((message, index) => (
        <div key={index}>
          {message?.query && (
            <div className="flex justify-end">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200">
                {message.query}
              </div>
            </div>
          )}
          {message?.response && (
            <div className="flex justify-start">
              <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-blue-200">
                {message.response}
              </div>
            </div>
          )}
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
