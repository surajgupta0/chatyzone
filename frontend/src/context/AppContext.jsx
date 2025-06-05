// context/AppContext.jsx
import { createContext, useContext, useState, useEffect } from "react";
import { fetchRootFolder } from "../api/files"; // Adjust the import path as necessary

const AppContext = createContext();

export function AppProvider({ children }) {
  const [rootFolder, setRootFolder] = useState({});
  const [currentSelection, setCurrentSelection] = useState({});
  const [folders, setFolders] = useState([]);
  const [expandedFolders, setExpandedFolders] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    const loadRootFolder = async () => {
      try {
        const data = await fetchRootFolder();
        const updated_data = {
          reference_id: data?.folder_id,
          reference_type: "folder",
          reference_name: data?.folder_name,
          reference_path: data?.folder_path,
          isRoot: true,
        };
        setCurrentSelection(updated_data);
        setRootFolder(data);
      } catch (error) {
        console.error("Error fetching root folder:", error);
      }
    };
    loadRootFolder();
  }, []);

  return (
    <AppContext.Provider
      value={{
        currentSelection,
        setCurrentSelection,
        folders,
        setFolders,
        expandedFolders,
        setExpandedFolders,
        rootFolder,
        setRootFolder,
        searchQuery,
        setSearchQuery,
        chatHistory,
        setChatHistory,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext);
}
