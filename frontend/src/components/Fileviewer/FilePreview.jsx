function FilePreview({ file }) {
  // This component will display the file preview based on the file type
  const renderPreview = () => {
    switch (file.type) {
      case "image":
        return (
          <img
            src={file.file_url}
            alt={file.file_name}
            className="w-full h-auto"
          />
        );
      case "video":
        return (
          <video controls className="w-full h-auto">
            <source src={file.file_url} />
          </video>
        );
      case "audio":
        return (
          <audio controls className="w-full h-auto">
            <source src={file.file_url} />
          </audio>
        );
      case "text":
        return <iframe src={file.file_url} className="w-full h-auto" />;
      default:
        return <div>Unsupported file type</div>;
    }
  };
}

export default FilePreview;
