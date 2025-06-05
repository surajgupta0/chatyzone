// components/FileViewer/FileMetadata.jsx
import { formatBytes, formatDate } from "../../utils/format";

export default function FileMetadata({ file }) {
  if (!file) return null;

  const metadata = [
    { label: "Type", value: file.file_ext },
    { label: "Size", value: formatBytes(file.file_size) },
    { label: "Created", value: formatDate(file.created_at) },
    { label: "Location", value: file.file_path },
  ];

  return (
    <div className="pt-4 mt-4">
      <h3 className="font-medium mb-3">File Details</h3>
      <div className="space-y-2">
        {metadata.map((item, index) => (
          <div key={index} className="grid grid-cols-3 text-sm">
            <span className="text-gray-500">{item.label}</span>
            <span className="col-span-2">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
