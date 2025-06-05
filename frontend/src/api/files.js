import { API_BASE_URL, API_HEADERS } from "../constant";

// api/files.js
// api/files.js
export async function fetchFolderStructure() {
  try {
    // Fetch folders
    const folderResponse = await fetch(`${API_BASE_URL}/folder/list`, {
      method: "POST",
      headers: API_HEADERS,
      body: JSON.stringify({ user_id: "USR0001" }),
    });

    if (!folderResponse.ok) {
      const errorData = await folderResponse.json();
      throw new Error(errorData?.message || "Failed to fetch folders");
    }

    // Fetch files
    const fileResponse = await fetch(`${API_BASE_URL}/file/get`, {
      method: "POST",
      headers: API_HEADERS,
      body: JSON.stringify({ user_id: "USR0001" }),
    });

    if (!fileResponse.ok) {
      const errorData = await fileResponse.json();
      throw new Error(errorData?.message || "Failed to fetch files");
    }

    // Process data
    const folders = (await folderResponse.json())?.data || [];
    const files = (await fileResponse.json())?.data || [];

    // Build hierarchy
    const buildHierarchy = (parentId = "") => {
      return folders
        .filter((folder) => folder.parent_id === parentId)
        .map((folder) => ({
          ...folder,
          files: files.filter((file) => file.folder_id === folder.folder_id),
          subFolders: buildHierarchy(folder.folder_id), // Recursive call
        }));
    };

    return buildHierarchy(); // Start with root folders (parent_id = null)
  } catch (error) {
    // Convert to a more specific error if needed
    throw new Error(`Failed to load folder structure: ${error.message}`);
  }
}

export async function fetchRootFolder() {
  // Fetch folders
  const folderResponse = await fetch(`${API_BASE_URL}/folder/list`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({ user_id: "USR0001" }),
  });

  var folders = await folderResponse.json();
  if (!folderResponse.ok) {
    throw new Error(folders?.message || "Failed to fetch folders");
  }

  const root_folders =
    folders?.data?.filter((folder) => folder.parent_id === "") || [];

  return root_folders[0];
}

export async function uploadFile(formData, onProgress) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    xhr.upload.onprogress = onProgress;

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        resolve(JSON.parse(xhr.response));
      } else {
        reject(new Error(JSON.parse(xhr.response)?.message || xhr.statusText));
      }
    };

    xhr.onerror = () =>
      reject(new Error(JSON.parse(xhr.response)?.message || xhr.statusText));

    xhr.open("POST", `${API_BASE_URL}/file/upload`);
    xhr.send(formData);
  });
}

export async function createFolder(userId, folderName, parentId) {
  const response = await fetch(`${API_BASE_URL}/folder/create`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: userId,
      folder_name: folderName,
      parent_id: parentId,
    }),
  });

  var result = await response.json();

  if (!response.ok)
    throw new Error(result?.message || "Failed to create folder");
  return await result.data;
}
export async function getFilePreview(fileId) {
  const response = await fetch(`/api/files/${fileId}/preview`);
  if (!response.ok) throw new Error("Failed to fetch file preview");
  return result;
}

export async function renameFolder(folderId, newName) {
  const response = await fetch(`${API_BASE_URL}/folder/rename`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: "USR0001",
      folder_id: folderId,
      new_folder_name: newName,
    }),
  });
  var result = await response.json();
  if (!response.ok)
    throw new Error(result?.message || "Failed to rename folder");
  return result.data;
}

export async function renameFile(fileId, newName) {
  const response = await fetch(`${API_BASE_URL}/file/rename`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: "USR0001",
      file_id: fileId,
      new_file_name: newName,
    }),
  });
  var result = await response.json();
  if (!response.ok) throw new Error(result?.message || "Failed to rename file");
  return result.data;
}

export async function deleteFolder(folderId) {
  const response = await fetch(`${API_BASE_URL}/folder/delete`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: "USR0001",
      folder_id: folderId,
    }),
  });

  var result = await response.json();
  if (!response.ok)
    throw new Error(result?.message || "Failed to delete folder");
  return result.data;
}

export async function deleteFile(file_id) {
  const response = await fetch(`${API_BASE_URL}/file/delete`, {
    method: "POST",
    headers: API_HEADERS,
    body: JSON.stringify({
      user_id: "USR0001",
      file_id: file_id,
    }),
  });

  var result = await response.json();
  if (!response.ok) throw new Error(result?.message || "Failed to delete File");
  return result.data;
}
