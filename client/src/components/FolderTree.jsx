import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { CreateFolderModal } from "./CreateFolderModal";
import { toast } from "react-hot-toast";
import { deleteFolder, getAllFoldersTree } from "../api/folder.api";

const Folder = ({ folder, triggerReloadSideBar, triggerReloadFolderTree }) => {
  const [isOpen, setIsOpen] = useState(false);
  const toggleFolder = () => {
    setIsOpen(!isOpen);
  };

  const navigate = useNavigate();

  return (
    <li>
      {folder.children.length > 0 && (
        <span onClick={toggleFolder} style={{ cursor: "pointer" }}>
          {isOpen ? (
            <i className="bi bi-folder2-open mx-2"></i>
          ) : (
            <i className="bi bi-folder mx-2"></i>
          )}
        </span>
      )}

      <Link
        className="text-dark"
        to={`/folder/${folder.id}`}
        style={{ textDecoration: "none" }}
      >
        {folder.name}{" "}
      </Link>

      <button className="btn btn btn-sm">
        <i className="bi bi-folder-symlink"></i>
      </button>

      <button
        className="btn btn-ligth btn-sm"
        onClick={async () => {
          const accepted = window.confirm("Estas seguro?");
          if (accepted) {
            await deleteFolder(folder.id);
            triggerReloadSideBar();
            triggerReloadFolderTree();
            toast.success("Carpeta eliminada", {
              position: "bottom-right",
            });
            navigate("/home");
          }
        }}
      >
        <i className="bi bi-folder-x"></i>
      </button>

      {isOpen && folder.children.length > 0 && (
        <ul style={{ listStyle: "none" }}>
          {folder.children.map((child) => (
            <Folder
              key={child.id}
              folder={child}
              triggerReloadSideBar={triggerReloadSideBar}
              triggerReloadFolderTree={triggerReloadFolderTree}
            />
          ))}
        </ul>
      )}
    </li>
  );
};

export const FolderTree = ({ folders, triggerReloadSideBar }) => {
  const [reload, setReload] = useState(false);
  const navigate = useNavigate();

  const triggerReloadFolderTree = () => {
    setReload(!reload);
  };

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between">
        <span>Navegación</span>
        <button
          type="button"
          className="btn btn-success btn-sm"
          data-bs-toggle="modal"
          data-bs-target="#staticBackdrop"
          onClick={
            ()=>{
                navigate("/create-folder/")
            }
          }
        >
          <i className="bi bi-folder-plus"></i>
        </button>
        <CreateFolderModal
          triggerReloadSideBar={triggerReloadSideBar}
          reloadFolderTree={reload}
        />
      </div>
      <div className="card-body nav">
        <ul style={{ listStyle: "none" }}>
          {folders.map((folder) => (
            <Folder
              key={folder.id}
              folder={folder}
              triggerReloadSideBar={triggerReloadSideBar}
              triggerReloadFolderTree={triggerReloadFolderTree}
            />
          ))}
        </ul>
      </div>
    </div>
  );
};
