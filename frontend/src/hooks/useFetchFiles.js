// hooks/useFetchFiles.js
import { useState, useEffect } from "react";
import { fetchFolderStructure } from "../api/files";

export default function useFetchFiles() {
  const [folders, setFolders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchFolderStructure();
        setFolders(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  return { folders, loading, error };
}
