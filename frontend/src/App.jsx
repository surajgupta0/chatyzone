// App.jsx
import { AppProvider } from "./context/AppContext";
import MainLayout from "./components/Layouts/MainLayout";

function App() {
  return (
    <AppProvider>
      <MainLayout />
    </AppProvider>
  );
}

export default App;
