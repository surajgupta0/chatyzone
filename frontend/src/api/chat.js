import { API_BASE_URL, API_HEADERS } from "../constant";

// api/chat.js
export async function fetchChatHistory(userId, referenceId, referenceType) {
  const response = await fetch(`${API_BASE_URL}/chat/history`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: userId,
      reference_id: referenceId,
      reference_type: referenceType,
    }),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result?.message || "Failed to fetch chat history");
  }
  return await result?.data; // Assuming the data is in the 'data' field of the response
}

export async function sendMessage(userId, referenceId, referenceType, message) {
  const response = await fetch(`${API_BASE_URL}/chat/chat`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: userId,
      reference_id: referenceId,
      reference_type: referenceType,
      message: message,
    }),
  });
  const result = await response.json();
  if (!response.ok) {
    throw new Error(result?.message || "Failed to fetch chat history");
  }
  return await result?.data; // Assuming the data is in the 'data' field of the response
}
