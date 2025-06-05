// components/Sidebar/FolderTree/index.jsx
import { useEffect, useState } from "react";
import { useAppContext } from "../../../context/AppContext";
import FolderNode from "./FolderNode";
import {
  fetchFolderStructure,
  renameFolder,
  renameFile,
  deleteFile,
  deleteFolder,
} from "../../../api/files";

export default function FolderTree() {
  const { folders, setFolders, setCurrentSelection } = useAppContext();

  useEffect(() => {
    const loadFolders = async () => {
      try {
        const data = await fetchFolderStructure();
        setFolders(data);
      } catch (error) {
        console.error("Error fetching folders:", error.message);
      }
    };
    loadFolders();
  }, []);

  const toggleFolder = (folder) => {
    var reference = {
      reference_id: folder?.subFolders ? folder?.folder_id : folder?.file_id,
      reference_type: folder?.subFolders ? "folder" : "file",
      reference_name: folder?.folder_name || folder?.file_name,
      reference_path: folder?.folder_path || folder?.file_path,
    };

    setCurrentSelection(reference);
  };

  const onRenameComplete = async (folder) => {
    try {
      if (folder?.subFolders) {
        const data = await renameFolder(folder?.folder_id, folder?.folder_name);
      } else {
        const data = await renameFile(folder?.file_id, folder?.file_name);
      }
    } catch (error) {
      console.error("Error renaming folders:", error.message);
    }
  };

  const onDeleteComplete = async (folder) => {
    try {
      if (folder?.subFolders) {
        const data = await deleteFolder(folder?.folder_id);
      } else {
        const data = await deleteFile(folder?.file_id);
      }
    } catch (error) {
      console.error("Error renaming folders:", error.message);
    }
  };

  return (
    <div className="space-y-1">
      {folders.map(
        (folder) =>
          folder.subFolders &&
          folder.subFolders.map((subfolder) => (
            <FolderNode
              key={subfolder.folder_id}
              folder={subfolder}
              level={0}
              onToggle={toggleFolder}
              onRenameComplete={onRenameComplete}
              onDeleteComplete={onDeleteComplete}
            />
          ))
      )}
      {folders.map(
        (folder) =>
          folder.files &&
          folder.files.map((file) => (
            <FolderNode
              key={file.file_id}
              folder={file}
              level={0}
              onToggle={toggleFolder}
              onRenameComplete={onRenameComplete}
              onDeleteComplete={onDeleteComplete}
            />
          ))
      )}
    </div>
  );
}
