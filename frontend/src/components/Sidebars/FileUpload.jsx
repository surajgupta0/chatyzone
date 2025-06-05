// components/Sidebar/FileUpload.jsx
import { useState } from "react";
import { useAppContext } from "../../context/AppContext";
import {
  uploadFile,
  createFolder,
  fetchFolderStructure,
} from "../../api/files";
import { Upload, X, Check, FolderPlus } from "react-feather";
import Button from "../Common/Button";

export default function FileUpload() {
  const { currentSelection, setFolders, setExpandedFolders } = useAppContext();
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [showNewFolder, setShowNewFolder] = useState(false);
  const [newFolderName, setNewFolderName] = useState("");

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);
    setSuccess(false);

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Add folder ID if a folder is selected
      formData.append("folder_id", currentSelection?.reference_id);

      // Add other metadata if needed
      formData.append("user_id", "USR0001");

      await uploadFile(formData, (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percentCompleted);
      });

      setSuccess(true);
      // Refresh folder structure
      const updatedFolders = await fetchFolderStructure();
      setFolders(updatedFolders);
      setExpandedFolders((prev) =>
        prev.filter((id) => id !== currentSelection?.reference_id)
      );
    } catch (err) {
      setError(err.message || "Failed to upload file");
    } finally {
      setIsUploading(false);
      setTimeout(() => {
        setSuccess(false);
        setProgress(0);
      }, 3000);
    }
  };

  const handleCreateFolder = async () => {
    if (!newFolderName.trim()) return;

    try {
      var res = await createFolder(
        "USR0001",
        newFolderName,
        currentSelection?.reference_id
      );

      // Refresh folder structure
      const updatedFolders = await fetchFolderStructure();
      setFolders(updatedFolders);
      setShowNewFolder(false);
      setNewFolderName("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-4 space-y-4">
      {/* File Upload Section */}
      <div className="space-y-2">
        <label className="flex flex-col items-center justify-center cursor-pointer w-full">
          <input
            type="file"
            className="hidden"
            onChange={handleFileUpload}
            disabled={isUploading}
          />
          <div className="w-full">
            <Button
              icon={<Upload size={16} />}
              label="Upload File"
              variant="outline"
              onClick={() =>
                document.querySelector('input[type="file"]').click()
              }
              fullWidth={true}
              disabled={isUploading}
            />
          </div>
        </label>

        {isUploading && (
          <div className="space-y-1">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500">Uploading... {progress}%</p>
          </div>
        )}
      </div>

      {/* Folder Creation Section */}
      <div className="space-y-2">
        {!showNewFolder ? (
          <Button
            icon={<FolderPlus size={16} />}
            label="New Folder"
            variant="outline"
            fullWidth
            onClick={() => setShowNewFolder(true)}
          />
        ) : (
          <div className="space-y-2">
            <input
              type="text"
              value={newFolderName}
              onChange={(e) => setNewFolderName(e.target.value)}
              placeholder="Folder name"
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />
            <div className="flex justify-between items-center pt-2">
              <Button
                label="Create"
                onClick={handleCreateFolder}
                variant="outline"
                disabled={!newFolderName.trim()}
              />
              <Button
                label="Cancel"
                variant="outline"
                onClick={() => {
                  setShowNewFolder(false);
                  setNewFolderName("");
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Status Messages */}
      <div className="min-h-6">
        {error && (
          <div className="flex items-center text-red-500 text-sm">
            <X size={16} className="mr-1" />
            {error}
          </div>
        )}
        {success && (
          <div className="flex items-center text-green-500 text-sm">
            <Check size={16} className="mr-1" />
            Upload successful!
          </div>
        )}
      </div>

      {/* Current Location Info */}
      <div className="text-xs text-gray-500 mt-2">
        {currentSelection ? (
          <p>
            Uploading to:{" "}
            <span className="font-medium">
              {currentSelection.reference_name}
            </span>
          </p>
        ) : (
          <p>Files will be uploaded to root directory</p>
        )}
      </div>
    </div>
  );
}
