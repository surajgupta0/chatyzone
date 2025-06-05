import { useState, useEffect, useRef } from "react";
import {
  ChevronRight,
  ChevronDown,
  Folder,
  File,
  Edit2,
  Trash2,
  Check,
  X,
} from "react-feather";
import { useAppContext } from "../../../context/AppContext";

export default function FolderNode({
  folder,
  level,
  onToggle,
  onRenameComplete,
  onDeleteComplete,
}) {
  const { currentSelection, expandedFolders, setExpandedFolders } =
    useAppContext();
  const [activeFolder, setActiveFolder] = useState("");
  const [showMenu, setShowMenu] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState("");
  const inputRef = useRef(null);
  const nodeRef = useRef(null);

  // Handle right-click context menu
  const handleContextMenu = (e) => {
    e.preventDefault();
    setMenuPosition({ x: e.clientX, y: e.clientY });
    setShowMenu(true);
    setEditValue(folder.folder_name || folder.file_name);
  };

  // Close menu when clicking elsewhere
  useEffect(() => {
    const handleClickOutside = () => {
      setShowMenu(false);
      if (isEditing) handleCancelEdit();
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, [isEditing]);

  // Focus input when editing starts
  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  const handleRename = () => {
    setIsEditing(true);
    setShowMenu(false);
  };

  const handleConfirmEdit = () => {
    if (editValue.trim()) {
      onRenameComplete({
        ...folder,
        [folder.subFolders ? "folder_name" : "file_name"]: editValue,
      });
    }
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditValue(folder.folder_name || folder.file_name);
  };

  const handleDelete = () => {
    if (
      window.confirm(
        `Delete ${folder.subFolders ? "folder" : "file"} permanently?`
      )
    ) {
      onDeleteComplete(folder);
    }
    setShowMenu(false);
  };

  return (
    <div className="pl-4" ref={nodeRef} onContextMenu={handleContextMenu}>
      <div
        className={`flex items-center py-1 px-2 hover:bg-gray-200 rounded cursor-pointer ${activeFolder} ${
          level > 0 ? "pl-" + level * 4 : ""
        }`}
        onClick={() => !isEditing && onToggle(folder)}
      >
        {isEditing ? (
          <div className="flex items-center w-full">
            <input
              ref={inputRef}
              type="text"
              value={editValue}
              onChange={(e) => setEditValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleConfirmEdit();
                if (e.key === "Escape") handleCancelEdit();
              }}
              className="flex-1 px-1 py-0.5 text-sm border rounded"
            />
          </div>
        ) : (
          <>
            {folder.subFolders ? (
              <>
                {expandedFolders.includes(folder.folder_id) ? (
                  <ChevronDown
                    size={16}
                    onClick={(e) => {
                      e.stopPropagation();
                      setExpandedFolders((prev) =>
                        prev.filter((id) => id !== folder.folder_id)
                      );
                    }}
                  />
                ) : (
                  <ChevronRight
                    size={16}
                    onClick={(e) => {
                      e.stopPropagation();
                      setExpandedFolders((prev) => [...prev, folder.folder_id]);
                    }}
                  />
                )}
                <Folder size={16} />
                <span className="ml-2 text-sm">{folder.folder_name}</span>
              </>
            ) : (
              <>
                <File size={16} />
                <span className="ml-2 text-sm">{folder.file_name}</span>
              </>
            )}
          </>
        )}
      </div>

      {/* Context Menu */}
      {showMenu && (
        <div
          className="fixed bg-white shadow-lg rounded-md py-1 z-50 border border-gray-200"
          style={{
            top: `${menuPosition.y}px`,
            left: `${menuPosition.x}px`,
            minWidth: "150px",
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <button
            className="flex items-center w-full px-4 py-2 text-sm hover:bg-gray-100"
            onClick={handleRename}
          >
            <Edit2 size={14} className="mr-2" />
            Rename
          </button>
          <button
            className="flex items-center w-full px-4 py-2 text-sm hover:bg-gray-100 text-red-600"
            onClick={handleDelete}
          >
            <Trash2 size={14} className="mr-2" />
            Delete
          </button>
        </div>
      )}

      {/* Child nodes */}
      {expandedFolders.includes(folder.folder_id) && folder.subFolders && (
        <div className="border-l border-gray-300 ml-3">
          {folder.subFolders.map((subfolder) => (
            <FolderNode
              key={subfolder.folder_id}
              folder={subfolder}
              level={level + 1}
              onToggle={onToggle}
              onRenameComplete={onRenameComplete}
              onDeleteComplete={onDeleteComplete}
            />
          ))}
          {folder.files.map((file) => (
            <FolderNode
              key={file.file_id}
              folder={file}
              level={level + 1}
              onToggle={onToggle}
              onRenameComplete={onRenameComplete}
              onDeleteComplete={onDeleteComplete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
