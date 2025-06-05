// components/FileViewer/index.jsx
import FilePreview from "./FilePreview";
import FileMetadata from "./FileMetadata";
import { useAppContext } from "../../context/AppContext";

export default function FileViewer() {
  const { currentSelection } = useAppContext();

  return (
    <div className="h-full overflow-y-auto p-4">
      {currentSelection?.refrence_type == "file" ? (
        <>
          <FilePreview file={currentSelection} />
          <FileMetadata file={currentSelection} />
        </>
      ) : (
        <div className="flex items-center justify-center h-full text-gray-500">
          Select a file to view details
        </div>
      )}
    </div>
  );
}
