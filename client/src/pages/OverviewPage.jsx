import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getFolder } from "../api/folder.api";
import { toast } from "react-hot-toast";
import { deleteFolder } from "../api/folder.api";
import { CreateFolderModal } from "../components/CreateFolderModal";
export function OverviewPage() {
  const { id } = useParams(); // Obtener el id de la URL
  const [folder, setFolder] = useState(null);
  const navigate = useNavigate()
   
  useEffect(() => {
    async function loadFolder() {
      if (id) {
        const { data } = await getFolder(id);
        // setValue('name',data.name)
        setFolder(data);
      }
    }
    loadFolder();
  }, [id]);

  if (!folder) {
    return <div>Folder no existe</div>;
  }

  return (
    <div className="container">
        <CreateFolderModal/>
      <div className="row">
        <div className="col-md-3"></div>
        <div className="col-md-6">
        <span className="mx-2">ID: {folder.id}</span>
        <span className="mx-2">NOMBRE: {folder.name}</span>
        </div>
        <div className="col-md-3 ">
        <button type="button" class="btn btn-success btn-sm" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
        Cambiar ruta
        </button>
        </div>
      </div>
    </div>
  );
}
