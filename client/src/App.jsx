import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// import { FolderFormPage } from "./pages/FolderFormPage";
import { OverviewPage } from "./pages/OverviewPage";
import { Navigation } from "./components/Navigation";
import { Toaster } from "react-hot-toast";
import {SideBar} from "./components/SideBar"
import { CreateFolder } from "./pages/CreateFolder";
import { ShowAllOfers } from "./pages/ShowAllOfers";
import { CreateProject } from "./pages/CreateProject";

function App() {
  return (
    <BrowserRouter>
      <div className="container-fluid">

        <div className="row">
            <Navigation />

        </div>
        <div className="row">
          <div className="col-md-3">
            <SideBar/>
          </div>
          <div className="col-md-9">
            <Routes>
              <Route path="/" element={<Navigate to="/home" />} />
              <Route path="/folder/:id" element={<OverviewPage />} />
              <Route path="/create-folder" element={<CreateFolder />} />
              <Route path="/show-all-offers" element={<ShowAllOfers />} />
              <Route path="/create-project" element={<CreateProject />} />
              <Route path="/create-project/:id" element={<CreateProject />} />
              {/* <Route path="/folder-create" element={<FolderFormPage />} />
            <Route path="/folder/:id" element={<FolderFormPage />} /> */}
            </Routes>
          </div>
        </div>
      </div>

      <Toaster />
    </BrowserRouter>
  );
}

export default App;
