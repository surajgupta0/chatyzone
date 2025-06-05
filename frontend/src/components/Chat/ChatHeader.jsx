// components/Chat/ChatHeader.jsx
import { useAppContext } from "../../context/AppContext";

export default function ChatHeader() {
  const { currentSelection } = useAppContext();

  return (
    <div className="p-4">
      <h5 className="font-semibold">
        {currentSelection?.isRoot == true
          ? "Root"
          : currentSelection?.reference_name || "Select a file or folder"}
      </h5>
      {currentSelection && (
        <p className="text-xs text-gray-500">
          {currentSelection.reference_type === "file" ? "File" : "Folder"}{" "}
          {currentSelection?.isRoot == true
            ? "/"
            : currentSelection.reference_path}
        </p>
      )}
    </div>
  );
}
