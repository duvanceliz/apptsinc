import { getAllProjects } from "../api/folder.api";
import { useEffect, useState } from "react";
import { Table } from "../components/Table";
import { Link } from "react-router-dom";
export function ShowAllOfers() {
  const [projects, setProjects] = useState([]);
  const [reload, setReload] = useState(false);

  useEffect(() => {
    async function loadProjects() {
      const { data } = await getAllProjects();
      setProjects(data);
    }
    loadProjects();
  }, [reload]);

  const triggerReloadOffers = () => {
    setReload(!reload);
  };

  return (
    <div className="Container">
      <div className="row">
      
        <div className="col-md-12">
          <Link to={"/create-project"} className="btn btn-success btn-sm">
            New
          </Link>
          <Table
            projects={projects}
            triggerReloadOffers={triggerReloadOffers}
          />
        </div>
     
      </div>
    </div>
  );
}
