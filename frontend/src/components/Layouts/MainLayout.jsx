// components/Layout/MainLayout.jsx
import Panel from "./Panel";
import Sidebar from "../Sidebars";
import Chat from "../Chat";
import FileViewer from "../Fileviewer";

export default function MainLayout() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Panel position="left" width="w-64">
        <Sidebar />
      </Panel>

      <Panel position="center" width="flex-1">
        <Chat />
      </Panel>

      <Panel position="right" width="w-96">
        <FileViewer />
      </Panel>
    </div>
  );
}
