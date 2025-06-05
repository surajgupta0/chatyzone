// components/Sidebar/index.jsx
import { useState, useEffect } from "react";
import FolderTree from "./FolderTree";
import FileUpload from "./FileUpload";
import SearchBar from "./SearchBar";
import { useAppContext } from "../../context/AppContext";
import { fetchRootFolder } from "../../api/files"; // Adjust the import path as necessary

export default function Sidebar() {
  const [searchQuery, setSearchQuery] = useState("");
  const { currentSelection, setCurrentSelection, rootFolder, setRootFolder } =
    useAppContext();

  return (
    <div className="flex flex-col h-full">
      <div className="p-4">
        <SearchBar value={searchQuery} onChange={setSearchQuery} />
      </div>

      <div className="flex-1 overflow-y-auto">
        <FolderTree searchQuery={searchQuery} />
      </div>

      <FileUpload />
    </div>
  );
}
